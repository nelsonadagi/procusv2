# Admin Functionality Status

## Purpose

This document records the current admin functionality that is actually available in the application, based on code review of both frontend and backend.

It should be treated as the working truth until the remaining admin modules are completed.

---

## Summary

The admin area is partially operational.

What is currently dependable:

- platform identity and regional settings
- currencies
- countries
- taxonomy categories
- Django group and role management
- admin user activation and role reassignment
- security violation monitoring
- audit log viewing
- property registry visibility
- dispute arbitration queue and refund/release actions
- vendor verification queue
- investor KYC review queue
- regulatory report viewing surface

What is currently partial or missing:
- deep document review workflow
- dedicated operator creation workflow in the admin panel

---

## Admin Dashboard Areas

### 1. Overview

Current state: `working`

Available now:

- audit log stream from `/api/rbac/audit-logs/`
- real counts for operators, pending verification items, disputes, and moderation queue

Limitations:

- metrics are operational, but still narrower than a full BI dashboard

Frontend:

- `frontend/src/components/admin/OverviewSection.vue`

Backend:

- `backend/rbac/views.py`

---

### 2. Verifications

Current state: `working`

Available now:

- contractor verification review
- contractor approval from the admin UI
- vendor approval and rejection
- investor KYC approval and rejection

Not currently available in the admin dashboard:

- document review detail workflow

Frontend:

- `frontend/src/components/admin/VerificationsSection.vue`

Backend:

- `backend/contractors/views.py`
- vendor status update support exists in `backend/vendors/views.py`, but is not surfaced in the current admin dashboard

---

### 3. User and Operator Management

Current state: `working`

Available now:

- user activation and role reassignment through the dedicated operator module
- user activation and role reassignment through the system configuration module
- Django group role creation and deletion

Limitations:

- operator creation is still routed to an external or central workflow

Frontend:

- `frontend/src/components/admin/SystemConfigSection.vue`
- `frontend/src/components/admin/UserManagementSection.vue`

Backend:

- `backend/platform_settings/views.py`

---

### 4. System Configuration

Current state: `working`

Available now:

- platform identity settings
- support contact details
- default region
- currency CRUD and rate updates
- country CRUD and default-country selection
- taxonomy category CRUD
- admin user activation and role update
- role/group CRUD
- predefined RBAC permission assignment to roles

Frontend:

- `frontend/src/components/admin/SystemConfigSection.vue`

Backend:

- `backend/platform_settings/views.py`
- `backend/taxonomy/views.py`

---

### 5. Security Monitoring

Current state: `working`

Available now:

- throttled request and violation log viewing
- security summary counts from violation data

Frontend:

- `frontend/src/components/admin/SecurityMonitorSection.vue`

Backend:

- `backend/security/views.py`

---

### 6. Reports and Compliance Downloads

Current state: `working`

Available now:

- regulatory report listing and export surface
- **comprehensive analytics dashboard** with 8 report categories (Overview, Financial, Marketplace, Users, Operations, Real Estate, Geographic, Regulatory)
- interactive charts (area, bar, donut, pie) powered by ApexCharts
- date-range filtering (7D, 30D, 90D, 1Y)
- server-side aggregation for all metrics

Frontend:

- `frontend/src/views/RegulatoryReports.vue`
- `frontend/src/components/admin/ReportsSection.vue`

Backend:

- `backend/reporting/views.py`
- `backend/reporting/analytics.py`

---

### 7. Property Registry

Current state: `working for listing, partial for admin operations`

Available now:

- property listing visibility in the admin dashboard
- summary statistics based on loaded property records

Limitations:

- the management action surface is shallow
- no deep admin moderation workflow is exposed yet

Frontend:

- `frontend/src/components/admin/PropertiesSection.vue`

Backend:

- `backend/property/views.py`

---

### 8. Disputes and Escrow Resolution

Current state: `working`

Available now:

- dispute creation
- evidence submission
- admin resolve endpoint with release/refund path
- dispute queue
- refund/release controls for admins

Backend:

- `backend/disputes/views.py`

---

## Working Interpretation

When planning admin work, use this rule:

1. trust `SystemConfigSection` for real admin settings functionality
2. treat `SecurityMonitorSection` and the audit log feed as real
3. treat `VerificationsSection`, `OverviewSection`, `UserManagementSection`, and `ModerationSection` as live operator surfaces
4. assume advanced compliance document review still needs deeper workflow UI

---

## Recommended Next Admin Fixes

1. add vendor verification to the admin verification module
2. add investor KYC review to the admin verification module
3. build a disputes admin module with resolve controls
4. repair or consolidate the dedicated user-management panel
