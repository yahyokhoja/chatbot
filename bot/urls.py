# urls.py
from django.urls import path
from . import views
from django.contrib import admin  # Добавьте импорт для admin
from .views import narh_view

urlpatterns = [

    path('', views.index, name='index'),  # Главная страница

    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('orders/', views.orders, name='orders'),
    path('logout/', views.logout_view, name='logout'),
    path('narh/', narh_view, name='narh'),
    path('add-api-key/', views.add_api_key, name='add_api_key'),  # добавляем маршрут для API-ключей

    path('some-protected-view/', views.some_protected_view, name='some_protected_view'),
    ]
