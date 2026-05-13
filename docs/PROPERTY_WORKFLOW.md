# PROPERTY_WORKFLOW.md

## Property Module Workflow Model

This document defines the intended operating model for the property module.

The property module is both:

* a standalone marketplace for property assets
* an integration hub that can connect into projects, finance, procurement, chat, notifications, and investment

It should not be treated as a dead-end listing catalog.

---

## 1. Core Product Position

The property module exists to support:

* listing land and built assets
* managing development opportunities
* moving from a property opportunity into project execution
* financing either a property itself or a project linked to that property
* allowing public discovery and lead generation
* exposing a rich property detail page for operational follow-through

---

## 2. Primary Actors

The property module is interacted with by **7 distinct actor types**.

### 1. Public / Unauthenticated Visitor (GUEST)

* browses property listings (`/properties`)
* views property detail (`/properties/:id`)
* submits inquiries if `inquiry_enabled` is true (anonymous allowed with phone/email)
* requests viewing appointments if `appointment_enabled` is true
* views available time slots via the `availability` endpoint

**Backend access:** `list`, `retrieve`, `availability` actions on `PropertyViewSet` are `AllowAny`.

### 2. Project Owner (PROJECT_OWNER)

* default base role for new users
* creates property listings
* updates / deletes **own** listings
* links properties to projects (`/v1/property/{id}/link-project/`)
* sets availability windows for viewings
* manages appointments and inquiries on owned properties
* assigns a property manager

**Backend permissions:** `property:view`, `property:list_property`, `property:update_property`

### 3. Property Manager (PROPERTY_MANAGER)

* approved specialized role (requires onboarding + admin approval)
* creates listings on behalf of property owners
* updates / manages properties where assigned as `manager`
* publishes availability windows
* manages appointments and inquiries on managed properties
* accesses the dedicated Property Manager Hub (`/property-manager/dashboard`)

**Backend permissions:** `property:view`, `property:list_property`, `property:update_property`

### 4. Buyer (BUYER)

* no explicit `property:*` permissions in RBAC matrix
* browses and views public listings
* submits inquiries
* books appointments
* accesses linked project details from a property page

### 5. Investor (INVESTOR / VERIFIED_INVESTOR)

* browses properties via public routes only
* evaluates properties as acquisition or development opportunities
* properties can be linked to investment projects they pledge into
* **No direct property CRUD** — no `property:*` permissions in RBAC matrix

### 6. Admin / Staff (ADMIN)

* full CRUD on **all** properties regardless of ownership
* manages all inquiries, appointments, and availability windows
* accesses Property Console from Admin Dashboard (`/admin`)
* views regulatory reports (`/admin/reports`)

**Backend access:** `ADMIN` role bypasses all ownership checks via `IsPropertyOperator` and `IsPropertyOwner`.

### 7. Finance / Banking Actor (via Finance Module)

* indirect interaction through `FinanceApplication`
* `FinanceApplication` may reference a `PropertyListing` via `property` FK
* investors can apply for property financing
* property detail page exposes financing entry points

**Model link:** `backend/finance/models.py` → `property = ForeignKey(PropertyListing)`

---

## 3. Listing Workflow

1. A property owner or approved property manager creates a property listing.
2. The listing is classified by asset type, listing type, location, and development stage.
3. Structured property profile sections are added as needed:
   * specifications
   * features and amenities
   * media and virtual-tour assets
   * pricing profile
   * ownership or disclosure context
4. Development metadata is added to show readiness, zoning, and utilities.
5. The operator decides whether the listing is:
   * a standalone property opportunity
   * a development opportunity that may become a project
   * a completed project that should remain marketable as a property
6. The property detail page becomes the hub for discovery, inquiries, appointments, financing, and linked project access.

---

## 4. Discovery, Inquiry, And Appointment Workflow

### Discovery

* public and authenticated users search by location, asset type, value, and development profile
* property results should be discoverable separately from projects, while still allowing transitions between the two modules

### Inquiry

1. Visitor opens property detail.
2. Visitor submits an inquiry.
3. Anonymous inquiry is allowed if callback phone number or email is supplied.
4. Inquiry automatically creates:
   * notifications for the property owner/manager
   * a communication thread or chat context
5. Owner/manager responds and qualifies the lead.

### Appointment

1. Property owner or manager defines available viewing slots.
2. Property detail page shows those slots on a calendar.
3. Visitor selects a slot and provides required contact information.
4. Appointment booking creates notifications and a communication thread.
5. Owner/manager confirms, reschedules, completes, or cancels the visit.

---

## 5. Property ↔ Project Workflow

Property must remain standalone, but it can become the origin point of a project.

Supported patterns:

### Property-first pattern

1. A property is listed as land, a renovation opportunity, or a development asset.
2. The owner or manager decides to start execution inside the platform.
3. A project is created and linked to the property.
4. Requirements, contracts, milestones, financing, and updates happen through the project.

### Project-first pattern

1. A project already exists in the platform.
2. The project is linked to a property record to expose site context, asset value, and downstream property marketability.

### Completed-project pattern

1. A project reaches completion.
2. The asset remains financeable, marketable, and viewable as a property.
3. Users can still move from the property detail page to the historical project context.

---

## 6. Property ↔ Finance Workflow

Finance should support either property or project targets.

### Property-targeted finance

Use cases:

* acquire a completed property
* finance renovation or completion of a property asset
* fund infrastructure improvements prior to full project setup

### Project-targeted finance

Use cases:

* finance completion of a linked project
* support structured project budgets, milestones, and execution cash flow

Documentation rule:

* finance applications should be allowed against either a property or a project
* the property module should expose financing entry points on the property detail page

---

## 7. Property ↔ Materials And Procurement Workflow

### Standalone property mode

* users can browse and buy materials independently from the property flow
* property detail can surface suggested products or categories, but material purchasing remains available to any marketplace user

### Project-linked mode

1. Property is linked to a project.
2. Project requirements define materials, services, and contractor demand.
3. Those requirements feed quote requests, vendor sourcing, contracts, and execution workflows.

This means procurement becomes formal when the property is moved into a project lifecycle.

---

## 8. Chat And Notification Rule

Property inquiries and appointments should automatically create:

* notifications
* an actionable communication thread

The same principle should apply across other inquiry-driven modules where fast coordination matters.

---

## 9. Property Detail Page

The property detail page should become a full operating surface, not just a brochure page.

It should include:

* gallery, floor plans, and virtual-tour assets
* asset summary and structured specifications
* feature and amenity highlights
* pricing profile and commercial terms
* ownership/management context where appropriate
* development readiness and zoning
* showing schedule and open-house visibility where relevant
* availability calendar and appointment booking
* inquiry and callback actions
* financing entry points
* linked project summary
* suggested materials/services or linked project requirements
* communication history and updates

---

## 10. Documentation Rule

When future property docs are updated:

* keep property standalone by default
* document the link to projects explicitly
* document financing as valid for both property and project
* treat inquiries and appointments as first-class workflows
* treat chat and notifications as automatic response infrastructure
* keep the property profile rich enough to support search, due diligence, and financing review without forcing everything into the root listing model

---

**Property workflow model defined for the integrated standalone-property direction.**
