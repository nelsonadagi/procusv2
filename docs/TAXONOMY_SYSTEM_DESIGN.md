# TAXONOMY_SYSTEM_DESIGN.md

## Taxonomy System Design — Construction Marketplace Platform

This document defines how taxonomy (hierarchical classification) is implemented across the platform.

Taxonomy is a platform primitive, alongside RBAC, escrow, and payments.

---

# 1. What is Taxonomy?

A taxonomy is a structured classification system that organizes platform entities into categories and subcategories.

Example:

* Materials

  * Cement

    * Portland Cement
    * Rapid Set Cement
  * Steel

    * Rebar
    * Structural Steel

Taxonomy enables:

* Search and filtering
* Marketplace discovery
* Analytics and reporting
* Contractor matching
* Financing risk scoring
* Compliance classification

---

# 2. What Requires Taxonomy in This Platform?

## Phase 1

* Materials categories

## Phase 2

* Contractor service categories
* Contract/tender classifications

## Phase 3

* Financing product taxonomy

## Phase 4

* Project type taxonomy
* Property asset taxonomy

## Phase 5

* Government procurement classifications
* Enterprise procurement categories

## Phase 6

* Jurisdiction compliance taxonomies
* Regulatory reporting classifications

---

# 3. Design Principle

Taxonomies must NOT be hardcoded.

They must be:

1. Stored in the database (source of truth)
2. Seeded from configuration files (default bootstrap)
3. Editable via admin backoffice (runtime customization)

---

# 4. Database Schema (Source of Truth)

## Generic Category Model

A universal hierarchical model supports all taxonomies.

### `taxonomy_category`

Fields:

* id
* name
* slug
* taxonomy_type (MATERIAL/SERVICE/PROJECT/PROPERTY/FINANCE)
* parent_id (self FK, nullable)
* active (boolean)
* region_code (nullable)
* created_at

This enables:

* Infinite nesting
* Regional customization
* Shared structure across domains

---

# 5. Taxonomy Seed Files (Platform Defaults)

Default taxonomies are stored in:

```
backend/taxonomy/seeds/
  materials.yaml
  services.yaml
  projects.yaml
  property.yaml
  finance.yaml
```

Example `materials.yaml`:

```yaml
materials:
  - Cement:
      - Portland Cement
      - Rapid Set Cement
  - Steel:
      - Rebar
      - Structural Steel
```

---

# 6. Seed Command

Taxonomies must be loaded automatically using:

```bash
python manage.py seed_taxonomies
```

The command:

* Creates missing categories
* Preserves existing edits
* Supports region-specific overrides

---

# 7. Admin Management Layer

Taxonomies must be editable through Django Admin:

Admins can:

* Add new categories
* Disable obsolete categories
* Define region-specific variants
* Control ordering and visibility

Taxonomy changes must not require redeployment.

---

# 8. Platform Integration

## 8.1 Catalog Products

Each product references a taxonomy category:

* product.category_id → MATERIAL taxonomy

Search uses subtree expansion.

---

## 8.2 Contractor Matching

Contractors reference service categories:

* contractor.services → SERVICE taxonomy

Projects can auto-suggest contractors.

---

## 8.3 Project Requirements

Projects define requirements using taxonomy:

* MATERIAL requirements
* SERVICE requirements

---

## 8.4 Financing Eligibility

Financing products are classified by taxonomy:

* Material Credit
* Working Capital
* Factoring

Taxonomy drives underwriting rules.

---

## 8.5 Compliance & Government Procurement

Government tenders require classification:

* Infrastructure
* Housing
* Roads

Taxonomy ensures audit-ready reporting.

---

# 9. Phase-by-Phase Taxonomy Growth

| Phase   | Taxonomies Introduced   |
| ------- | ----------------------- |
| Phase 1 | Materials               |
| Phase 2 | Services, Contracts     |
| Phase 3 | Finance Products        |
| Phase 4 | Projects, Property      |
| Phase 5 | Government, Enterprise  |
| Phase 6 | Jurisdiction Compliance |

---

# 10. Strategic Importance

Taxonomy is a long-term platform moat:

* Enables structured global marketplace scaling
* Supports AI-driven recommendations
* Powers compliance and reporting
* Improves financing underwriting

---

**Taxonomy System Design Complete.**
