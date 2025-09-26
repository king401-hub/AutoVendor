from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png')
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    theme_preference = models.CharField(max_length=10, choices=[
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('auto', 'Auto')
    ], default='auto')
    profile_visibility = models.CharField(max_length=10, choices=[
        ('public', 'Everyone'),
        ('registered', 'Registered users only'),
        ('none', 'Only me')
    ], default='public')
    contact_preference = models.CharField(max_length=10, choices=[
        ('public', 'Everyone'),
        ('registered', 'Registered users only'),
        ('none', 'No one')
    ], default='public')
    data_collection = models.BooleanField(default=True)
    personalized_ads = models.BooleanField(default=True)
    two_factor_auth = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Car(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to="cars/")

    def __str__(self):
        return f"{self.brand} {self.name} ({self.year})"

# Use settings.AUTH_USER_MODEL for all related user fields
class AccountSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="account_settings")

    # Password change handled by Django’s built-in auth, no need to store here
    two_factor_enabled = models.BooleanField(default=False)

    google_connected = models.BooleanField(default=False)
    facebook_connected = models.BooleanField(default=False)
    twitter_connected = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - Account Settings"


class NotificationSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notification_settings")

    # Email
    email_notifications = models.BooleanField(default=True)
    marketing_emails = models.BooleanField(default=True)
    newsletter = models.BooleanField(default=True)

    # Push
    push_notifications = models.BooleanField(default=True)
    new_messages = models.BooleanField(default=True)
    price_alerts = models.BooleanField(default=True)

    # SMS
    sms_notifications = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - Notification Settings"


class PrivacySettings(models.Model):
    PROFILE_VISIBILITY_CHOICES = [
        ("public", "Everyone"),
        ("registered", "Registered users only"),
        ("none", "Only me"),
    ]

    CONTACT_CHOICES = [
        ("public", "Everyone"),
        ("registered", "Registered users only"),
        ("none", "No one"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="privacy_settings")

    data_collection = models.BooleanField(default=True)
    personalized_ads = models.BooleanField(default=True)

    profile_visibility = models.CharField(max_length=20, choices=PROFILE_VISIBILITY_CHOICES, default="public")
    contact_permission = models.CharField(max_length=20, choices=CONTACT_CHOICES, default="public")

    def __str__(self):
        return f"{self.user.username} - Privacy Settings"


class AppearanceSettings(models.Model):
    THEME_CHOICES = [
        ("light", "Light"),
        ("dark", "Dark"),
        ("auto", "Auto"),
    ]

    DENSITY_CHOICES = [
        ("comfortable", "Comfortable"),
        ("compact", "Compact"),
        ("spacious", "Spacious"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="appearance_settings")

    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default="light")
    language = models.CharField(max_length=50, default="English")
    display_density = models.CharField(max_length=20, choices=DENSITY_CHOICES, default="comfortable")

    def __str__(self):
        return f"{self.user.username} - Appearance Settings"
    def __str__(self):
        return f"{self.user.username} - Appearance Settings"

