.PHONY: up down logs test build
up:
	docker compose up --build -d
down:
	docker compose down
logs:
	docker compose logs --tail=100 website
test:
	python3 tests/smoke_test.py http://127.0.0.1:$${WEB_PORT:-8082}/
build:
	docker build -t releaseforge:local .
