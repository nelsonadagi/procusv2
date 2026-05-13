# Frontend Context

## Frontend stack

- Vue 3
- Vite
- Vue Router
- Pinia
- Axios
- Custom CSS tokens and component styles
- Light i18n setup for English and Swahili

## Frontend structure

Main areas in `frontend/src/`:

- `views/`: page-level route views
- `components/`: reusable UI and domain components
- `components/ui/`: low-level UI primitives
- `stores/`: Pinia state stores
- `services/`: API client setup
- `styles/`: design tokens, layouts, components, base styling
- `router/`: SPA routes

## Main route families

- public marketplace browsing
- authentication
- contracts and tenders
- projects
- properties
- buyer dashboard
- vendor dashboard
- contractor dashboard
- courier dashboard
- investor dashboard
- owner dashboard
- admin dashboard
- regulatory reports
- secondary market

## Frontend design intent

The documentation and code suggest:

- a shared-account application shell with specialized workspaces
- a custom marketplace visual identity
- responsive layouts
- dashboard-oriented workspaces for each actor
- SPA-first navigation with API-backed data flows

## Key frontend responsibilities

- route orchestration
- workspace activation and dashboard rendering
- form submission for marketplace and workflow actions
- data fetching from versioned and app-level APIs
- configuration-driven localization with country-derived currency display and record-level source currency conversion for property, product, and procurement prices

## Prompt and copy direction

Frontend prompts should reinforce the role policy clearly:

- one account first
- specialized workspace activation second
- admin approval where required third

Preferred copy patterns:

- "Activate vendor workspace"
- "Continue contractor onboarding"
- "Pending admin review"
- "Approved and ready"

Copy to avoid:

- "Pick your permanent role"
- "Change role to unlock access" when profile approval is the real gate
- approval-blind success messages that imply specialization is instant

## Frontend caution areas

When extending the UI, always confirm:

- the route namespace matches the backend namespace
- the payload shape matches the serializer expectation
- the dashboard copy distinguishes between:
  - base access
  - missing specialized profile
  - pending admin approval
  - approved specialized role activation

## Admin dashboard reality

The admin shell exists and is visually mature, but the modules are not equally complete.

High-confidence admin frontend surfaces:

- `SystemConfigSection.vue`
- `SecurityMonitorSection.vue`
- `RegulatoryReports.vue`
- audit log feed inside `OverviewSection.vue`

Partial or drift-prone admin frontend surfaces:

- `VerificationsSection.vue`
- `UserManagementSection.vue`
- `OverviewSection.vue` headline stats

Missing admin UI areas relative to docs:

- dispute arbitration workspace
- vendor verification workspace
- investor KYC review workspace

## Context sources

- `docs/USER_GUIDE.md`
- `docs/USER_MANUAL.md`
- `docs/BUYER_DASHBOARD_NAVIGATION.md`
- `docs/UX_IMPROVEMENTS.md`
- `docs/ROLE_AND_ONBOARDING_POLICY.md`
- `docs/ADMIN_FUNCTIONALITY_STATUS.md`
- `frontend/FRONTEND_STYLE_GUIDE.md`
