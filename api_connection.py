from urllib import request
import json
import os
from datetime import datetime

from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

SELLER = os.environ.get('CLIENT_ID')
KEY = os.environ.get('API_KEY')

today = str(datetime.now().date())
first_day = str(datetime.now().date().replace(day=1))

def get_sales():
    url = "https://api-seller.ozon.ru/v1/analytics/data"

    # укажите требуемые данные для создания товара в виде словаря
    request_data = {
    "date_from": first_day,
    "date_to": today,
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
    # укажите заголовки запроса
    headers = {
    "Content-Type": "application/json",
    # укажите свой магазин ID и API ключ
    "Client-Id": SELLER,
    "Api-Key": KEY
    }

    data = json.dumps(request_data).encode('utf-8')
    req = request.Request(url, headers=headers, data=data, method="POST")
    r = request.urlopen(req)
    # получите ответ в формате json
    result = json.loads(r.read().decode('utf-8'))['result']

    return result
