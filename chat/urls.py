# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("help/", views.help_chat, name="help_chat"),
    path("stream/", views.stream_chat, name="stream_chat"),  # ✅ no leading slash
]
