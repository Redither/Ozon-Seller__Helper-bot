import time
import logging
import re
import os
from datetime import datetime
import calendar
import db_connection
import api_connection

from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from aiogram import Bot, Dispatcher, executor, types

TOKEN = os.environ.get('TOKEN')
USER = os.environ.get('USER_ID')
CHAT = os.environ.get('CHAT_ID')

PARAM_UNMUTE = db_connection.get_setting_value('UNMUTE')
PARAM_TIME = db_connection.get_setting_value('time')

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
        await message.reply(f"Здравствуйте!\n Я Ваш персональный бот-аналитик для работы с **OZON!**\n Для получения статистики введите /statistic\n Чтобы ввести/изменить план продаж, введите /plan ")

@dp.message_handler(commands=['statistic'])
async def svodka_handler(message: types.Message):
    today = datetime.now().date()
    first_day = today.replace(day=1)
    last_day = first_day.replace(day = calendar.monthrange(2023, 4)[1])
    total = 865342
    plan = db_connection.get_sales_plan(today.strftime('%Y-%m'))
    if type(plan) != int:
        await message.reply('Не указан план продаж на этот месяц!')
    else:
        result = api_connection.get_sales()
        total = result['totals'][0]
        data = result['data'][0:5]
        top_sales = ""
        for element in data:
            name = element['dimensions'][0]['name']
            num = element['metrics'][1]
            sum = element['metrics'][0]
            top_sales += (f'{name}\nПродано {num} штук на {sum} рублей\n\n')

        await message.reply(f'Данные по статистике на {today}:\n\nВыручка общая: {total}/{plan}/{total/plan*100}%\n\nТоп-5 по продажам:\n{top_sales}\n\n')

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

@dp.message_handler(commands=['speak'])
async def plan_handler(message: types.Message):
    if str(message.from_user.id) != USER:
        await message.reply(f"Недостаточно прав!")
        return
    else:
        if PARAM_UNMUTE == "True":
            db_connection.change_settings("UNMUTE", "False")
            await message.reply("Ежедневное сообщение отключено")
        else:
            db_connection.change_settings("UNMUTE", "True")
            await message.reply("Ежедневное сообщение включено")

@dp.message_handler(commands=['message'])
async def plan_handler(message: types.Message):
    if str(message.from_user.id) != USER:
        await message.reply(f"Недостаточно прав!")
        return
    else:
        if not message.get_args():
            await message.reply("Для того, чтобы изменить время оповещения о статистике, отправьте сообщение:\n /message ЧЧ:ММ \n\n Пример:\n\n /message 09:00\n\n\nПримечание: Изменить план продаж может только директор!")
        else:
            if not re.fullmatch('\d\d\D\d\d', message.get_args()):
                await message.reply("Данные введены некорректно! Попробуйте снова!")
            else:
                value = message.get_args().split()
                value = re.compile('\D').sub(':', id)
                db_connection.add_sales_plan("time", value)
                
                await message.reply(f"Данные сохранены!\n Теперь сообщения будут отсылаться в {value}")
        
if __name__ == "__main__":
    executor.start_polling(dp)