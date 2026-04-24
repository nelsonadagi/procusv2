# Architecture

## High-level shape

The platform follows an API-first architecture:

- Vue 3 SPA for presentation
- Django + DRF for API and domain logic
- PostgreSQL for relational persistence
- Redis for broker/cache/realtime support
- Celery for background work
- Django Channels for websocket features such as chat and notifications

## Core layers

### Client layer

- Vue 3
- Vite
- Vue Router
- Pinia
- Axios
- Custom CSS design system

### Application layer

- Django project config in `backend/config/`
- Domain apps grouped by business capability
- DRF viewsets, serializers, models, and permissions
- Channels-based ASGI entrypoint for websocket routes

### Data and async layer

- PostgreSQL / PostGIS for primary relational storage and geospatial features
- Redis for Celery broker/result backend and channel layers
- Celery worker and Celery beat for queued and scheduled processing

## Architectural principles reflected in docs

- Strong domain separation by Django app
- Versioned API namespaces
- Role-gated access control
- Thin transport layer with domain logic in app code
- Environment-driven configuration
- Dockerized local and deployment workflows

## Notable implementation themes

- Geospatial search for vendors, products, and projects
- Role-based dashboards and workflows
- Financial operations with escrow and milestone release concepts
- Realtime chat and notification channels
- Extensible taxonomy/master-data layer

## Key runtime files

- `backend/config/settings.py`
- `backend/config/urls.py`
- `backend/config/asgi.py`
- `docker-compose.yml`

## Context sources

- `docs/SDD.md`
- `docs/DEPLOYMENT_GUIDE.md`
- `README.md`
