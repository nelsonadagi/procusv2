# PROPERTY_SCHEMA.md

## Phase 4+ — Property Marketplace And Asset Operations Schema

This document defines the target data model for the property module as a standalone but fully integrated platform domain.

The property module should support:

* property owners and approved property managers listing and operating property assets
* public and authenticated users discovering properties
* anonymous inquiries and appointment booking with callback or email details
* optional property-to-project linkage
* financing for either property acquisition/completion or project completion
* downstream material and service orchestration when a property is linked to a project

---

## 1. Property Listing Entity

### Property Listing (`property_listing`)

Fields:

* id
* owner_id (FK → accounts_user)
* manager_id (FK → accounts_user, nullable)
* listed_by_id (FK → accounts_user)
* title
* description
* asset_type (LAND/RESIDENTIAL/COMMERCIAL/INDUSTRIAL/MIXED_USE/HOSPITALITY/RENOVATION/SPECIAL_PURPOSE)
* listing_type (SALE/LEASE/DEVELOPMENT_OPPORTUNITY/COMPLETED_PROJECT)
* price_estimate
* financing_allowed (boolean)
* inquiry_enabled (boolean)
* appointment_enabled (boolean)
* country_id
* location_text
* formatted_address
* latitude
* longitude
* status (DRAFT/ACTIVE/UNDER_OFFER/SOLD/LEASED/INACTIVE)
* created_at
* updated_at

Notes:

* `owner_id` captures legal or beneficial ownership.
* `manager_id` supports the approved `PROPERTY_MANAGER` role operating the listing on behalf of the owner.
* standalone property listings remain valid even when no project exists yet.

---

## 2. Development And Operating Metadata

### Development Metadata (`property_development`)

Fields:

* id
* property_id
* zoning_info
* build_ready (boolean)
* utilities_available
* development_stage (RAW_LAND/SERVICED_SITE/IN_DESIGN/IN_PROGRESS/COMPLETED)
* estimated_completion_budget
* expected_completion_date
* recommended_use

Purpose:

* describes development readiness
* informs whether the asset should remain standalone or progress into a linked project
* supports finance, project-setup, and procurement decisions

---

## 3. Structured Property Profile

Modern property listings should support a richer profile around the core listing instead of overloading one table with every possible field.

### Property Specification (`property_specification`)

Fields:

* id
* property_id
* bedrooms
* bathrooms
* floors
* parking_spaces
* internal_area
* internal_area_unit
* lot_size
* lot_size_unit
* year_built
* renovation_year
* furnishing_state
* condition_rating
* energy_rating
* occupancy_status

Purpose:

* captures searchable built-asset facts
* supports richer listing comparison on detail and search pages
* allows different asset classes to expose only the relevant specifications

### Property Feature (`property_feature`)

Fields:

* id
* property_id
* category
* code
* name
* description
* is_highlighted

Purpose:

* models amenities and selling points in a structured way
* supports filtering, search boosting, and detail-page highlights

### Property Media Asset (`property_media_asset`)

Fields:

* id
* property_id
* media_type (IMAGE/VIDEO/FLOOR_PLAN/DOCUMENT/VIRTUAL_TOUR)
* file
* external_url
* title
* caption
* alt_text
* sort_order
* is_primary
* is_public

Purpose:

* supports gallery, floor plans, virtual tours, and downloadable attachments
* allows the property detail page to feel like a decision surface, not a plain record

### Property Ownership Profile (`property_ownership_profile`)

Fields:

* id
* property_id
* legal_owner_name
* ownership_type
* title_reference
* deed_reference
* has_liens
* lien_notes
* disclosure_notes
* verification_status

Purpose:

* stores due-diligence context separately from the public listing body
* supports internal review, financing, and higher-trust transactions

### Property Pricing Profile (`property_pricing_profile`)

Fields:

* id
* property_id
* currency
* asking_price
* rent_amount
* pricing_strategy
* requires_deposit
* deposit_amount
* price_per_area_unit
* area_unit
* service_charge_amount
* tax_percentage
* insurance_percentage
* financing_notes

Purpose:

