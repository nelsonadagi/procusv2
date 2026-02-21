# Phase 1 Buyer Workflow - Complete Implementation

## Overview
This document details the complete end-to-end buyer workflow implemented for Phase 1 of the Ujenzi Construction Marketplace.

## 1. Buyer Onboarding & Profile Management

### Account Creation
- **Endpoint**: `POST /api/accounts/register/`
- **Roles**: Buyers register as `PROJECT_OWNER` or `CONTRACTOR`
- **Authentication**: Token-based authentication via DRF

### Profile Management
- **Endpoint**: `GET/PATCH /api/accounts/profile/`
- **Features**:
  - Personal information (name, email, phone)
  - Preferred region for deliveries
  - Delivery instructions
  - Order history access

### Address Management
- **Endpoints**: 
  - `GET /api/accounts/addresses/` - List all addresses
  - `POST /api/accounts/addresses/` - Add new address
  - `PATCH /api/accounts/addresses/{id}/` - Update address
  - `DELETE /api/accounts/addresses/{id}/` - Remove address
- **Features**:
  - Multiple delivery locations
  - Default address selection
  - Site-specific addresses (e.g., "Construction Site A")

## 2. Product Discovery & Marketplace Browsing

### Catalog Access
- **Endpoint**: `GET /api/v1/products/`
- **Public Access**: Anonymous users can browse active products
- **Filtering Options**:
  - By category: `?category__slug=cement`
  - By region: `?region=NAIROBI`
  - By vendor: `?vendor=1`
  - By status: `?status=ACTIVE`

### Search Functionality
- **Full-text search**: `?search=dangote cement`
- **Fields searched**: Product name, description, vendor name

### Sorting
- **Price**: `?ordering=base_price` or `?ordering=-base_price`
- **Recent**: `?ordering=-created_at`

### Product Display
Each product shows:
- Vendor name with verification badge
- Stock status
- Unit pricing
- Minimum order quantity
- Delivery regions
- Category taxonomy

## 3. Quote Request Workflow (Recommended for Construction)

### Step 1: Request Quote
- **Endpoint**: `POST /api/orders/quote-requests/`
- **Process**:
  1. Buyer creates quote request
  2. Adds items with quantities
  3. System notifies relevant vendors

### Step 2: Vendor Response
- **Endpoint**: `POST /api/orders/quote-requests/{id}/respond/`
- **Vendor provides**:
  - Confirmed price
  - Delivery fee
  - Expiration date
  - Availability confirmation

### Step 3: Buyer Checkout
- **Endpoint**: `POST /api/orders/quote-requests/{id}/checkout/`
- **Process**:
  1. Buyer selects vendor response
  2. System validates stock availability
  3. Creates order with line items
  4. Decrements product stock
  5. Creates payment intent (placeholder)
  6. Triggers vendor notification

## 4. Order Lifecycle Tracking

### Order States
```
PLACED → CONFIRMED → PACKING → SHIPPED → DELIVERED → COMPLETED
                                                    ↓
                                              CANCELLED
```

### State Transitions
- **PLACED**: Order created, awaiting vendor confirmation
- **CONFIRMED**: Vendor accepted, preparing order
- **PACKING**: Items being prepared for shipment
- **SHIPPED**: Order dispatched with tracking number
- **DELIVERED**: Order arrived at delivery location
- **COMPLETED**: Buyer confirmed receipt
- **CANCELLED**: Order cancelled (only from PLACED/CONFIRMED)

### Buyer Actions by State

#### PLACED/CONFIRMED
- **Cancel Order**: `POST /api/orders/orders/{id}/cancel_order/`
- **Initiate Dispute**: `POST /api/orders/orders/{id}/initiate_dispute/`

#### DELIVERED
- **Confirm Delivery**: `POST /api/orders/orders/{id}/confirm_delivery/`
  - Marks order as COMPLETED
  - Triggers vendor performance update
  - Enables rating/review

#### COMPLETED
- **Rate Vendor**: `POST /api/reviews/ratings/`
  - Score: 1-5 stars
  - Optional comment
  - Updates vendor average_rating
  - Feeds into vendor performance metrics

## 5. Payment Integration (Phase 1 Placeholder)

