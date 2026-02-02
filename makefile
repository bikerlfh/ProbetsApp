# these will speed up builds, for docker-compose >= 1.25
export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

.PHONY: help

.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

black: ## black
	black . --line-length=79 --exclude migrations\

dev-check: ## dev-check
	pre-commit run --all-files

build: ## build
	docker compose build

up: ## up
	docker compose up

up-d: ## up d
	docker compose up -d

down: ## down
	docker compose down --remove-orphans

down-d: ## down
	docker compose down --remove-orphans --rmi local

run:  ## run
	docker compose run --rm --service-ports app ${ARGS}

startapp:  ## makemigrations
	docker compose run --rm --entrypoint=python app manage.py startapp ${app_name}

makemigrations:  ## makemigrations
	docker compose run --rm --entrypoint=python app probetspp/manage.py makemigrations

reset-migrations: ## reset-migrations - delete all migration files and recreate them
	@echo "🗑️  Deleting all migration files..."
	@find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	@find . -path "*/migrations/*.pyc" -delete
	@echo "✨ Recreating migrations..."
	docker compose run --rm --entrypoint=python app probetspp/manage.py makemigrations

migrate: ## migrate
	docker compose run --rm --entrypoint=python app probetspp/manage.py migrate

load-fixtures: ## loaddata
	docker compose run --rm --entrypoint=python worker manage.py loaddata fixtures/*.json

dumpdata: ## dumpdata - create fixture from specific table (usage: make dumpdata table=app.ModelName)
	docker compose run --rm --entrypoint=python worker manage.py dumpdata ${table} --indent=2 --output=fixtures/$(shell echo ${table} | sed 's/\./_/g').json

clear-cache: ## loaddata
	docker compose run --rm --entrypoint=python worker manage.py invalidate all

create-superuser: ## loaddata
	docker compose run --rm --entrypoint=python app probetspp/manage.py createsuperuser

create-predictions: ## create-predictions
	docker compose run --rm --entrypoint=python app probetspp/manage.py create_predictions

reset-db: ## reset_db
	docker compose run --rm --entrypoint=python app manage.py reset_db -c

shell: ## shell
	docker compose run --rm --entrypoint=python app manage.py shell_plus

run-tests:  # run-tests
	docker compose run --rm --entrypoint=pytest app tests/ -s $(args)

celery: ## run celery
	docker compose run --rm --entrypoint=celery worker -A apps.messaging.app worker -l info

exec-celery: ## exec celery
	docker compose run --rm --entrypoint=celery worker -A apps.messaging.app beat

beat: ## run celery beat
	docker compose run --rm --entrypoint=celery worker -A apps.messaging.app beat

docker-celery: ## docker celery
	docker exec -it ${CONTAINER_ID} celery -A apps.messaging.app worker -l info

docker-attach: ## docker attach
	docker attach --detach-keys ctrl-d ${CONTAINER_ID}


ssh-add: ## ssh-add
	sudo ssh-add ~/.ssh/id_ed25519

init-db: ## init-db
	make reset-db && make migrate && make load-fixtures