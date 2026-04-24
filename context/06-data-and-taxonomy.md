# Data And Taxonomy

## Data model themes

The system is built around a few recurring entity families:

- users, profiles, and organizations
- vendors, contractors, and couriers
- products, orders, quotes, and reviews
- contracts, bids, and milestones
- escrow, disputes, finance, and scoring
- projects, requirements, commitments, and updates
- property, investment, and government tender records
- platform settings, countries, currencies, and taxonomies

## Taxonomy role in the platform

Taxonomy is treated as a core platform capability, not a side table. It supports classification across multiple business domains such as:

- materials
- services
- projects
- property
- finance
- government tenders
- compliance jurisdictions

## Why taxonomy matters here

- powers discovery and filtering
- standardizes onboarding forms
- supports domain-specific categorization
- improves reporting and policy logic
- reduces free-text inconsistency across modules

## Data design patterns in the docs

- normalized entities for core business records
- JSON fields for flexible supplemental metadata
- status-driven workflows
- auditability for regulated and financial actions
- location-aware fields for country, formatted address, and hierarchy

## Important source docs

- `docs/DATABASE_SCHEMA.md`
- `docs/TAXONOMY_SYSTEM_DESIGN.md`
- `docs/MATERIALS_TAXONOMY.md`
- `docs/SERVICES_TAXONOMY.md`
- `docs/PROJECTS_TAXONOMY.md`
- `docs/PROPERTY_TAXONOMY.md`
- `docs/FINANCE_TAXONOMY.md`
- `docs/GOVERNMENT_TENDER_TAXONOMY.md`
- `docs/COMPLIANCE_JURISDICTION_TAXONOMY.md`
