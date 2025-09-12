from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png')
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username

from django.db import models

class Car(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to="cars/")

    def __str__(self):
        return f"{self.brand} {self.name} ({self.year})"