* normalizes pricing for sale, rent, and development opportunities
* supports finance and affordability presentation on the property detail page

### Property Showing (`property_showing`)

Fields:

* id
* property_id
* event_type (OPEN_HOUSE/PRIVATE_SHOWING)
* occurrence_type (SINGLE/RECURRING/APPOINTMENT_ONLY)
* start_at
* end_at
* recurrence_rule
* recurrence_end_at
* contact_person
* phone
* instructions
* virtual_tour_url
* is_active

Purpose:

* supports richer property calendar use cases beyond raw appointment slots
* allows open houses, recurring viewings, and appointment-only schedules

Implementation note:

* `PropertyListing` remains the root entity
* the richer profile should be layered through focused one-to-one and one-to-many submodels
* public listing, inquiry, appointment, project-link, and finance workflows should continue to work even when some profile sections are incomplete

---

## 4. Property Inquiry Layer

### Property Inquiry (`property_inquiry`)

Fields:

* id
* property_id
* inquirer_user_id (nullable FK → accounts_user)
* inquiry_type (GENERAL/VIEWING/FINANCING/PARTNERSHIP/MATERIALS/SERVICE)
* full_name
* email
* phone_number
* preferred_contact_method
* message
* status (NEW/CONTACTED/QUALIFIED/CLOSED/SPAM)
* chat_room_id (nullable)
* created_at

Rules:

* anonymous inquiries are allowed if callback phone or email is provided
* creating an inquiry should create notifications for the owner/manager
* inquiry creation should also open or attach a chat thread so the actors can respond quickly

---

## 5. Appointment And Availability Layer

### Property Availability Window (`property_availability_window`)

Fields:

* id
* property_id
* managed_by_id
* start_at
* end_at
* recurrence_rule (nullable)
* slot_duration_minutes
* is_active

### Property Appointment (`property_appointment`)

Fields:

* id
* property_id
* availability_window_id (nullable)
* visitor_user_id (nullable FK → accounts_user)
* full_name
* email
* phone_number
* scheduled_start
* scheduled_end
* notes
* status (REQUESTED/CONFIRMED/COMPLETED/CANCELLED/NO_SHOW)
* created_by_id (nullable FK → accounts_user)
* created_at

Rules:

* public visitors should be able to see available slots
* property owners and managers define and maintain the availability calendar
* booking an appointment should create notifications and a chat-capable communication trail

---

## 6. Property → Project Link

### Property Project Link (`property_project_link`)

Fields:

* id
* property_id
* project_id
* linkage_type (ORIGIN_SITE/SHOWCASE_ASSET/COMPLETED_PROJECT/DEVELOPMENT_PIPELINE)
* created_by_id
* created_at

Purpose:

* keeps property standalone while allowing transition into project execution
* enables users to move from property detail into project detail and back
* allows a completed project to continue to exist as a financeable or marketable property

---

## 7. Financing Relationship

Financing should be supported for either a property or a project.

Target rule:

* a finance application may reference a `property_id`
* a finance application may reference a `project_id`
* either reference may be present depending on the financing use case

Examples:

* acquire a completed property
* finance completion of a property under development
* finance completion of a project linked to a property

---

## 8. Procurement And Materials Relationship

The property module should integrate with materials in two modes:

### Standalone property mode

* property detail can surface suggested materials, finishes, fixtures, or service categories
* users may browse and purchase materials independently through the main marketplace

### Project-linked mode

* when a property is linked to a project, material and service demand should be structured through `ProjectRequirement`
* linked requirements can then feed procurement, quote requests, vendor orders, contracts, and milestone execution

---

## 9. Property Detail Aggregate View

The target property detail experience should aggregate:

* core property information
* structured specifications and feature highlights
* pricing profile and commercial terms
* media gallery, floor plans, and virtual tours
* ownership or verification context where appropriate
* development metadata
* showing schedule and appointment availability
* inquiry actions and communication status
* appointment calendar and upcoming visits
* financing options and application entry points
* linked project summary where applicable
* recommended or required materials/services
* activity history and operational notes for the owner/manager

---

**Property schema target updated for standalone operation plus cross-module integration.**
