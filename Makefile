build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

push:
	docker-compose push

pull:
	docker-compose pull

sh:
	docker-compose exec app /bin/bash