# Context Folder

This folder is a curated working context built from the repository documentation in `docs/`.

It is designed to give you a fast, practical view of the platform without having to read every source document end-to-end.

## What is in here

- `01-platform-overview.md`: product scope, user roles, and system purpose
- `02-architecture.md`: technical architecture and runtime shape
- `03-phases-and-domains.md`: the six delivery phases and the domain modules they introduce
- `04-backend-context.md`: backend structure, app boundaries, and API patterns
- `05-frontend-context.md`: frontend structure, routes, dashboards, and UX shape
- `06-data-and-taxonomy.md`: data model themes, taxonomy system, and major entities
- `07-workflows.md`: main user and business workflows across the platform
- `08-security-compliance-and-risk.md`: security, RBAC, compliance, and risk features
- `09-deployment-and-operations.md`: environment, Docker, async services, and deployment assumptions
- `10-source-map.md`: source docs used to build this folder
- `11-implementation-status.md`: what looks implemented, partial, or drift-prone
- `12-api-truth-map.md`: practical route truth for backend and frontend alignment
- `13-role-permission-matrix.md`: role and permission reference from code and docs
- `14-known-gaps-and-mismatches.md`: current integration and documentation drift
- `15-build-order.md`: recommended execution order for delivering or stabilizing the platform
- `16-design-principles.md`: visual direction, typography, color, motion, and design constraints
- `17-ui-patterns.md`: canonical UI patterns for major interface structures
- `18-brand-application-rules.md`: how the Paanguzo brand should show up in product UI
- `19-page-priorities.md`: recommended visual refinement order across the app

Important supporting docs in `docs/`:

- `docs/ADMIN_FUNCTIONALITY_STATUS.md`: current admin capability status and gaps
- `docs/ROLE_AND_ONBOARDING_POLICY.md`: current role, approval, and multi-role onboarding policy
- `docs/PROPERTY_WORKFLOW.md`: target operating model for standalone property plus project/finance integration
- `docs/VENDOR_INVENTORY_SYSTEM.md`: current supplier inventory behavior, stock movements, and order reconciliation

## How to use this folder

1. Read `01-platform-overview.md` first.
2. Use `02-architecture.md` and `04-backend-context.md` when planning implementation work.
3. Use `05-frontend-context.md` before making UI or routing changes.
4. Use `07-workflows.md` before touching business logic.
5. Use `12-api-truth-map.md` before wiring any endpoint.
6. Use `13-role-permission-matrix.md` before changing access control.
7. Use `14-known-gaps-and-mismatches.md` before fixing integration issues.
8. Use `15-build-order.md` when sequencing larger implementation work.
9. Use `16-design-principles.md`, `17-ui-patterns.md`, and `18-brand-application-rules.md` before major UI changes.
10. Use `19-page-priorities.md` when planning visual polish work.
11. Use `10-source-map.md` when you need the original document behind a summary.
12. Use `docs/ADMIN_FUNCTIONALITY_STATUS.md` when planning admin dashboard work.
13. Use `docs/ROLE_AND_ONBOARDING_POLICY.md` when planning role, onboarding, approval, or access-control changes.
14. Use `docs/PROPERTY_WORKFLOW.md` when planning property, inquiry, appointment, or property-project integration work.
15. Use `docs/VENDOR_INVENTORY_SYSTEM.md` when refining supplier inventory, stock adjustments, or order-linked stock reconciliation.

## Important note

These files are condensed context, not a legal or contractual replacement for the source documentation. If something here conflicts with code, verify against the live implementation and the original docs in `docs/`.
