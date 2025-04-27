# bot/bybit_api.py
import time
import hmac
import hashlib
import requests

def make_bybit_request(api_key, secret_key, endpoint, params=None):
    url = f"https://api.bybit.com{endpoint}"

    if params is None:
        params = {}

    # Добавляем обязательные параметры
    params.update({
        'api_key': api_key,
        'timestamp': int(time.time() * 1000),
        'recv_window': 5000,
    })

    # Создаем строку для подписи
    sorted_params = sorted(params.items())
    query_string = '&'.join(f"{k}={v}" for k, v in sorted_params)
    signature = hmac.new(secret_key.encode(), query_string.encode(), hashlib.sha256).hexdigest()

    # Добавляем подпись
    params['sign'] = signature

    response = requests.get(url, params=params)

    return response.json()
