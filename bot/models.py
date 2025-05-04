# bot/models.py

from django.db import models
from django.contrib.auth.models import User
from django_cryptography.fields import encrypt  # Добавляем шифрование
from django.contrib.auth.models import User


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Связь с пользователем
    symbol = models.CharField(max_length=10)  # Символ ордера, например BTCUSDT
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Количество
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена
    status = models.CharField(max_length=20, default="pending")  # Статус ордера
    created_at = models.DateTimeField(auto_now_add=True)  # Время создания ордера
    updated_at = models.DateTimeField(auto_now=True)  # Время последнего обновления ордера

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"




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
