import os
from dotenv import load_dotenv
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from tortoise import fields
from tortoise.models import Model
from pydantic import BaseModel

import logging
logging.basicConfig(level=logging.DEBUG)

load_dotenv()

db_url = os.getenv("db_tmp_url")
print(f"url of db: {db_url}")

app = FastAPI()


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50)
    email = fields.CharField(max_length=100)


class test(BaseModel):
    name: str
    email: str


register_tortoise(
    app,
    db_url=db_url,  # Для PostgreSQL
    modules={"models": ["__main__"]},  # Где находятся модели
    generate_schemas=True,  # Автоматическая генерация схем
    add_exception_handlers=True,  # Добавляет обработчики ошибок для базы данных
)

# Пример асинхронного эндпоинта


@app.post("/")
async def create_user(tmp: test):
    user = await User.create(username=tmp.name, email=tmp.email)
    return {"id": user.id, "username": user.username, "email": user.email}


@app.get("/")
async def home():
    return {"message" : "Hello world"}

def main():
    pass

if __name__ == '__main__':
    main()