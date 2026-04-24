# PHASE1_REQUIREMENTS.md

## Construction Marketplace — Phase 1 Requirements (Materials Marketplace)

Phase 1 establishes the core procurement engine, connecting Buyers and Vendors for construction materials.

---

## 1. Actors & Permissions

### Guest
*   **Permissions**: `catalog:view`, `contracts:view`, `projects:view`, `government:view`
*   **Scope**: Public access only. Can browse and search products but cannot initiate transactions.

### Buyer
*   **Permissions**: `catalog:view`, `orders:create`, `orders:view`, `contracts:view`, `projects:view`
*   **Actions**: Can request quotes, place orders, and view order history.
*   **Forbidden**: Cannot list products or manage vendor inventory.

### Vendor
*   **Permissions**: `catalog:create`, `catalog:update`, `catalog:view`, `catalog:manage_stock`, `orders:view`, `orders:process`
*   **Actions**: List products, update pricing, manage stock levels, and fulfill orders.
*   **Enforcement**: Must be flagged as `APPROVED` by an Admin to appear in the public catalog and respond to quote requests.

### Vendor Staff
*   **Permissions**: `catalog:view`, `catalog:manage_stock`, `orders:view`, `orders:process`
*   **Scope**: Scoped to their specific vendor organization.

### Platform Admin
*   **Permissions**: `*:*`
*   **Actions**: Manage all platform settings, verify vendors, moderate reviews, and intervene in disputes.

### Support Agent
*   **Permissions**: `catalog:view`, `orders:view`, `disputes:view`
*   **Scope**: Read-only access to help resolve customer queries.

---

## 2. Requirements & Enforcement

### 2.1 Product Catalog
*   **Enforcement**: Only authenticated users with the `VENDOR` role can create products.
*   **Gating**: Products created by vendors are restricted to their own organization scope.

### 2.2 Ordering Workflow
*   **Enforcement**: Orders require `orders:create` permission.
*   **Validation**: Buyers cannot place orders for their own products (if they hold both roles).

### 2.3 Vendor Verification
*   **Gating**: Vendors who are `PENDING` verification cannot have their products visible to `GUEST` or `BUYER` roles.

---

## 3. Security & Audit

*   **Audit Logging**: Every product price change and order status update must be logged with the Actor ID and Timestamp.
*   **RBAC Enforcement**: All backend ViewSets must enforce `HasRequiredPermission` via logical namespaces.

---

## 4. Vendor Workflow Lifecycle (Implemented)

### 4.1 Onboarding & Governance
* **Onboarding**: Vendors create a user account first, then submit a vendor profile via `POST /api/vendors/`. The frontend path is `/vendors/register`.
* **Moderation**: Admins use the "Vendor Status Queue" in Django Admin to approve/suspend vendors.
* **Gating**: Only `APPROVED` vendors can have `ACTIVE` products visible to the public and can submit quote responses.

### 4.2 Order Fulfillment Pipeline
Orders progress through a strict state machine:
1. `PLACED`: Buyer initiates order.
2. `CONFIRMED`: Vendor accepts and provides `estimated_delivery_at`.
3. `PACKING`: Vendor preparing goods.
4. `SHIPPED`: Goods in transit (tracking number required).
5. `DELIVERED`: Goods at destination.
6. `COMPLETED`: Buyer confirms receipt.

### 4.3 Inventory Management
* **Scope**: Vendor inventory management is scoped to the authenticated vendor via `GET /api/v1/products/me/`.
* **CRUD**: Vendors create products with real material categories and can update or delete only their own records.
* **Bulk Import**: Vendors can import products with `POST /api/v1/products/import_products/` and download the CSV template from `GET /api/v1/products/download_template/`.
* **Adjustment Ledger**: Vendors can adjust inventory with `POST /api/v1/products/{product_uuid}/adjust-inventory/` and inspect movements with `GET /api/v1/products/{product_uuid}/inventory-history/`.
* **Structured Material Data**: Products should support structured certifications, technical attributes, product documents, and richer inventory signals rather than relying only on free-form text fields.
* **Buyer Discovery**: Public product search should expose filters for certification, brand, stock state, region, and special handling to make material comparison faster.
* **Vendor Operations**: Inventory controls should show low-stock warnings, reorder thresholds, movement history, and quick stock-adjustment operations from the vendor workspace.
* **Order Reconciliation**: Checkout should record inventory commits and eligible order cancellation should restore stock.

### 4.4 Performance Monitoring
The platform automatically tracks:
* **Fulfillment Rate**: Ratio of completed to total orders.
* **Cancellation Rate**: Percentage of orders cancelled by vendor.
* **Delivery Timeliness**: Compliance with estimated delivery windows.
