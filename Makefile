.PHONY: back

gen_migration:
	alembic -c services/alembic/alembic.ini revision --autogenerate -m "first migration"

migration:
	alembic -c services/alembic/alembic.ini upgrade head

down_migration:
	alembic -c services/alembic/alembic.ini downgrade -1

add_frontend:
	git submodule add --name frontend https://github.com/ImmortalAI/vpn_front_vue services/frontend

install_submodules:
	git submodule update --init --recursive

update_submodules:
	git submodule update --remote --recursive
