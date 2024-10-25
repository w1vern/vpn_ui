

import json
import os
from dotenv import load_dotenv


load_dotenv()

SECRET = os.getenv('SECRET')

with open ('app/site/config.json', encoding='utf-8') as file:
    config = json.load(file)