from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import ChatMessage

@login_required
def help_chat(request):
    """User help page"""
    chats = ChatMessage.objects.filter(user=request.user)

    if request.method == "POST":
        message = request.POST.get("message")
        if message:
            ChatMessage.objects.create(user=request.user, message=message)
        return redirect("help_chat")

    return render(request, "chat/help_chat.html", {"chats": chats})


@user_passes_test(lambda u: u.is_staff)  # only staff/admins
def admin_chat(request):
    """Admin chat dashboard"""
    chats = ChatMessage.objects.all()

    if request.method == "POST":
        chat_id = request.POST.get("chat_id")
        response = request.POST.get("response")

        chat = get_object_or_404(ChatMessage, id=chat_id)
        chat.response = response
        chat.is_resolved = True
        chat.save()

        return redirect("admin_chat")

    return render(request, "chat/admin_chat.html", {"chats": chats})
from django.shortcuts import render, redirect
from .models import ChatMessage
from django.contrib.auth.decorators import login_required

@login_required
def help_chat(request):
    if request.method == "POST":
        message = request.POST.get("message")
        if message:
            ChatMessage.objects.create(user=request.user, message=message)
            return redirect("help_chat")  # refresh after sending

    chats = ChatMessage.objects.filter(user=request.user).order_by("-timestamp")
    return render(request, "chat/help_chat.html", {"chats": chats})
import openai
from django.conf import settings

def bot_response(user_message):
    openai.api_key = settings.OPENAI_API_KEY

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",   # You can use gpt-4o if available
            messages=[
                {"role": "system", "content": "You are AutoVendor's helpful car assistant. Answer professionally about cars, prices, financing, and services."},
                {"role": "user", "content": user_message},
            ],
            max_tokens=200,
            temperature=0.7,
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ Error: {str(e)}"
from django.shortcuts import render
from django.http import JsonResponse
from .utils import bot_response

def help_chat(request):
    if request.method == "POST":
        user_message = request.POST.get("message")
        reply = bot_response(user_message)
        return JsonResponse({"reply": reply})
    return render(request, "chat/help_chat.html")

from django.http import StreamingHttpResponse
from django.conf import settings
from openai import OpenAI

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def help_chat(request):
    return render(request, "chat/help_chat.html")

def stream_chat(request):
    prompt = request.GET.get("prompt", "Hello AI")
    response = client.responses.create(
        model="gpt-5",
        input=prompt,
    )
    return StreamingHttpResponse(response.output_text)
from django.http import JsonResponse
from openai import OpenAI
import os

# 👇 Better to load from settings or .env instead of hardcoding
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def stream_chat(request):
    user_message = request.GET.get("message", "Hello AI")
    
    response = client.responses.create(
        model="gpt-4o-mini",
        input=user_message,
        store=True,
    )
    
    return JsonResponse({"reply": response.output_text})
from django.http import StreamingHttpResponse