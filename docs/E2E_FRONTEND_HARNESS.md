# API-Only E2E Harness

`backend/scripts/e2e_frontend_runner.py` is a Python HTTP client that exercises the backend the way the frontend would.

It is API-based only: no browser automation, no Playwright, no Selenium, and no Cypress.

It is intended for broad end-to-end coverage across the mounted modules, not just unit or app-local API tests.

## What It Covers

- Logs in as seeded actors: `admin`, `owner_jane`, `vendor_mall`, `contractor_expert`, `investor_wealth`, and related role users.
- Registers fresh accounts and exercises admin-mediated onboarding for key actor types:
  - self-service project owner registration and profile bootstrap
  - vendor registration with admin role approval plus vendor application approval
  - contractor registration with admin role approval plus contractor application approval
  - investor registration with admin role approval plus KYC approval
  - courier registration with admin role approval and courier profile creation
  - government registration with admin role approval and first tender publication
- Runs real frontend-style workflows for the highest-value modules:
  - platform bootstrap
  - account profile and address updates
  - admin control-plane reads and managed-user creation
  - vendor profile access and product inventory adjustment
  - catalog search and active-country scoping checks
  - project creation, requirement posting, investor commitment
  - project search, `owner=me`, and active-country scoping checks
  - property listing, availability window, inquiry, and appointment
  - property search and active-country scoping checks
  - notification preference updates
- Sweeps the rest of the mounted API modules with authenticated `GET` requests so versioned modules under `/api/v2` to `/api/v6` are still covered.

## Default Assumptions

- Backend is reachable at `http://localhost:8007`
- Seeded credentials are present from the repo bootstrap/reset flow
- Active country header defaults to `KE`

## Run

Full workflow mode:

```bash
python3 backend/scripts/e2e_frontend_runner.py
```

Smoke mode:

```bash
python3 backend/scripts/e2e_frontend_runner.py --mode smoke
```

Target only selected modules:

```bash
python3 backend/scripts/e2e_frontend_runner.py --module projects --module property
```

Fail immediately on the first broken step:

```bash
python3 backend/scripts/e2e_frontend_runner.py --fail-fast
```

Point it at a different backend:

```bash
python3 backend/scripts/e2e_frontend_runner.py --base-url http://localhost:8000
```

## Notes

- The harness intentionally mixes true write flows with read sweeps. That gives meaningful workflow coverage without requiring handcrafted fixture creation for every advanced module.
- The harness talks directly to the backend over HTTP using `requests.Session`; it does not drive the Vue app or a browser.
- Admin approval coverage is actor-specific. Vendor, contractor, and KYC use explicit backend approval actions; courier and government currently rely on admin role approval because this backend does not yet expose dedicated approval endpoints for those actor profiles.
- If a seeded user password changes, update the actor map near the top of the script.
- If a new module is mounted in `backend/config/urls.py` or the versioned routers, add it to the `module_sweep` endpoint list or create a dedicated workflow step for it.
