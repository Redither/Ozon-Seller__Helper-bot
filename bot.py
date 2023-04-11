import time
import logging
import asyncio
import os

from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from aiogram import Bot, Dispatcher, executor, types

TOKEN = os.environ.get('TOKEN')
MSG = "Программировал ли ты сегодня, {}?"
USER = os.environ.get('USER_ID')
CHAT = os.environ.get('CHAT_ID')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

@dp.message_handler(commands=['start'])

async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id} {user_full_name} {time.asctime()}')
    if user_id != USER:
        await message.reply(f"Пошел нахуй, {user_full_name}!")
    else:
        await message.reply(f"Добро пожаловать, {user_full_name}!")

    for i in range(7):
        await asyncio.sleep(60*60*24)
        await bot.send_message(user_id, MSG.format(user_name))

if __name__ == "__main__":
    executor.start_polling(dp)