# Material Workflow Fixes & UX Transformation

**Date:** 2026-05-17  
**Status:** Implementation Complete

---

## 🔴 Critical Fixes

### 1. ProductListSerializer Certification Highlights Crash
**File:** `backend/catalog/serializers.py`

**Bug:** `get_certification_highlights()` referenced `entry.registry_name` on a model instance. `registry_name` is a serializer field, not a model attribute.

**Fix:** Removed `entry.registry_name` and safely fall back to `entry.registry.name` with null check.

---

### 2. Unapproved Vendors Could Create Products
**Files:** `backend/catalog/views.py`, `backend/rbac/permissions.py`

**Bug:** `get_permissions()` returned `[IsAuthenticated()]` for `create` and `import_products`. `perform_create` only checked `hasattr(user, 'vendor_profile')`, not `verified_status == 'APPROVED'`.

**Fix:**
- Added `VendorApprovedOnly` permission class to all mutating actions
- Added explicit approval checks in `perform_create`, `import_products`, `upload_images`, and `upload_documents`

**Permissions after fix:**

| Action | Required Permissions |
|--------|---------------------|
| `list`, `retrieve` | `AllowAny` |
| `me` | `IsAuthenticated` |
| `create`, `import_products` | `IsAuthenticated`, `VendorApprovedOnly`, `HasRequiredPermission` |
| `update`, `partial_update`, `destroy`, `upload_images`, `upload_documents`, `adjust_inventory`, `inventory_history` | `HasRequiredPermission`, `IsVendorOwner`, `VendorApprovedOnly` |

---

### 3. Vendor Dashboard "Certified" Count Stuck at 0
**File:** `frontend/src/components/vendor/VendorInventorySection.vue`

**Fix:** Changed `certification_highlights?.length` → `certification_entries?.length` since `/v1/products/me/` returns `ProductSerializer`.

---

### 4. DRF Validation Errors Swallowed in Frontend
**File:** `frontend/src/components/vendor/VendorInventorySection.vue`

**Fix:** `saveProduct` now parses DRF error objects and surfaces the first field-level message.

---

## 🟡 Medium Fixes

### 5. Product.save() Auto-Overwrote Vendor Status Choices
**File:** `backend/catalog/models.py`

**Fix:** Status auto-update now only runs when the product is **new** or `stock_quantity` **actually changed**.

---

### 6. Search Only Triggered on Enter
**File:** `frontend/src/views/ProductList.vue`

**Fix:** Added `watch(searchQuery, debouncedSearch)` so the main marketplace search fires as the user types (400ms debounce).

---

### 7. Mobile Inventory Signal Raw Value
**File:** `frontend/src/components/vendor/VendorInventoryList.vue`

**Fix:** Mobile view now uses `formatInventorySignal()` instead of raw `inventory_signal`.

---

## 🟠 Gap Fixes

### 8. Marketing Flags Added to Vendor Form
**File:** `frontend/src/components/vendor/VendorInventorySection.vue`

Added checkbox row in the Commercial tab for `is_featured`, `is_new_arrival`, and `is_on_sale`.

---

### 9. Image & Document Deletion in Vendor Modal
**Files:** `backend/catalog/views.py`, `frontend/src/components/vendor/VendorInventorySection.vue`

- Backend: Added `remove_document` action to `ProductViewSet`
- Frontend: Added delete buttons (×) to existing image and document chips in the Media tab

---

### 10. Quantity Selector on Product Detail
**File:** `frontend/src/views/ProductDetail.vue`

Added a quantity stepper control. `requestQuote` now uses the selected quantity instead of defaulting to `min_order_quantity`.

---

### 11. Product Comparison Modal
**File:** `frontend/src/views/ProductList.vue`

The sticky compare bar's "COMPARE PRODUCTS" button now opens a side-by-side comparison table for up to 4 selected products.

---

### 12. contactVendor Button Removed
**File:** `frontend/src/views/ProductDetail.vue`

Removed the non-functional "Contact Vendor" button.

---

### 13. Destructive Nested Updates Fixed
**File:** `backend/catalog/serializers.py`

