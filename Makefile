build-dev:
	docker-compose --env-file .env.dev -f docker-compose-dev.yaml build

run-dev:
	docker-compose --env-file .env.dev -f docker-compose-dev.yaml up --remove-orphans