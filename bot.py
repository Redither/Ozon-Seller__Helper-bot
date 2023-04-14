import time
import logging
import re
import os
from datetime import datetime
import calendar
import db_connection

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

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    # должно логать действия
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id} {user_full_name} {time.asctime()}')

    if str(message.from_user.id) != USER:
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

@dp.message_handler(commands=['plan'])
async def plan_handler(message: types.Message):
    if str(message.from_user.id) != USER:
        await message.reply(f"Недостаточно прав!")
        return
    else:
        if not message.get_args():
            await message.reply("Для того, чтобы ввести или изменить план продаж на месяц, отправьте сообщение:\n /plan ГГГГ-ММ СУММА \n\n Пример:\n\n /plan 2023-04 2000000\n\n\nПримечание: Изменить план продаж может только директор!")
        else:
            if not re.fullmatch('\d\d\d\d\D\d\d \d+', message.get_args()):
                await message.reply("Данные введены некорректно! Попробуйте снова!")
            else:
                id, plan = message.get_args().split()
                id = re.compile('\D').sub('-', id)
                db_connection.add_sales_plan(id, plan)
                await message.reply(f"Данные сохранены!\n На месяц {id} установлен план {plan}")


if __name__ == "__main__":
    executor.start_polling(dp)