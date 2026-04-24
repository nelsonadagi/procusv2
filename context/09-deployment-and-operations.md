# Deployment And Operations

## Local and deployment model

The repository is designed as a Dockerized monorepo with separate runtime services for frontend, backend, database, broker, and async workers.

## Expected services

- `frontend`
- `backend`
- `postgres`
- `redis`
- `celery-worker`
- `celery-beat`

## Environment expectations

Key environment variables include:

- `DATABASE_URL`
- `REDIS_URL`
- `CELERY_BROKER_URL`
- `CELERY_RESULT_BACKEND`
- `DJANGO_SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- payment/integration secrets

## Operational concerns

- API and websocket support must both be considered
- geospatial features imply PostGIS, not plain PostgreSQL only
- media and static handling need explicit deployment strategy
- Celery and Redis are first-class runtime dependencies
- production should externalize secrets and persistent storage

## Recommended operational checks

- confirm database engine matches required GIS features
- confirm Redis is reachable for both Celery and Channels
- confirm `.env` values work both locally and in containers
- confirm tests are run in an environment that can actually resolve service hosts

## Context sources

- `docs/DEPLOYMENT_GUIDE.md`
- `docs/SYSTEM_REQUIREMENTS.md`
- `docs/MONOREPO_BOOTSTRAP.md`
- `.env.example`
- `docker-compose.yml`
