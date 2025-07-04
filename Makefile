.PHONY: back

back:
	uvicorn services.backend.main:app --reload

back_install:
	uv sync

bot:
	python -m services.bot

redis:
	docker start Redis

postgres:
	docker start PostgreSQL
	
gen_migration:
	alembic -c services/alembic/alembic.ini revision --autogenerate -m "first migration"

migration:
	alembic -c services/alembic/alembic.ini upgrade head

down_migration:
	alembic -c services/alembic/alembic.ini downgrade -1

fill_db:
	python -m services.fill_db

create_postgres:
	docker run --name PostgreSQL -p 5432:5432 -e POSTGRES_PASSWORD=1234 -d postgres

create_redis:
	docker run --name Redis -p 6379:6379 -d redis

proxy_install:
	npm install --prefix ./proxy

setup:
	create_postgres

create_rabbit:
	docker run -d --hostname my-rabbit --name RabbitMQ -p 5672:5672 rabbitmq:3

rabbit:
	docker start RabbitMQ

docker:
	docker compose up -d

docker_down:
	docker compose down --volumes

docker_build:
	docker compose up -d --build

add_frontend:
	git submodule add --name frontend https://github.com/ImmortalAI/vpn_front_vue services/frontend

install_submodules:
	git submodule update --init --recursive

update_submodules:
	git submodule update --remote --recursive
