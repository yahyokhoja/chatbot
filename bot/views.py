# bot/views.py

import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST

from .forms import APIKeyForm
from .models import APIKey
from .bybit_api import make_bybit_request

# ============================== #
# Основные страницы
# ============================== #

def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def logout_view(request):
    return render(request, 'logout.html')

# ============================== #
# Профиль пользователя
# ============================== #

@login_required
def profile(request):
    keys_exist = APIKey.objects.filter(user=request.user).exists()
    return render(request, 'profile.html', {'keys_exist': keys_exist})

# ============================== #
# Работа с API-ключами
# ============================== #

@login_required
def add_api_key(request):
    if request.method == 'POST':
        form = APIKeyForm(request.POST)
        if form.is_valid():
            api_key_text = form.cleaned_data['api_key']
            api_secret_text = form.cleaned_data['api_secret']

            # Создание или обновление ключей
            api_key_obj, _ = APIKey.objects.get_or_create(user=request.user)
            api_key_obj.save_keys(api_key_text, api_secret_text)

            messages.success(request, "API-ключ успешно добавлен или обновлен.")
            return redirect('profile')
    else:
        form = APIKeyForm()

    return render(request, 'add_api_key.html', {'form': form})

@login_required
@require_POST
def delete_api_key(request):
    try:
        api_key_obj = APIKey.objects.get(user=request.user)
        api_key_obj.delete()
        messages.success(request, "Ваш API-ключ успешно удалён.")
    except APIKey.DoesNotExist:
        messages.error(request, "У вас нет сохранённого API-ключа.")

    return redirect('profile')

# ============================== #
# Работа с Bybit
# ============================== #

def narh_view(request):
    try:
        url = "https://api.bybit.com/v5/market/tickers?category=linear&symbol=BTCUSDT"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            price = res.json()['result']['list'][0]['lastPrice']
        else:
            price = f"Ошибка API: {res.status_code}"
    except Exception as e:
        price = f"Ошибка: {e}"

    return render(request, 'narh.html', {'price': price})

@login_required
def some_protected_view(request):
    try:
        api_key_obj = APIKey.objects.get(user=request.user)
    except APIKey.DoesNotExist:
        messages.error(request, "Сначала добавьте свой API-ключ.")
        return redirect('add_api_key')

    api_key = api_key_obj.api_key
    secret_key = api_key_obj.api_secret

    params = {'symbol': 'BTCUSDT'}
    response = make_bybit_request(api_key, secret_key, '/v2/public/tickers', params)

    return render(request, 'some_template.html', {'response': response})
