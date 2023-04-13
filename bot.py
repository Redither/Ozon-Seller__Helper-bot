import time
import logging
import asyncio
import os
from datetime import datetime
import calendar

from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from aiogram import Bot, Dispatcher, executor, types

TOKEN = os.environ.get('TOKEN')
USER = os.environ.get('USER_ID')
CHAT = os.environ.get('CHAT_ID')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

def isAdmin(id):
    if id not in USER:
        return True
    else:
        return False
    

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    # должно логать действия
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id} {user_full_name} {time.asctime()}')

    if isAdmin(message.from_user.id):
        await message.reply(f"Недостаточно прав!")
        return
    else:
        await message.reply(f"Здравствуйте!\n Я Ваш персональный бот-аналитик для работы с __**OZON!**__\n Для получения сводки введите /svodka\n Чтобы ввести/изменить план продаж введите /plan ")

@dp.message_handler(commands=['svodka'])
async def svodka_handler(message: types.Message):
    today = datetime.now().date()
    first_day = today.replace(day=1)
    last_day = today.replace(day = calendar.monthrange(2023, 4)[1])
    REQUEST = {
        "date_from": first_day.strftime('%Y-%M-%D'),
        "date_to": last_day.strftime('%Y-%M-%D'),
        "metrics": [
            "revenue"
        ],
        "dimension": [
            "day",
            "month"
        ],
        "filters": [ ],
        "sort": [
            {
                "key": "revenue",
                "order": "DESC"
            }
        ],
        "limit": 1000,
        "offset": 0
    }
    await message.reply(f'{today} + {type(today)}, {first_day} + {type(first_day)}, {last_day} + {type(last_day)}')


if __name__ == "__main__":
    executor.start_polling(dp)