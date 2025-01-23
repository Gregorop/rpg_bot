import os, json
from aio_pika import connect, Message
from dotenv import load_dotenv
load_dotenv()

RABBIT_HOST = os.getenv('RABBIT_HOST')
RABBIT_USER, RABBIT_PASS = os.getenv('USER'),os.getenv('PASSWORD')
RABBITMQ_URL = f'amqp://{RABBIT_USER}:{RABBIT_PASS}@{RABBIT_HOST}/'

async def rabbitmq_sender(message,chat_id):
    connection = await connect(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(name='messages',durable=True) 

        message = Message(body=message.encode(),
                          delivery_mode=2,
                          headers={'chat_id':chat_id})
        
        await channel.default_exchange.publish(
            message,
            routing_key=queue.name,
        )


async def rabbitmq_listener(bot):
    connection = await connect(RABBITMQ_URL,login=RABBIT_USER,password=RABBIT_PASS)
    channel = await connection.channel()
    queue = await channel.declare_queue(name='messages',durable=True) 

    async for message in queue:
        async with message.process():
            headers = message.headers
            chat_id = headers.get('chat_id')
            text = message.body.decode()

            await bot.send_message(chat_id, f'Сам ты {text}')