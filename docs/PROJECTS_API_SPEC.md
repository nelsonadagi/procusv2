# PROJECTS_API_SPEC.md

## Phase 4 — Projects Marketplace API Specification

This document defines the REST API endpoints required for Phase 4.

Base URL:

`/api/v4/`

---

## 1. Project APIs

### POST `/projects`

Create a new project listing.

Request:

* title
* description
* location
* estimated_budget
* funding_required

Response:

* project_id

---

### GET `/projects`

List active projects.

Query params:

* location
* status
* funding_required

---

### GET `/projects/{id}`

Retrieve project detail.

---

## 2. Project Requirements

### POST `/projects/{id}/requirements`

Add required materials/services.

Request:

* type
* description
* quantity

---

## 3. Investment Commitment APIs (Foundation)

### POST `/projects/{id}/commit`

Investor pledges commitment.

Request:

* amount_committed

Response:

* commitment_id

---

### GET `/projects/{id}/commitments`

Owner views commitments.

---

## 4. Execution Linkage

### POST `/projects/{id}/link-contract`

Link awarded contract to project.

Request:

* contract_id

---

## 5. Project Updates

### POST `/projects/{id}/updates`

Owner posts progress update.

Request:

* update_text

---

### GET `/projects/{id}/updates`

List updates.

---

## 6. Permissions

* Only owners can create projects
* Only investors can commit funding
* Only owners can link contracts and post updates

---

**Phase 4 projects API contract is now defined.**
