# Vendor Inventory System

## Purpose

This document defines the current supplier inventory model that is implemented in the repository.

It should be used as the source of truth when refining vendor inventory UX, order reconciliation, or product stock APIs.

## Working model

Vendor inventory is no longer just product CRUD plus a raw `stock_quantity` field.

The implemented system now includes:

- vendor-scoped inventory records via `/api/v1/products/me/`
- product-level stock state with reorder thresholds and computed inventory signals
- inventory movement logging for stock creation, CSV imports, manual adjustments, order commits, and order restocks
- vendor stock-adjustment actions from the inventory workspace
- inventory history per product
- stock restoration when cancellable orders are cancelled

## Stock terminology

- `stock_quantity`: on-hand stock currently recorded against the product
- `available_quantity`: current quantity available for sale in the implemented workflow
- `reorder_level`: low-stock threshold used to derive warning states
- `inventory_signal`: computed state:
  - `IN_STOCK`
  - `LOW_STOCK`
  - `OUT_OF_STOCK`

Current implementation note:

- quote requests do not create stock reservations yet
- availability is enforced at checkout and then committed into the order flow
- because reservations are not yet implemented, `available_quantity` currently mirrors on-hand quantity

## Inventory movements

Inventory movements are recorded in `catalog.ProductInventoryMovement`.

Current movement types:

- `INITIAL`
- `IMPORT`
- `MANUAL_ADJUSTMENT`
- `ORDER_COMMIT`
- `ORDER_RESTOCK`

Each movement records:

- product
- quantity delta
- quantity before
- quantity after
- actor when available
- note
- reference
- created timestamp

## API surface

### Vendor inventory feed

- `GET /api/v1/products/me/`

Returns the authenticated vendor's products with inventory-facing fields including:

- `stock_quantity`
- `available_quantity`
- `inventory_signal`
- `reorder_level`

### Inventory history

- `GET /api/v1/products/{product_uuid}/inventory-history/`

Returns the movement ledger for that product.

### Manual adjustment

- `POST /api/v1/products/{product_uuid}/adjust-inventory/`

Payload:

```json
{
  "quantity_delta": 25,
  "note": "Goods received from warehouse recount",
  "reference": "GRN-448"
}
```

Rules:

- positive values add stock
- negative values remove stock
- the API rejects adjustments that would make stock negative

## Order reconciliation behavior

### Checkout

During quote checkout:

1. stock is validated under transaction lock
2. order items are created with a product reference and snapshots
3. stock is decremented
4. an `ORDER_COMMIT` movement is recorded

### Cancel order

For orders still in `PLACED` or `CONFIRMED`:

1. order cancellation restores stock to the referenced products
2. an `ORDER_RESTOCK` movement is recorded

## Vendor dashboard expectations

The vendor inventory workspace should support:

- list-based inventory scanning, not card-only browsing
- stock-on-hand and available stock visibility
- reorder-threshold visibility
- manual stock adjustment
- product movement history access
- product edit/delete controls
- CSV import for initial catalog loading

## Vendor Approval Enforcement

As of 2026-05-17, all inventory-mutating operations require the vendor to have `verified_status == 'APPROVED'`:

- `POST /api/v1/products/` — Create product
- `POST /api/v1/products/import_products/` — CSV import
- `POST /api/v1/products/{uuid}/upload_images/` — Upload images
- `POST /api/v1/products/{uuid}/upload-documents/` — Upload documents
- `POST /api/v1/products/{uuid}/adjust-inventory/` — Manual stock adjustment

Unapproved (`PENDING`, `REJECTED`, `SUSPENDED`) vendors receive `403 Forbidden` with the message:
> "Vendor account must be approved before publishing materials."

This is enforced via the `VendorApprovedOnly` permission class in `rbac/permissions.py`.

## Remaining gaps

These should still be treated as open follow-up items rather than silently assumed complete:

- quote-stage stock reservation / hold logic
- warehouse or multi-location inventory
- batch / lot tracking
- returns workflow with dedicated return movements
- purchase-order or supplier replenishment workflow
- inventory valuation and cost layers
- image/document deletion from the vendor edit modal
- product comparison workflow
- vendor-facing marketing flag controls (`is_featured`, `is_new_arrival`, `is_on_sale`)
