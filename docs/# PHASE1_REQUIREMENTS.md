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
*   **Enforcement**: Must be flagged as `VERIFIED` by an Admin to appear in the public catalog.

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
* **Onboarding**: Vendors register via `/api/vendors/profiles/` and remain `PENDING` until Admin approval.
* **Moderation**: Admins use the "Vendor Status Queue" in Django Admin to approve/suspend vendors.
* **Gating**: Only `APPROVED` vendors can have `ACTIVE` products visible to the public.

### 4.2 Order Fulfillment Pipeline
Orders progress through a strict state machine:
1. `PLACED`: Buyer initiates order.
2. `CONFIRMED`: Vendor accepts and provides delivery estimate.
3. `PACKING`: Vendor preparing goods.
4. `SHIPPED`: Goods in transit (tracking number required).
5. `DELIVERED`: Goods at destination.
6. `COMPLETED`: Buyer confirms receipt.

### 4.3 Performance Monitoring
The platform automatically tracks:
* **Fulfillment Rate**: Ratio of completed to total orders.
* **Cancellation Rate**: Percentage of orders cancelled by vendor.
* **Delivery Timeliness**: Compliance with estimated delivery windows.

---

**Phase 1 vendor workflow fully implemented and integrated.**
