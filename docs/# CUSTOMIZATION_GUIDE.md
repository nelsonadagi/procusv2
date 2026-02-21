# CUSTOMIZATION_GUIDE.md

## Construction Marketplace MVP — Customization Guide (Phase 1)

This document defines how the platform should remain **highly customizable** from Day 1.

Goal: Enable regional adaptation and future expansion without rewrites.

---

## 1. Config-Driven Marketplace Design

Key marketplace elements must be configurable:

* Product categories
* Units of sale
* Supported payment providers
* Delivery rules

Store these in:

* Database tables
* YAML/JSON config files
* Admin-managed settings

---

## 2. Branding & Theming

Frontend should support:

* Custom logo
* Primary/secondary colors
* Typography variables

Implement via:

* CSS variables
* Theme config module

---

## 3. Feature Flags

Enable controlled rollout of features:

* Financing (Phase 2)
* Escrow (Phase 3)
* Projects marketplace (Phase 4)

Feature flags can be:

* Environment-based
* Database-driven

---

## 4. Regional Expansion Support

Design for:

* Multi-currency pricing
* Local tax rules
* Region-specific logistics partners

Approach:

* Region model + configuration mapping

---

## 5. Modular Django Apps

Each domain is isolated:

* catalog
* orders
* payments
* logistics

This ensures new modules can be added cleanly.

---

## 6. Vendor Customization

Allow vendors to:

* Manage storefront profile
* Set delivery zones
* Configure minimum order quantities

---

## 7. Admin Customization

Admins must be able to configure:

* Category activation
* Verification requirements
* Dispute workflows

Use Django Admin as control center.

---

**Customization foundation is now defined for Phase 1.**
