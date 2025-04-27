# bot/models.py

from django.db import models
from django.contrib.auth.models import User
from django_cryptography.fields import encrypt  # Добавляем шифрование

class APIKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    api_key = encrypt(models.CharField(max_length=255))
    api_secret = encrypt(models.CharField(max_length=255))

    def __str__(self):
        return f"API Key for {self.user.username}"

    def save_keys(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.save()
