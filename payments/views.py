from django.shortcuts import render

# Create your views here.
# payments/views.py
import json, uuid, hmac, hashlib
from django.conf import settings
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Payment
from .paystack import initialize_transaction, verify_transaction

def create_checkout(request):
    """
    Renders a page with a 'Pay Now' button (ATM card + bank transfer via Paystack popup).
    Change the demo amount/email to dynamic values in your app.
    """
    context = {
        "public_key": settings.PAYSTACK_PUBLIC_KEY,
        "email": "customer@example.com",
        "amount": 500000,  # ₦5,000 in kobo
    }
    return render(request, "payments/checkout.html", context)

def api_initialize(request):
    """
    Server-side initialize. Returns auth URL if you prefer redirect checkout.
    Not required for inline popup, but good for server-side trust.
    """
    if request.method != "POST":
        return HttpResponseBadRequest("POST only")

    data = json.loads(request.body.decode() or "{}")
    email = data.get("email")
    amount = int(data.get("amount", 0))  # kobo
    if not email or amount <= 0:
        return HttpResponseBadRequest("email and amount required")

    reference = uuid.uuid4().hex

    payment = Payment.objects.create(
        reference=reference,
        email=email,
        amount=amount,
        metadata={"source": "api_initialize"}
    )

    init_res = initialize_transaction(email, amount, reference, payment.metadata)
    if not init_res.get("status"):
        # Mark as failed to initialize
        payment.status = "failed"
        payment.save(update_fields=["status"])
        return JsonResponse({"ok": False, "error": init_res.get("message", "init failed")}, status=400)

    data = init_res["data"]
    return JsonResponse({"ok": True, "authorization_url": data["authorization_url"], "reference": reference})

def verify(request):
    """
    Called after client callback: ?reference=xxxx
    Verifies with Paystack and updates DB.
    """
    reference = request.GET.get("reference")
    if not reference:
        return HttpResponseBadRequest("missing reference")

    payment = get_object_or_404(Payment, reference=reference)
    res = verify_transaction(reference)
    if not res.get("status"):
        payment.status = "failed"
        payment.save(update_fields=["status"])
        return render(request, "payments/result.html", {"payment": payment, "ok": False, "msg": res.get("message")})

    data = res["data"]
    status = data.get("status")  # 'success' | 'failed' | 'abandoned'
    auth = data.get("authorization") or {}
    payment.status = status
    payment.authorization_code = auth.get("authorization_code", "") or ""
    payment.metadata.update({"gateway_response": data.get("gateway_response")})
    payment.save()

    return render(request, "payments/result.html", {"payment": payment, "ok": status == "success"})

@csrf_exempt
def webhook(request):
    """
    Paystack webhook to auto-update on 'charge.success'.
    Set the URL in your Paystack dashboard.
    """
    if request.method != "POST":
        return HttpResponseBadRequest("POST only")

    signature = request.headers.get("x-paystack-signature")
    body = request.body
    # Validate signature
    expected = hmac.new(
        key=settings.PAYSTACK_SECRET_KEY.encode("utf-8"),
        msg=body,
        digestmod=hashlib.sha512
    ).hexdigest()

    if not signature or signature != expected:
        return HttpResponseForbidden("Invalid signature")

    event = json.loads(body.decode())
    event_type = event.get("event")
    data = event.get("data", {})
    reference = data.get("reference")

    if event_type == "charge.success" and reference:
        try:
            payment = Payment.objects.get(reference=reference)
            payment.status = "success"
            auth = data.get("authorization") or {}
            payment.authorization_code = auth.get("authorization_code", "") or ""
            payment.metadata.update({"webhook": True})
            payment.save()
        except Payment.DoesNotExist:
            pass

    return HttpResponse("OK")
# payments/views.py
import uuid
from django.shortcuts import render
from django.conf import settings

def create_checkout(request):
    context = {
        "public_key": settings.PAYSTACK_PUBLIC_KEY,
        "email": "customer@example.com",
        "amount": 500000,  # ₦5,000 in kobo
        "reference": uuid.uuid4().hex,  # safe unique ref
    }
    return render(request, "payments/checkout.html", context)
