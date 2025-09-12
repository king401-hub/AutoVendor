# payments/paystack.py
import os, requests
from django.conf import settings

BASE_URL = "https://api.paystack.co"

def headers():
    return {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }

def initialize_transaction(email: str, amount: int, reference: str, metadata: dict):
    url = f"{BASE_URL}/transaction/initialize"
    payload = {
        "email": email,
        "amount": amount,            # in kobo
        "reference": reference,
        "currency": "NGN",
        "channels": ["card", "bank_transfer"],  # enable ATM card + bank transfer
        "metadata": metadata or {},
    }
    return requests.post(url, json=payload, headers=headers()).json()

def verify_transaction(reference: str):
    url = f"{BASE_URL}/transaction/verify/{reference}"
    return requests.get(url, headers=headers()).json()