Rewrote `_save_nested()` to use diff-based updates by natural key, preserving PKs and supporting partial updates.

---

### 14. effective_price Respects bulk_threshold
**File:** `backend/catalog/models.py`

`effective_price` now only returns `bulk_price` when **both** `bulk_price` and `bulk_threshold` are configured.

---

### 15. DB-Level Uniqueness on slug
**File:** `backend/catalog/models.py`

Changed `unique=False` to `unique=True`. Added migration `0011_add_product_constraints.py`.

---

### 16. Unique Constraints on Nested Models
**File:** `backend/catalog/models.py`

Added `unique_together` on `ProductAttribute(product, name)`, `ProductDocument(product, title)`, and conditional unique on `ProductCertification(product, registry)`.

---

## 🚀 UX Transformation (New)

### Phase 1: Vendor Command Center

**New Components:**
- `VendorWorkspaceHeader.vue` — Priority strip + health score + recommendations
- `VendorProductCard.vue` — Operational card with readiness bar and contextual actions

**Changes to `VendorInventorySection.vue`:**
- Replaced raw summary grid with `VendorWorkspaceHeader`
- Replaced `VendorInventoryList` table with grouped operational cards:
  - **Needs Attention**: Low stock, out of stock, incomplete listings
  - **Healthy Listings**: Active, well-stocked, complete
  - **Drafts**: Unpublished products
  - **Hidden**: Disabled or out-of-stock active products
- Added guided empty state with wizard launcher + CSV template CTA
- Added `toggleProductStatus` function for quick enable/disable

**Backend:**
- `GET /v1/products/dashboard-stats/` — Returns catalog aggregation (total, active, draft, low_stock, out_of_stock, with_images, with_certs)
- `GET /v1/quote-requests/unresponded-count/` — Returns count of unresponded quotes for vendor

### Phase 2: Guided Publish Wizard

**Changes to `VendorInventorySection.vue`:**
- New products open in **wizard mode** (editing keeps existing tabs)
- Step indicator: Commercial → Technical → Compliance → Documents → Media → Review
- Real-time readiness meter (0-100%) that updates as fields fill
- Previous / Next navigation buttons
- Review step shows buyer-facing preview + readiness checklist
- `wizardMode` ref toggles between wizard (create) and tab (edit) UX

### Phase 3: Buyer Discovery Trust Signals

**Changes to `ProductDetail.vue`:**
- Added trust strip below product title with:
  - ✅ Verified Supplier badge (when vendor is approved)
  - 📋 Certification count badge
  - ⭐ Featured / 🆕 New Arrival badges
- Added prominent certifications banner in Overview tab with status indicators

### Phase 4: Intelligent Notifications

**New Components:**
- `VendorNotificationPanel.vue` — Inline alert panel with actionable items

**Backend:**
- Added low-stock and out-of-stock notification triggers in `adjust_inventory` action
- `notify_user` call fires WebSocket push to vendor when stock goes critical

**Frontend:**
- `VendorInventorySection` fetches notifications from `/notifications/` and renders them inline
- Notifications show icon, title, message, timestamp, and contextual action button
- Auto-marked as read on interaction

### Phase 5: Operational Timeline

**New Components:**
- `VendorProductTimeline.vue` — Chronological activity feed per product

**Backend:**
- `GET /v1/products/{uuid}/timeline/` — Aggregates events from:
  - Product creation
  - Inventory movements (last 20)
  - Image uploads (last 10)
  - Certifications (last 10)
- Events sorted chronologically with icon, title, description, actor, and timestamp

**Frontend:**
- Timeline opens inside the existing "Inventory Movement History" modal
- Visual vertical timeline with connecting lines and emoji icons

---

## Deployment Notes

- Backend changes require container rebuild and redeploy
- Migration `0011_add_product_constraints.py` must run on PostgreSQL/PostGIS
- No breaking API changes — all new endpoints are additive
- Frontend builds successfully with all new components
- WebSocket notifications already functional; new triggers reuse existing `notify_user` service
