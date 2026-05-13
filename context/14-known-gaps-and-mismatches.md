# Known Gaps And Mismatches

## Purpose

This file records current drift that should be assumed real until fixed.

## Frontend and backend route mismatches

### Projects namespace mismatch

Observed frontend usage:

- `OwnerDashboard.vue` uses `/v2/projects/`

But backend routing places projects in:

- `/api/projects/`
- `/api/v4/projects/`

Impact:

- owner dashboard project fetches are likely broken or stale

### Logistics namespace mismatch

Observed frontend usage:

- `/logistics/zones/`
- `/logistics/zones/calculate/`

But backend routing exposes:

- `/api/logistics/pricing-zones/`

Impact:

- logistics calculator and related UI may fail unless adapted

### Platform settings delete mismatch

Observed frontend usage:

- `/config/countries/{id}/`

But backend routing exposes:

- `/api/platform_settings/countries/{id}/`

Impact:

- country deletion from admin settings is likely broken

## Documentation and implementation mismatches

### Auth token style

Some docs describe JWT-style auth, while the implemented frontend/backend flow currently uses DRF token authentication patterns.

Impact:

- new work should not assume JWT unless the auth layer is intentionally migrated

### API examples in phase docs

Some API docs are conceptual or phase-scoped and do not exactly match current live route names.

Impact:

- use docs for intent, not as route truth, unless verified against code

### Vendor workflow documentation drift

Older vendor docs previously referred to outdated profile routes and incomplete inventory behavior.

Current corrected workflow:

- vendor onboarding uses `/api/vendors/` with frontend path `/vendors/register`
- vendor inventory uses `/api/v1/products/me/`
- vendor inventory history uses `/api/v1/products/{id}/inventory-history/`
- vendor inventory adjustment uses `/api/v1/products/{id}/adjust-inventory/`
- vendor CSV import uses `/api/v1/products/import_products/`
- vendor CSV template download uses `/api/v1/products/download_template/`

Impact:

- use the vendor docs updated in this pass, not older assumptions copied from prior phases

### Admin documentation drift

Some documents describe a more complete admin control plane than the current product actually exposes.

Examples:

- dispute arbitration is implemented in backend APIs but not surfaced in admin dashboard UI
- admin verifications currently cover contractors, not the full vendor and investor review scope described in docs
- the dedicated user-management panel does not match the more complete settings-based admin user tools
- overview metrics mix real data and placeholder values

Impact:

- use `docs/ADMIN_FUNCTIONALITY_STATUS.md` as the current admin truth document

## Environment mismatches

### Test execution environment

Local test execution may fail because the test suite expects Docker-style service resolution for PostgreSQL hostnames.

Impact:

- test failure may indicate environment setup problems before it indicates business logic failure

### Dependency version drift

Declared dependency versions and active local runtime versions may not match.

Impact:

- subtle behavior differences across Django or plugin versions are possible

## Property module gaps

### 1. No dedicated `property:delete` permission
The `destroy` action in `PropertyViewSet` maps to `property:update_property`. This means anyone who can edit a property can also delete it. If you ever want managers to edit but **not** delete listings, a separate `property:delete` permission must be added to `backend/rbac/permission_catalog.py` and the view permission map.

### 2. No inquiry/appointment-specific permissions
`PropertyInquiryViewSet` and `PropertyAppointmentViewSet` use `IsPropertyOperator` (owner + manager + admin). There is no fine-grained permission like `property:manage_inquiries` or `property:manage_appointments`. A front-desk assistant cannot be granted booking-only access without full property edit rights.

### 3. Government role has zero property access
`GOVERNMENT`, `GOVERNMENT_OWNER`, and `GOVERNMENT_AUDITOR` have no `property:*` permissions. If the platform needs land registry verification, building permit audits, or zoning compliance checks, these roles must be granted `property:view` (and possibly `property:update_property` for auditors).

### 4. Missing real estate professional roles
The `asset_type` includes `RENOVATION`, `COMMERCIAL`, `MIXED_USE`, etc., but there is no dedicated role for:
- **Real Estate Agent / Broker** — distinct from Property Manager (agents sell/lease; managers operate)
- **Surveyor / Valuer** — updates `price_estimate`, `ownership_profile.verification_status`, or `specification.condition_rating`
- **Architect / Developer** — edits `development_metadata`

Currently these workflows are handled by `PROJECT_OWNER` or `PROPERTY_MANAGER`, which may not reflect real-world separation of duties.

### 5. Organization-level property access is unused
The `User` model has an `organization` FK, but `IsPropertyOperator` only checks `owner == user` or `manager == user`. It never checks organization membership. Multi-employee real estate firms cannot share a portfolio without individually assigning each user as owner or manager.

## Data and workflow gaps to treat carefully

- advanced compliance workflows need end-to-end validation
- advanced banking/reporting/AI features need operational verification
- chat and notification custom actions should be confirmed in code before frontend expansion
- vendor inventory still does not implement quote-stage reservations or multi-warehouse stock
- versioned and direct endpoints should not be mixed casually in new code

## Working rule

If a doc, frontend file, and backend router disagree, trust the backend router first, then the serializer/view behavior, then the docs.
