from django.contrib import admin
from django.urls import path, include  # Убедись, что include импортирован

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bot.urls')),  # Подключение маршрутов из приложения 'bot'
    # Другие маршруты, если они есть
]
