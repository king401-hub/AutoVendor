from django.contrib.auth.models import AbstractUser
from django.db import models
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