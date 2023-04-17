
up:
	docker-compose -f production.yml up --build -d

build:
	docker-compose -f production.yml build

makemigrations:
	docker-compose -f production.yml run --rm django python manage.py makemigrations

migrate:
	docker-compose -f production.yml run --rm django python manage.py migrate

down:
	docker-compose -f production.yml down

logs:
	docker-compose -f production.yml logs -f

rebuild: down up logs

git_pull:
	git pull

git_rebuild: down git_pull up logs


.DEFAULT_GOAL := git_rebuild