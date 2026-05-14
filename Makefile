COMPOSE_DEV = docker compose
COMPOSE_PROD = docker compose --env-file .env.production -f docker-compose.yml -f docker-compose.prod.yml

.PHONY: dev prod prod-config stop logs backend-shell migrate seed

dev:
	$(COMPOSE_DEV) up --build

prod:
	test -f .env.production
	$(COMPOSE_PROD) up -d --build

prod-config:
	test -f .env.production
	$(COMPOSE_PROD) config

stop:
	docker compose down

logs:
	docker compose logs -f --tail=150

backend-shell:
	docker compose exec backend python manage.py shell

migrate:
	docker compose exec backend python manage.py migrate --noinput --fake-initial

seed:
	docker compose exec backend python manage.py seed_roles
