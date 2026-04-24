# Deployment Readiness Prompt

```md
Review this repository for deployment readiness.

Read first:
- `context/02-architecture.md`
- `context/08-security-compliance-and-risk.md`
- `context/09-deployment-and-operations.md`

Then inspect:
- `docker-compose.yml`
- `.env.example`
- backend settings
- ASGI/WSGI configuration
- database and Redis assumptions
- Celery and websocket dependencies

Provide:
- required services
- required environment variables
- production risks
- local-vs-container drift
- security concerns
- a prioritized readiness checklist
```
