# Phase 1 Buyer Workflow - Quick Reference

## 🚀 Quick Start

### Run the Platform
```bash
cd construction-marketplace
docker-compose up -d
```

- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:8080
- **Django Admin**: http://localhost:8000/admin

### Test Buyer Flow
1. Register at http://localhost:8080/register (role: PROJECT_OWNER)
2. Browse products at http://localhost:8080/
3. Click "Request Quote" on any product
4. Go to http://localhost:8080/buyer/dashboard
5. View quote in "Quotes" tab

---

## 📡 API Quick Reference

### Authentication
```bash
# Register
POST /api/accounts/register/
{
  "email": "buyer@example.com",
  "password": "secure123",
  "role": "PROJECT_OWNER",
  "first_name": "John",
  "last_name": "Doe"
}

# Login
POST /api/accounts/login/
{
  "email": "buyer@example.com",
  "password": "secure123"
}
# Returns: { "token": "abc123...", "user": {...} }
```

### Product Discovery
```bash
# Browse all products
GET /api/v1/products/

# Search
GET /api/v1/products/?search=cement

# Filter by category
GET /api/v1/products/?category__slug=cement

# Filter by region
GET /api/v1/products/?region=NAIROBI

# Combine filters
GET /api/v1/products/?category__slug=steel&region=MOMBASA&search=TMT
```

### Quote & Checkout
```bash
# Create quote request
POST /api/orders/quote-requests/
{}
# Returns: { "id": 1, "status": "REQUESTED", ... }

# Add items (vendor does this, but for testing)
POST /api/orders/quote-requests/1/respond/
{
  "confirmed_price": 5000.00,
  "delivery_fee": 500.00,
  "expires_at": "2026-02-15T00:00:00Z"
}

# Checkout from quote
POST /api/orders/quote-requests/1/checkout/
{
  "response_id": 1
}
# Returns: Order object
```

### Order Management
```bash
# List my orders
GET /api/orders/orders/

# Confirm delivery (buyer)
POST /api/orders/orders/1/confirm_delivery/

# Cancel order (buyer)
POST /api/orders/orders/1/cancel_order/

# Initiate dispute (buyer)
POST /api/orders/orders/1/initiate_dispute/
{
  "reason": "Wrong items delivered"
}
```

### Ratings
```bash
# Rate vendor (after order completion)
POST /api/reviews/ratings/
{
  "order": 1,
  "score": 5,
  "comment": "Excellent service!"
}
```

---

## 🗂️ Database Models

### Key Relationships
```
User (Buyer)
  ├── BuyerProfile (1:1)
  ├── Address (1:N)
  ├── QuoteRequest (1:N)
  └── Order (1:N)
      ├── OrderItem (1:N)
      ├── Payment (1:N)
      └── Rating (1:1)

Product
  ├── Category (N:1)
  └── Vendor (N:1)

Order
  ├── Buyer (N:1)
  ├── Vendor (N:1)
  └── QuoteResponse (1:1, optional)
```

---

## 🎨 Frontend Routes

```javascript
/                      → ProductList (public)
/login                 → Login
/register              → Register
/buyer/dashboard       → BuyerDashboard (auth required)
  ├── Orders tab
  ├── Quotes tab
  ├── Profile tab
  └── Addresses tab
```

---

## 🔐 RBAC Cheat Sheet

### Buyer Permissions
```python
# Can Do
✅ Browse products (anonymous OK)
✅ Request quotes (authenticated)
✅ Checkout from quotes
✅ View own orders
✅ Confirm delivery
✅ Cancel orders (PLACED/CONFIRMED only)
✅ Rate vendors (completed orders)
✅ Initiate disputes

# Cannot Do
❌ View other buyers' orders
❌ Update fulfillment status
❌ Access vendor dashboard
❌ Modify product catalog
❌ Access admin panel
```

---

## 🔄 Order State Machine

```
PLACED ──────────────────────────────────┐
  │                                       │
  │ (vendor confirms)                     │ (buyer/vendor cancels)
  ▼                                       │
CONFIRMED ────────────────────────────────┤
  │                                       │
  │ (vendor packs)                        │
  ▼                                       ▼
PACKING                              CANCELLED
  │
  │ (vendor ships)
  ▼
SHIPPED
  │
  │ (vendor marks delivered)
  ▼
DELIVERED
  │
  │ (buyer confirms)
  ▼
COMPLETED
```

