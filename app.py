import logging
import os
import subprocess
import time

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.chat import Chat

from mailer import send_file

if (str(os.uname()).split('nodename=')[1].split()[0][1:-2]) == 'rpi':
        os.chdir('/home/pi/Desktop/TelegramBot')

def execute_shell_command(command):
    command_array = command.split()
    if command_array[0] == 'cd':
        try:
            os.chdir(command_array[1])
        except OSError:
            return ("No such directory: " + command_array[1])
        return 'Changed directory to ' + command_array[1]
    else:
        try:
            return subprocess.getoutput(command)
        except Exception as e:
            return e

import json
with open('config.json') as f:
    credentials = json.load(f)

API_TOKEN = credentials['API_TOKEN']

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
EMAIL_ADDRESS = credentials['EMAIL_ADDRESS']
EMAIL_PASSWORD = credentials['EMAIL_PASSWORD']

CHAT_ID = int(credentials['CHAT_ID'])
USER_ID = int(credentials['USER_ID'])
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

admin_only = lambda message: message.from_user.id == USER_ID

@dp.message_handler(admin_only)
async def echo(message: types.Message):
    try:
        text_array = message.text.split()
        if text_array[0] == 'sendfile':
            send_file(text_array[1].strip(), EMAIL_ADDRESS, EMAIL_PASSWORD)
            await message.answer('Emailed the file to you kind sir.')
        else:
            await message.answer(execute_shell_command(message.text))
    except Exception as e:
            await message.answer(e)

if __name__ == '__main__':
        time.sleep(10)
        executor.start_polling(dp, skip_updates=True)

# @dp.message_handler(commands=['start', 'help'])
# async def send_welcome(message: types.Message):
#     """
#     This handler will be called when user sends `/start` or `/help` command
    
#         """

#     await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")