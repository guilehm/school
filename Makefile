DOCKER_COMPOSE=docker-compose
BACKEND_SERVICE=school

run:
	-$(DOCKER_COMPOSE) up

stop:
	@echo "Stopping containers"
	-$(DOCKER_COMPOSE) stop

down:
	@echo "Removing containers"
	-$(DOCKER_COMPOSE) down

remove:
	@echo "Removing containers and volumes"
	-$(DOCKER_COMPOSE) down -v

build:
	@echo "Building the app"
	-$(DOCKER_COMPOSE) build

lint:
	-$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) bash -c "isort . && flake8"

test:
	-$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) pytest -vv

migrations:
	-$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) python manage.py makemigrations

migrate:
	-$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) python manage.py migrate

showmigrations:
	-$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) python manage.py showmigrations

superuser:
	-$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) python manage.py createsuperuser

mm: migrations migrate
