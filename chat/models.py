from django.db import models
from django.conf import settings   # import this

class ChatMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # <-- FIXED
    message = models.TextField()
    response = models.TextField(blank=True, null=True)
    is_resolved = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat from {self.user} at {self.timestamp}"
