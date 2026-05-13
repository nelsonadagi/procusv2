# API Truth Map

## Purpose

This file is a practical routing reference. Use it before wiring frontend calls, writing tests, or documenting endpoints.

## Root API namespaces

Defined in backend routing:

- `/api/v1/` -> `catalog`
- `/api/v2/` -> contracts and contractor-era versioned routes
- `/api/v3/` -> escrow, disputes, finance, scoring
- `/api/v4/` -> projects and property
- `/api/v5/` -> regulated investment and government-era routes
- `/api/v6/` -> banking, reporting, AI, secondary market, integrations
- `/api/accounts/`
- `/api/rbac/`
- `/api/taxonomy/`
- `/api/platform_settings/`
- `/api/vendors/`
- `/api/orders/`
- `/api/reviews/`
- `/api/contractors/`
- `/api/contracts/`
- `/api/projects/`
- `/api/bids/`
- `/api/milestones/`
- `/api/notifications/`
- `/api/property/`
- `/api/security/`
- `/api/logistics/`
- `/api/compliance/`
- `/api/chat/`

## High-confidence route truths

### Accounts

Base:

- `/api/accounts/register/`
- `/api/accounts/login/`
- `/api/accounts/profile/`
- `/api/accounts/management/`
- `/api/accounts/addresses/`

### Taxonomy

Base:

- `/api/taxonomy/categories/`

### Platform settings

Base:

- `/api/platform_settings/platform/`
- `/api/platform_settings/currencies/`
- `/api/platform_settings/countries/`
- `/api/platform_settings/admin-users/`
- `/api/platform_settings/roles/`
- `/api/platform_settings/features/`
- `/api/platform_settings/payment-gateways/`
- `/api/platform_settings/payment-methods/`

### Vendors

Base:

- `/api/vendors/`
- `/api/vendors/me/`

### Catalog

Base:

- `/api/v1/products/`
- `/api/v1/product-images/`

Catalog custom actions:

- `/api/v1/products/locations/`
- `/api/v1/products/me/`
- `/api/v1/products/{id}/inventory-history/`
- `/api/v1/products/{id}/adjust-inventory/`
- `/api/v1/products/{id}/upload_images/`
- `/api/v1/products/import_products/`

### Orders and quote workflow

Base:

- `/api/orders/`
- `/api/orders/quote-requests/`

Order custom actions include:

- `/api/orders/{id}/update_fulfillment/`
- `/api/orders/{id}/confirm_delivery/`
- `/api/orders/{id}/cancel_order/`
- `/api/orders/{id}/initiate_dispute/`
- `/api/orders/vendor_orders/`

Quote request custom actions include:

- `/api/orders/quote-requests/{id}/respond/`
- `/api/orders/quote-requests/{id}/checkout/`

Order custom actions include:

- `/api/orders/{id}/simulate_payment/`

### Contractors

Base:

- `/api/contractors/`

Important note:

- any frontend usage of `/api/contractors/register/` should be verified against actual view actions before relying on it

### Contracts

Base:

- `/api/contracts/`
- `/api/v2/contracts/`

Custom actions:

- `/api/contracts/{id}/bids/`
- `/api/contracts/{id}/milestones/`
- `/api/contracts/{id}/review/`

### Bids

Base:

- `/api/bids/`
- `/api/v2/bids/`

### Finance

Base:

- `/api/v3/finance/products/`
- `/api/v3/finance/applications/`

Notes:

- finance products are public catalog entries
- finance applications require authentication and permission checks
- financing targets may include projects, properties, contracts, and material orders depending on serializer payload

### Milestones

Base:

- `/api/milestones/`
- `/api/v2/milestones/`

Expected custom actions:

- approval-related actions should be verified directly in the view before wiring

### Projects

Base:

- `/api/projects/`
- `/api/v4/projects/`

Custom actions:

- `/api/v4/projects/{id}/requirements/`
- `/api/v4/projects/{id}/commit/`
- `/api/v4/projects/{id}/commitments/`
- `/api/v4/projects/{id}/link-contract/`
- `/api/v4/projects/{id}/updates/`

### Property

Base:

- `/api/property/`
- `/api/v4/property/`

### Logistics

Base:

- `/api/logistics/carriers/`
- `/api/logistics/couriers/`
- `/api/logistics/pricing-zones/`
- `/api/logistics/pricing-rules/`
- `/api/logistics/shipments/`

Important note:

- there is no router evidence for `/api/logistics/zones/`; use `pricing-zones`

### Security

Base:

- `/api/security/violations/`

### Chat

Base:

- `/api/chat/rooms/`
- `/api/chat/messages/`
- `/api/chat/attachments/`

Any custom room actions like `get-or-create` should be verified in the view before assuming availability.

## Version guidance

Use these rules when implementing:

1. If a frontend page already uses a stable direct namespace like `/api/accounts/` or `/api/orders/`, prefer consistency there.
2. Use versioned namespaces when the backend explicitly groups a phase or compatibility layer there.
3. Avoid inventing new frontend paths without verifying backend router registration.

## Common mistakes to avoid

- using `/v2/projects/` instead of `/v4/projects/` or `/projects/`
- using `/logistics/zones/` instead of `/logistics/pricing-zones/`
- using `/config/countries/` instead of `/platform_settings/countries/`
- assuming docs-only endpoints exist because they are named in a phase document
