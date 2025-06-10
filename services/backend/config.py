




from shared.config import env_config

SECRET = env_config.backend.secret

class Config:
	tg_code_lifetime = 60 * 2
	access_token_lifetime = 60 * 10
	refresh_token_lifetime = 3600 * 24 * 30
	tg_code_gap = 20
	login_gap = 20
	ip_buffer = 10
	ip_buffer_lifetime = 60*60*24
	algorithm = "HS256"
