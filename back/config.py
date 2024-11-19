

import os

from dotenv import load_dotenv

load_dotenv()

SECRET = os.getenv("SECRET")

class Config:
	tg_code_lifetime = 60 * 2
	access_token_lifetime = 60 * 10
	refresh_token_lifetime = 3600 * 24 * 30
	algorithm = "HS256"
