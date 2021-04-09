import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.chat import Chat

import json
with open('config.json') as f:
    credentials = json.load(f)

API_TOKEN = credentials['API_TOKEN']

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
CHAT_ID = int(credentials['CHAT_ID'])
USER_ID = int(credentials['USER_ID'])
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    
        """

    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")

admin_only = lambda message: message.from_user.id == USER_ID

@dp.message_handler(admin_only)
async def echo(message: types.Message):
    await message.answer(message.text)
   

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)