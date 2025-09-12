from django.db import models

# Create your models here.
from django.db import models

class Payment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
        ("abandoned", "Abandoned"),
    ]

    reference = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    amount = models.PositiveIntegerField(help_text="Amount in kobo (₦5000 => 500000)")
    currency = models.CharField(max_length=10, default="NGN")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    metadata = models.JSONField(default=dict, blank=True)
    authorization_code = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_successful(self):
        return self.status == "success"

    def __str__(self):
        return f"{self.email} — {self.reference} — {self.status}"
