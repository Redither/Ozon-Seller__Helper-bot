import time
import logging
import re
import os
from datetime import datetime
# import calendar
import db_connection
import api_connection

from time import sleep

from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from aiogram import Bot, Dispatcher, executor, types

from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN = os.environ.get('TOKEN')
USER = os.environ.get('USER_ID')
CHAT = os.environ.get('CHAT_ID')
MESSAGE_TIME = os.environ.get('MESSAGE_TIME')
time_h, time_m = MESSAGE_TIME.split(':')
# PARAM_TIME = db_connection.get_setting_value('time')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


scheduler = AsyncIOScheduler(timezone="Europe/Moscow")


async def send_statistic(bot: Bot):
    today = datetime.now().date()
    # first_day = today.replace(day=1)
    # last_day = first_day.replace(day = calendar.monthrange(2023, 4)[1])
    try:
        plan = db_connection.get_sales_plan(today.strftime('%Y-%m'))
    except TypeError:
        print('План не введен или данные не действительны')
        await bot.send_message(CHAT, f'Не указан план продаж на этот месяц!')
        plan = 0
        
    if type(plan) != int:
        await message.reply('Не указан план продаж на этот месяц!')
    else:
        result = api_connection.get_sales_month()
        total = result['totals'][0]
        data = result['data'][0:5]
        ids = []
        for item in data:
            ids.append(item['dimensions'][0]['id'])
        sleep(5)
        results_day = api_connection.find_object_by_id(api_connection.get_sales_today()['data'], ids)
        sleep(5)
        results_day_pm = api_connection.find_object_by_id(api_connection.get_sales_today__last()['data'], ids)
        sleep(5)
        results_month_pm = api_connection.find_object_by_id(api_connection.get_sales_month__last()['data'], ids)

        top_sales = ""
        for idx, element in enumerate(data):
            name = element['dimensions'][0]['name']
            num = int(element['metrics'][1])
            num_d = int(results_day[idx]['metrics'][1])
            num_lm = int(results_month_pm[idx]['metrics'][1])
            num_ld = int(results_day_pm[idx]['metrics'][1])

            growth_m = ''
            if num_lm == 0:
                if num == 0:
                    growth_m = 0
                else:
                    growth_m = 100
            else:
                growth_m = round((num - num_lm)/num_lm*100, 2)

            growth_d = ''
            if num_ld == 0:
                if num_d == 0:
                    growth_d = 0
                else:
                    growth_d = 100
            else:
                growth_d = round((num_d - num_ld)/num_ld*100, 2)

            top_sales += (f'{name}\n*1M* {num} ({growth_m})% *1D* {num_d} ({growth_d})%\n\n')

        await message.reply(f'Данные по статистике на {today}:\n\nВыручка общая: {total}/{plan}/{round(total/plan*100, 2)}%\n\nТоп-5 по продажам:\n{top_sales}\n\n', parse_mode='markdown')

scheduler.add_job(send_statistic, trigger='cron', hour = time_h, minute = time_m, start_date = datetime.now(), kwargs = {'bot': bot})
    

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    if str(message.from_user.id) != USER:
        await message.reply(f"Недостаточно прав!")
        return
    else:
        await message.reply(f"Здравствуйте!\n Я Ваш персональный бот-аналитик для работы с *OZON!*\n Для получения статистики введите /statistic\n Чтобы ввести/изменить план продаж, введите /plan ", parse_mode='markdown')


@dp.message_handler(commands=['statistic'])
async def statistic_handler(message: types.Message):
    if str(message.chat.id) not in [CHAT, USER]:
        await message.reply(f"Недостаточно прав!")
        return
    else:
        today = datetime.now().date()
        # first_day = today.replace(day=1)
        # last_day = first_day.replace(day = calendar.monthrange(2023, 4)[1])
        plan = db_connection.get_sales_plan(today.strftime('%Y-%m'))
        if type(plan) != int:
            await message.reply('Не указан план продаж на этот месяц!')
        else:
            result = api_connection.get_sales_month()
            total = result['totals'][0]
            data = result['data'][0:5]
            ids = []
            for item in data:
                ids.append(item['dimensions'][0]['id'])
            sleep(5)
            results_day = api_connection.find_object_by_id(api_connection.get_sales_today()['data'], ids)
            sleep(5)
            results_day_pm = api_connection.find_object_by_id(api_connection.get_sales_today__last()['data'], ids)
            sleep(5)
            results_month_pm = api_connection.find_object_by_id(api_connection.get_sales_month__last()['data'], ids)

            top_sales = ""
            for idx, element in enumerate(data):
                name = element['dimensions'][0]['name']
                num = int(element['metrics'][1])
                num_d = int(results_day[idx]['metrics'][1])
                num_lm = int(results_month_pm[idx]['metrics'][1])
                num_ld = int(results_day_pm[idx]['metrics'][1])

                growth_m = ''
                if num_lm == 0:
                    if num == 0:
                        growth_m = 0
                    else:
                        growth_m = 100
                else:
                    growth_m = round((num - num_lm)/num_lm*100, 2)

                growth_d = ''
                if num_ld == 0:
                    if num_d == 0:
                        growth_d = 0
                    else:
                        growth_d = 100
                else:
                    growth_d = round((num_d - num_ld)/num_ld*100, 2)

                top_sales += (f'{name}\n*1M* {num} ({growth_m})% *1D* {num_d} ({growth_d})%\n\n')
            await message.reply(f'Данные по статистике на {today}:\n\nВыручка общая: {total}/{plan}/{round(total/plan*100, 2)}%\n\nТоп-5 по продажам:\n{top_sales}\n\n', parse_mode='markdown')


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
    scheduler.start()
    executor.start_polling(dp)