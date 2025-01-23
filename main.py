import asyncio
import logging
import sys
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

import pika

load_dotenv()
TOKEN = os.getenv('TOKEN_dev')
RABBIT_HOST = os.getenv('RABBIT_HOST')
RABBIT_USER, RABBIT_PASS = os.getenv('USER'),os.getenv('PASSWORD')

dp = Dispatcher()

@dp.message()
async def start_handler(message: types.Message):
    credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
                                            host=RABBIT_HOST,
                                            port=5672,
                                            credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=message.text)
    connection.close()

    await message.answer("Тебя записали в книжечку!")

async def main():
    bot = Bot(TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.getLogger('pika').setLevel(logging.WARNING)
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())