import asyncio
import logging
import sys
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types
from _rb import rabbitmq_listener, rabbitmq_sender

load_dotenv()
TOKEN = os.getenv('TOKEN_dev')


dp = Dispatcher()

@dp.message()
async def start_handler(message: types.Message):

    await rabbitmq_sender(message.text, message.chat.id)
    await message.answer("Тебя записали в книжечку!")

async def main():
    
    bot = Bot(TOKEN)
    asyncio.create_task(rabbitmq_listener(bot))

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.getLogger('pika').setLevel(logging.WARNING)
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    asyncio.run(main())