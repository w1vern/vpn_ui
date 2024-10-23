import json
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
import pika

from app.site.token import TgCode

load_dotenv()

SECRET = os.getenv('SECRET')

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
queue_name = 'message_queue'
channel.queue_declare(queue=queue_name)

def send_message(data):
    message = json.dumps(TgCode.to_dict())
    channel.basic_publish(exchange='', routing_key=queue_name, body=message)

app = FastAPI()