### Payment Model
```python
class Payment:
    order: ForeignKey
    provider: str  # 'MODERN_CHECKOUT', 'MPESA', 'STRIPE'
    amount: Decimal
    status: UNPAID | PENDING | PAID | FAILED
    transaction_reference: str
    paid_at: DateTime
```

### Payment Flow
1. Order created with `payment_status='UNPAID'`
2. Payment intent created with `status='PENDING'`
3. **Phase 1**: Manual status update via admin
4. **Phase 3+**: Gateway integration (M-Pesa, Stripe)

### Payment Validation
- Orders cannot proceed to fulfillment without payment confirmation
- Buyers can view payment status in dashboard
- Admins can update payment status via Django Admin

## 6. Buyer Notifications (Celery Tasks)

### Implemented Notifications
```python
# Order placed
notify_vendor_new_order.delay(order_id)

# Vendor confirmed order
notify_buyer_order_confirmed.delay(order_id)

# Delivery updates
notify_delivery_update.delay(order_id, status)
```

### Notification Channels
- **Phase 1**: Email (via Django email backend)
- **Phase 2+**: SMS, WhatsApp via MessagingGatewayConfig

## 7. Dispute & Cancellation System

### Cancellation Rules
- **Allowed States**: PLACED, CONFIRMED
- **Endpoint**: `POST /api/orders/orders/{id}/cancel_order/`
- **Process**:
  - Order status → CANCELLED
  - Audit log created
  - Stock restored (if deducted)

### Dispute Triggers
- **Endpoint**: `POST /api/orders/orders/{id}/initiate_dispute/`
- **Valid Reasons**:
  - Vendor failed to ship
  - Wrong items delivered
  - Damaged goods
  - Quality issues

### Dispute Model
```python
class Dispute:
    opened_by: User
    order: Order
    status: OPENED | UNDER_REVIEW | RESOLVED_RELEASE | RESOLVED_REFUND | CLOSED
    reason: TextField
    created_at: DateTime
```

### Escalation
- Disputes escalate to admin moderation
- Admins view via Django Admin
- Evidence submission supported (Phase 2)

## 8. RBAC Enforcement

### Buyer Permissions
```python
class IsBuyer(BasePermission):
    """PROJECT_OWNER and CONTRACTOR can act as buyers"""
    def has_permission(self, request, view):
        return request.user.role in ['PROJECT_OWNER', 'CONTRACTOR', 'ADMIN']

class IsOrderOwner(BasePermission):
    """User is buyer or vendor of the order"""
    def has_object_permission(self, request, view, obj):
        return obj.buyer == request.user or 
               (hasattr(request.user, 'vendor_profile') and 
                obj.vendor == request.user.vendor_profile)
```

### Access Controls
- ✅ Buyers can browse products (anonymous allowed)
- ✅ Buyers can place orders (authenticated only)
- ✅ Buyers can track their own orders only
- ✅ Buyers can open disputes on their orders
- ❌ Buyers cannot access vendor dashboards
- ❌ Buyers cannot modify fulfillment states
- ❌ Buyers cannot view other buyers' orders
- ❌ Buyers cannot access admin controls

## 9. Vendor Performance & Trust Signals

### Performance Metrics
```python
class Vendor:
    fulfillment_rate: Float  # % of completed orders
    cancellation_rate: Float  # % of cancelled orders
    delivery_timeliness: Float  # % on-time deliveries
    average_rating: Float  # Average buyer rating (1-5)
    total_reviews: Integer  # Number of ratings
```

### Metric Updates
- **Trigger**: Order completion, rating submission
- **Method**: Async Celery task `update_vendor_performance_metrics.delay(vendor_id)`
- **Calculation**:
  ```python
  fulfillment_rate = (completed_orders / total_orders) * 100
  cancellation_rate = (cancelled_orders / total_orders) * 100
  average_rating = AVG(ratings.score)
  ```

### Rating System
- **Endpoint**: `POST /api/reviews/ratings/`
- **Validation**:
  - Only order buyer can rate
  - Only completed orders can be rated
  - One rating per order
- **Impact**: Feeds vendor trust score for future underwriting (Phase 4+)

