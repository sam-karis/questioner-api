# Define filename references
DEV_FOLDER := docker
DEV_COMPOSE_FILE := docker/docker-compose.yml

build:
	@ echo "Building Questioner API..."
	@ docker-compose -f ${DEV_COMPOSE_FILE} up -d

down:
	@ echo "Questioner API going down..."
	@ docker-compose -f ${DEV_COMPOSE_FILE} down

start:
	@ echo 'Starting  $(service) service...'
	@ docker-compose -f ${DEV_COMPOSE_FILE} start $(service)

stop:
	@ echo 'Stoping  $(service) service...'
	@ docker-compose -f ${DEV_COMPOSE_FILE} stop $(service)

status:
	@ echo "Checking status..."
	@ docker-compose -f ${DEV_COMPOSE_FILE} ps

migrate:
	@echo "Running migrations..."
	@ docker-compose -f ${DEV_COMPOSE_FILE} exec django python  manage.py migrate

migrations:
	@echo "Running migrations..."
	@ docker-compose -f ${DEV_COMPOSE_FILE} exec django python  manage.py makemigrations

run-app:
	@ echo 'Running Questioner API on port 8000...'
	@ docker-compose -f ${DEV_COMPOSE_FILE} exec django python  manage.py runserver 0.0.0.0:8000

psql:
	@ echo 'Entering psql interface...'
	@ docker-compose -f ${DEV_COMPOSE_FILE} exec database psql --u postgres