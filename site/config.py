

import json
import os
from dotenv import load_dotenv


load_dotenv()

SECRET = os.getenv('SECRET')

class Config:
    tg_code_lifetime = 120
    access_token_lifetime = 600
    refresh_token_lifetime = 2592000
    algorithm = 'HS256'