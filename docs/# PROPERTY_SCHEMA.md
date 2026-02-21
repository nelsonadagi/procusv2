# PROPERTY_SCHEMA.md

## Phase 4 — Property Marketplace Database Schema

This document defines the database structures required for property and development asset listings.

---

## 1. Property Listing Entity

### Property Listing (`property_listing`)

Fields:

* id
* owner_id (FK → accounts_user)
* title
* description
* location
* asset_type (LAND/RESIDENTIAL/COMMERCIAL/RENOVATION)
* price_estimate
* status (ACTIVE/SOLD/INACTIVE)
* created_at

---

## 2. Development Potential

### Development Metadata (`property_development`)

Fields:

* id
* property_id
* zoning_info
* build_ready (boolean)
* utilities_available

---

## 3. Property → Project Link

### Property Project Link (`property_project_link`)

Fields:

* id
* property_id
* project_id

---

**Phase 4 property schema is now defined.**
