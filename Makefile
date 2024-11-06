
front:
	npm run dev --prefix ./front

bot:
	python -m bot

back:
	uvicorn back.main:app --reload

proxy:
	node ./proxy/main.js

redis:
	docker run --name redis -p 6379:6379 -d redis

rabbitmq:
	docker run -d --hostname my-rabbit --name rabbit -p 5672:5672 rabbitmq:3
