from faststream import FastStream
from faststream.rabbit import RabbitBroker
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
RABBITMQ_CONNECT = os.getenv("RABBITMQ_CONNECT")
broker = RabbitBroker(RABBITMQ_CONNECT)
app = FastStream(broker)

async def main():
    await app.run()

if __name__ == "__main__":
    asyncio.run(main())
