build-dev:
	docker-compose --env-file .env.dev -f docker-compose-dev.yaml build

run-dev:
	docker-compose --env-file .env.dev -f docker-compose-dev.yaml up --remove-orphans

down-dev:
	docker-compose --env-file .env.dev -f docker-compose-dev.yaml down --remove-orphans

shell-dev:
	docker-compose --env-file .env.dev -f docker-compose-dev.yaml run app-dev bash

build-test:
	docker-compose --env-file .env.test -f docker-compose-test.yaml build

run-test:
	docker-compose --env-file .env.test -f docker-compose-test.yaml up --remove-orphans

down-test:
	docker-compose --env-file .env.test -f docker-compose-test.yaml down --remove-orphans

shell-test:
	docker-compose --env-file .env.test -f docker-compose-test.yaml run app-test bash