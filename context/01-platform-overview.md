# Platform Overview

## Summary

Procus v2 is a multi-role construction marketplace platform covering procurement, contracting, project execution, escrow-backed payments, investment, logistics, compliance, reporting, and admin operations.

The platform is implemented as:

- A Vue 3 single-page application in `frontend/`
- A Django REST Framework backend in `backend/`
- PostgreSQL, Redis, Celery, and Docker-based infrastructure

## Product scope

The documented scope spans the full lifecycle of construction activity:

- Material discovery and ordering
- Vendor onboarding and inventory management
- Contractor registration and bidding
- Contract creation and milestone tracking
- Escrow and finance workflows
- Project lifecycle and investment commitments
- Standalone property operations, inquiries, appointments, and capital marketplace features
- Compliance, KYC, AML, and government procurement
- Regulatory reporting, banking settlement, and AI-assisted risk workflows

## Primary user roles

- `PROJECT_OWNER`: base default user identity; project creation, procurement, and owner-side execution
- `VENDOR`: approved supplier specialization for product listing, inventory, quotes, fulfillment
- `CONTRACTOR`: approved service-provider specialization for registration, tender discovery, and bid submission
- `INVESTOR`: approved capital-provider specialization for onboarding, commitments, and agreements
- `PROPERTY_MANAGER`: approved property-operations specialization for listing management, inquiries, appointments, and owner-side property workflows
- `COURIER`: approved logistics specialization for shipment, pricing, and delivery operations
- `GOVERNMENT`: approved institutional specialization for tender and procurement workflows
- `ADMIN`: separate operator identity for platform operations, governance, configuration, and moderation

## Role model in practice

- new non-admin users should start as `PROJECT_OWNER`
- other non-admin roles should be added after user-initiated onboarding and admin approval
- normal users may hold multiple non-admin roles
- `ADMIN` should be manually assigned and kept separate from normal multi-role user identities

## Major business areas

- Identity and access
- Marketplace commerce
- Construction contracts
- Financial infrastructure
- Project and property systems
- Investment and enterprise workflows
- Compliance and regulation
- Logistics and integrations
- Intelligence, reporting, and admin tooling

## Context sources

- `docs/SRS.md`
- `docs/SDD.md`
- `docs/PHASES.md`
- `docs/ROLE_AND_ONBOARDING_POLICY.md`
- `README.md`
