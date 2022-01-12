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

def analyse_crypto_by_message(param, time_span_days=365, moving_average_days=30, bollinger_bands_days=30):
    output = execute_shell_command(f'python3 Crypto/main.py {param} {time_span_days} {moving_average_days} {bollinger_bands_days}')
    try:
        send_file('export.jpg',EMAIL_ADDRESS, EMAIL_PASSWORD,'Crypto Report')
    except:
        output += '\ncould not send file for some reason'
    return output

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
            send_file(text_array[1].strip(), EMAIL_ADDRESS, EMAIL_PASSWORD, text_array[1].strip())
            await message.answer('Emailed the file to you kind sir.')
        elif text_array[0] == 'analyse':
            output = analyse_crypto_by_message(text_array[1], text_array[2], text_array[3], text_array[4])
            if output:
                output += "\nSent you a detailed report sir."
                await message.answer(output)
        else:
            output = execute_shell_command(message.text)
            if output:
                await message.answer(output)
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