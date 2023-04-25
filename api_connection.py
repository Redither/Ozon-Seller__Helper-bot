from urllib import request
import json
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from retrying import retry

        
SELLER = os.environ.get('CLIENT_ID')
KEY = os.environ.get('API_KEY')


last_month = datetime.today().month -1
if last_month < 1:
    last_month = 12
else:
    last_month = last_month

today = datetime.now().date()
today_of_prev_month = datetime.today().replace(month= last_month)
first_day = datetime.now().date().replace(day=1)
last_day_of_prev_month = datetime.today().replace(day=1) - timedelta(days=1)
start_day_of_prev_month = datetime.today().replace(day=1) - timedelta(days=last_day_of_prev_month.day)
if today.day > last_day_of_prev_month.day:
    today_of_prev_month = last_day_of_prev_month
else:
    today_of_prev_month = today_of_prev_month


url = "https://api-seller.ozon.ru/v1/analytics/data"
    # укажите заголовки запроса
headers = {
    "Content-Type": "application/json",
    # укажите свой магазин ID и API ключ
    "Client-Id": SELLER,
    "Api-Key": KEY
}

@retry(stop_max_attempt_number=5, wait_fixed=5000)
def get_sales_month():    
    # укажите требуемые данные для создания товара в виде словаря
    request_data = {
    "date_from": str(first_day),
    "date_to": str(today),
    "metrics": [
        "revenue",
        "ordered_units"
    ],
    "dimension": [
        "sku",
        "month"
    ],
    "filters": [],
    "sort": [
        {
            "key": "revenue",
            "order": "DESC"
        }
    ],
    "limit": 1000,
    "offset": 0
    }

    data = json.dumps(request_data).encode('utf-8')
    try:
        req = request.Request(url, headers=headers, data=data, method="POST")
        r = request.urlopen(req)
        # получите ответ в формате json
        result = json.loads(r.read().decode('utf-8'))['result']
        return result
    except request.HTTPError as e:
        if e.response.status_code == 429:
          print("Сервер вернул ошибку 429: слишком много запросов")
          raise e  # повторяем попытку выполнения запроса
        else:
          raise  # пробрасываем ошибку дальше

@retry(stop_max_attempt_number=5, wait_fixed=5000)
def get_sales_today():
    request_data = {
        "date_from": str(today),
        "date_to": str(today),
        "metrics": [
            "revenue",
            "ordered_units"
        ],
        "dimension": [
            "sku",
            "day"
        ],
        "filters": [],
        "sort": [
            {
                "key": "revenue",
                "order": "DESC"
            }
        ],
        "limit": 1000,
        "offset": 0
    }
    data = json.dumps(request_data).encode('utf-8')
    try:
        req = request.Request(url, headers=headers, data=data, method="POST")
        r = request.urlopen(req)
        # получите ответ в формате json
        result = json.loads(r.read().decode('utf-8'))['result']
        return result
    except request.HTTPError as e:
        if e.response.status_code == 429:
          print("Сервер вернул ошибку 429: слишком много запросов")
          raise e  # повторяем попытку выполнения запроса
        else:
          raise  # пробрасываем ошибку дальше

@retry(stop_max_attempt_number=5, wait_fixed=5000)
def get_sales_today__last():
    # укажите требуемые данные для создания товара в виде словаря
    request_data = {
    "date_from": str(today_of_prev_month),
    "date_to": str(today_of_prev_month),
    "metrics": [
        "revenue",
        "ordered_units"
    ],
    "dimension": [
        "sku",
        "day"
    ],
    "filters": [],
    "sort": [
        {
            "key": "revenue",
            "order": "DESC"
        }
    ],
    "limit": 1000,
    "offset": 0
    }

    data = json.dumps(request_data).encode('utf-8')
    try:
        req = request.Request(url, headers=headers, data=data, method="POST")
        r = request.urlopen(req)
        # получите ответ в формате json
        result = json.loads(r.read().decode('utf-8'))['result']
        return result
    except request.HTTPError as e:
        if e.response.status_code == 429:
          print("Сервер вернул ошибку 429: слишком много запросов")
          raise e  # повторяем попытку выполнения запроса
        else:
          raise  # пробрасываем ошибку дальше

@retry(stop_max_attempt_number=5, wait_fixed=5000)
def get_sales_month__last():    
    # укажите требуемые данные для создания товара в виде словаря
    request_data = {
    "date_from": str(start_day_of_prev_month),
    "date_to": str(today_of_prev_month),
    "metrics": [
        "revenue",
        "ordered_units"
    ],
    "dimension": [
        "sku",
        "month"
    ],
    "filters": [],
    "sort": [
        {
            "key": "revenue",
            "order": "DESC"
        }
    ],
    "limit": 1000,
    "offset": 0
    }

    data = json.dumps(request_data).encode('utf-8')
    try:
        req = request.Request(url, headers=headers, data=data, method="POST")
        r = request.urlopen(req)
        # получите ответ в формате json
        result = json.loads(r.read().decode('utf-8'))['result']
        return result
    except request.HTTPError as e:
        if e.response.status_code == 429:
          print("Сервер вернул ошибку 429: слишком много запросов")
          raise e  # повторяем попытку выполнения запроса
        else:
          raise  # пробрасываем ошибку дальше


def find_object_by_id(data, list):
    needed = []
    for id in list:
        for item in data:
            if item['dimensions'][0]['id'] in id:
                needed.append(item)
    return needed
