.PHONY: front back proxy 


front:
	npm run dev --prefix ./front

front_install:
	npm install --prefix ./front

back:
	uvicorn back.main:app --reload

back_install:
	poetry install

proxy:
	node ./proxy/main.js

redis:
	docker start Redis

postgres:
	docker start PostgreSQL
	
gen_migration:
	alembic revision --autogenerete -m "first migration"

migration:
	alembic upgrade head

down_migration:
	alembic downgrade -1

fill_data:
	python -m static.db_base_data

create_postgres:
	docker run --name PostgreSQL -p 5432:5432 -e POSTGRES_PASSWORD=1234 -d postgres

create_redis:
	docker run --name Redis -p 6379:6379 -d redis

main_install:
	poetry install

proxy_intall:
	npm install --prefix ./proxy

setup:
	create_postgres

cteate_rabbit:
	docker run -d --hostname my-rabbit --name RabbitMQ -p 5672:5672 rabbitmq:3

rabbit:
	docker start RabbitMQ