## 10. Frontend Implementation

### Buyer Dashboard (`/buyer/dashboard`)
**Tabs**:
- **Orders**: Track all purchases with status
- **Quotes**: View quote requests and vendor responses
- **Profile**: Update personal information
- **Addresses**: Manage delivery locations
- **Disputes**: View open disputes (future)

**Key Features**:
- Confirm delivery button (DELIVERED → COMPLETED)
- Rate vendor modal (post-completion)
- Cancel order (PLACED/CONFIRMED only)
- Initiate dispute
- Checkout from quote responses

### Product Listing (`/`)
**Features**:
- Search bar with real-time filtering
- Category dropdown (from taxonomy)
- Region filter
- "Request Quote" button per product
- Anonymous browsing enabled

## 11. API Endpoints Summary

### Accounts
- `POST /api/accounts/register/` - Register buyer
- `POST /api/accounts/login/` - Login
- `GET/PATCH /api/accounts/profile/` - Manage profile
- `GET/POST /api/accounts/addresses/` - Manage addresses

### Catalog
- `GET /api/v1/products/` - Browse products (public)
- `GET /api/v1/products/{id}/` - Product detail

### Orders
- `POST /api/orders/quote-requests/` - Create quote request
- `GET /api/orders/quote-requests/` - List buyer's quotes
- `POST /api/orders/quote-requests/{id}/checkout/` - Convert quote to order
- `GET /api/orders/orders/` - List buyer's orders
- `POST /api/orders/orders/{id}/confirm_delivery/` - Confirm delivery
- `POST /api/orders/orders/{id}/cancel_order/` - Cancel order
- `POST /api/orders/orders/{id}/initiate_dispute/` - Open dispute

### Reviews
- `POST /api/reviews/ratings/` - Rate vendor after completion

## 12. Testing Checklist

### Buyer Registration
- [ ] Register as PROJECT_OWNER
- [ ] Register as CONTRACTOR
- [ ] Login with email
- [ ] View profile

### Product Discovery
- [ ] Browse products anonymously
- [ ] Search for products
- [ ] Filter by category
- [ ] Filter by region
- [ ] View product details

### Quote & Checkout
- [ ] Request quote for product
- [ ] Vendor responds to quote
- [ ] Buyer checks out from quote
- [ ] Stock decrements correctly
- [ ] Payment intent created

### Order Tracking
- [ ] View order in dashboard
- [ ] Vendor updates to CONFIRMED
- [ ] Vendor updates to SHIPPED
- [ ] Vendor updates to DELIVERED
- [ ] Buyer confirms delivery
- [ ] Order status → COMPLETED

### Ratings
- [ ] Rate vendor after completion
- [ ] Vendor metrics updated
- [ ] Cannot rate incomplete order
- [ ] Cannot rate twice

### Cancellation & Disputes
- [ ] Cancel order in PLACED state
- [ ] Cancel order in CONFIRMED state
- [ ] Cannot cancel SHIPPED order
- [ ] Open dispute on order
- [ ] Dispute visible to admin

## 13. Known Limitations (Phase 1)

1. **Payment**: Placeholder only, no gateway integration
2. **Notifications**: Email only, no SMS/WhatsApp
3. **Dispute Resolution**: Admin manual review only
4. **Stock Management**: Basic decrement, no reservation system
5. **Delivery Tracking**: Manual updates, no carrier integration
6. **Bulk Orders**: Single-vendor quotes only
7. **Price Negotiation**: Fixed quote response, no counter-offers

## 14. Next Steps (Phase 2+)

1. **Escrow Integration**: Secure payment holding
2. **Real Payment Gateways**: M-Pesa, Stripe, Flutterwave
3. **Advanced Notifications**: SMS, WhatsApp, Push
4. **Delivery Tracking**: Carrier API integration
5. **Multi-vendor Quotes**: Compare multiple responses
6. **Automated Dispute Resolution**: Evidence upload, timeline tracking
7. **Buyer Analytics**: Spending patterns, procurement insights

---

**Status**: ✅ Phase 1 Buyer Workflow Complete
**Last Updated**: 2026-01-31
**Maintainer**: Ujenzi Engineering Team
