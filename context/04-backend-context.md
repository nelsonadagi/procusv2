# Backend Context

## Backend stack

- Python 3.10+
- Django
- Django REST Framework
- django-filter
- django-cors-headers
- Django Channels
- Celery
- PostgreSQL / PostGIS

## Backend structure

The backend is organized as a multi-app Django codebase where each domain owns:

- `models.py`
- `serializers.py`
- `views.py`
- `urls.py`
- `admin.py`
- `tests.py`
- `migrations/`

## Important backend app groups

### Core platform

- `accounts`: auth, registration, profiles, addresses
- `rbac`: roles, permissions, audit concepts
- `platform_settings`: countries, currencies, platform config
- `taxonomy`: shared master data and category trees

### Commerce and fulfillment

- `vendors`
- `catalog`
- `orders`
- `payments`
- `reviews`
- `logistics`

### Execution and financial control

- `contractors`
- `contracts`
- `bids`
- `milestones`
- `escrow`
- `finance`
- `disputes`
- `scoring`

### Projects and advanced domains

- `projects`
- `property`
- `investments`
- `regulation`
- `enterprise`
- `government`
- `compliance`
- `risk`
- `banking`
- `reporting`
- `ai_engine`
- `liquidity`
- `integrations`

### Realtime and operational support

- `notifications`
- `security`
- `chat`

## API style

The docs and codebase reflect a mixed API style:

- versioned endpoints such as `/api/v1/` to `/api/v6/`
- direct app endpoints such as `/api/accounts/`, `/api/vendors/`, `/api/contracts/`
- DRF routers for most domain resources
- custom actions for workflow transitions like approve, award, respond, and track

## Backend design expectations from docs

- domain separation
- role-based authorization
- transaction-aware financial flows
- reusable serializer validation
- environment-based settings
- support for async and realtime workloads

## Admin backend reality

Several admin-relevant backend capabilities exist even where frontend admin surfaces are incomplete.

Examples:

- audit log read API in `rbac`
- security violation monitoring in `security`
- system configuration, country, role, and admin-user APIs in `platform_settings`
- dispute resolution endpoint in `disputes`
- regulatory report read APIs in `reporting`

This means some admin work is blocked by frontend integration rather than backend absence.

## Use this file when

- planning backend feature work
- tracing which app should own a new capability
- deciding whether an endpoint belongs in a versioned router or an app namespace

## Context sources

- `docs/SDD.md`
- `docs/API_SPEC.md`
- `docs/PROJECTS_API_SPEC.md`
- `docs/BIDDING_API_SPEC.md`
- `docs/ADMIN_FUNCTIONALITY_STATUS.md`
- `docs/VENDOR_DASHBOARD_API_FIXES.md`