**Buyer Actions**:
- PLACED/CONFIRMED → Can cancel
- DELIVERED → Can confirm delivery
- COMPLETED → Can rate vendor

---

## 🧪 Testing Scenarios

### Scenario 1: Happy Path
```
1. Register as PROJECT_OWNER
2. Browse products, filter by category
3. Request quote for "Dangote Cement"
4. Admin creates vendor response (via Django Admin)
5. Checkout from quote
6. Admin updates order status to DELIVERED
7. Confirm delivery
8. Rate vendor 5 stars
9. Verify vendor metrics updated
```

### Scenario 2: Cancellation
```
1. Create order (via quote checkout)
2. Immediately cancel (status: PLACED)
3. Verify order status → CANCELLED
4. Verify stock restored
```

### Scenario 3: Dispute
```
1. Create order
2. Admin updates to DELIVERED
3. Initiate dispute: "Wrong items"
4. Verify dispute created
5. Admin reviews in Django Admin
```

---

## 🐛 Common Issues & Fixes

### Issue: "Cannot import ContractorReviewSerializer"
**Fix**: Already resolved. Restart frontend if error persists.
```bash
docker-compose restart frontend
```

### Issue: "Pagination warning for unordered QuerySet"
**Fix**: Already resolved. Models have default ordering.

### Issue: "Stock not decrementing"
**Fix**: Ensure checkout endpoint is used (not direct order creation).

### Issue: "Cannot rate order"
**Fix**: Order must be in COMPLETED status. Buyer must be order owner.

---

## 📊 Monitoring

### Check Celery Tasks
```bash
docker-compose logs celery
```

### Check Database
```bash
docker-compose exec backend python manage.py dbshell
SELECT * FROM orders_order ORDER BY created_at DESC LIMIT 5;
```

### Check API Logs
```bash
docker-compose logs backend | grep "POST /api/orders"
```

---

## 🔧 Development Commands

### Create Migrations
```bash
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
```

### Create Superuser
```bash
docker-compose exec backend python manage.py createsuperuser
```

### Django Shell
```bash
docker-compose exec backend python manage.py shell
```

### Run Tests (when implemented)
```bash
docker-compose exec backend python manage.py test
```

---

## 📚 Documentation Index

- **BUYER_WORKFLOW_PHASE1.md** - Complete workflow guide
- **PHASE1_REQUIREMENTS.md** - Requirements tracking
- **IMPLEMENTATION_SUMMARY.md** - High-level overview
- **README.md** - Project setup (if exists)

---

## 🎯 Key Files

### Backend
```
backend/
├── accounts/
│   ├── models.py          # User, BuyerProfile, Address
│   ├── views.py           # ProfileView, AddressViewSet
│   └── serializers.py     # Profile & Address serializers
├── orders/
│   ├── models.py          # Order, QuoteRequest, QuoteResponse
│   ├── views.py           # OrderViewSet, QuoteRequestViewSet
│   ├── tasks.py           # Celery notification tasks
│   └── serializers.py     # Order serializers
├── reviews/
│   ├── models.py          # Rating
│   ├── views.py           # RatingViewSet
│   └── serializers.py     # RatingSerializer
├── rbac/
│   └── permissions.py     # IsBuyer, IsOrderOwner, IsQuoteOwner
└── catalog/
    └── views.py           # ProductViewSet with filters
```

### Frontend
```
frontend/src/
├── views/
│   ├── BuyerDashboard.vue    # Main buyer interface
│   └── ProductList.vue        # Product discovery
├── router/
│   └── index.js               # Route definitions
└── stores/
    └── auth.js                # Authentication state
```

---

## 💡 Pro Tips

1. **Use Django Admin for testing**: Create quote responses manually
2. **Check Celery logs**: Notifications are async, check worker logs
3. **Test with multiple users**: Create PROJECT_OWNER and VENDOR accounts
4. **Use browser DevTools**: Network tab shows all API calls
5. **Read the docs**: BUYER_WORKFLOW_PHASE1.md has detailed flow diagrams

---

## 🆘 Support

**Issues?** Check:
1. Docker containers running: `docker-compose ps`
2. Backend logs: `docker-compose logs backend`
3. Frontend logs: `docker-compose logs frontend`
4. Database migrations: `docker-compose exec backend python manage.py showmigrations`

**Still stuck?** Review the implementation summary or workflow documentation.

---

**Last Updated**: 2026-01-31  
**Version**: 1.0.0  
**Status**: Production Ready
