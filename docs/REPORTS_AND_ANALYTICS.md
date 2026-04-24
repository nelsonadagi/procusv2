# Reports & Analytics

## Overview

The admin Reports dashboard provides comprehensive business intelligence and analytics for the Ujenzi Marketplace platform. It aggregates data across all marketplace modules — orders, vendors, contractors, projects, properties, payments, disputes, compliance, and more — into interactive visual dashboards.

---

## Architecture

### Backend

- **Module:** `backend/reporting/analytics.py`
- **ViewSet:** `AnalyticsViewSet` (`backend/reporting/views.py`)
- **URL Prefix:** `/api/v6/analytics/`
- **Permission:** `AdminOnly` — accessible only to staff, superusers, and users with `ADMIN` role

All aggregation is performed server-side using Django ORM (`annotate`, `aggregate`, `TruncDate`) for efficient database queries. No client-side computation is required.

### Frontend

- **Entry Component:** `frontend/src/components/admin/ReportsSection.vue`
- **Charting Library:** `vue3-apexcharts` (ApexCharts)
- **Integration:** Mounted as the `reports` tab inside `AdminDashboard.vue`

---

## API Endpoints

All endpoints accept an optional `?days=N` query parameter (default: 30) to scope time-windowed metrics.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v6/analytics/summary/` | GET | High-level KPIs (users, orders, revenue, vendors, properties, disputes, KYC) |
| `/api/v6/analytics/financial/` | GET | Revenue trends, payment status breakdown, AOV |
| `/api/v6/analytics/marketplace/` | GET | Order funnel, top products, vendor leaderboard, product status, low-stock alerts |
| `/api/v6/analytics/users/` | GET | Role distribution, signup trend, activation status |
| `/api/v6/analytics/operations/` | GET | KYC pipeline, dispute status, contract/project/contractor status |
| `/api/v6/analytics/property/` | GET | Real estate listing status, asset types, inquiry/appointment analytics |
| `/api/v6/analytics/geographic/` | GET | Geo-coordinates for vendors, projects, properties, and orders (for mapping) |

### Example Response: `/api/v6/analytics/summary/?days=30`

```json
{
  "users": { "total": 1250, "new": 45 },
  "orders": { "total": 3420, "new": 128 },
  "revenue": { "total": 15400000.00, "period": 1280000.00 },
  "vendors": { "total": 87, "approved": 62 },
  "properties": { "total": 340, "active": 210 },
  "disputes": { "total": 24, "open": 3 },
  "projects": 56,
  "contracts": 128,
  "pending_kyc": 12,
  "period_days": 30
}
```

---

## Dashboard Tabs

### 1. Overview
Executive summary with KPI command nodes and trend charts:
- Total users, orders, revenue (all-time + period)
- Vendor and property counts
- Open disputes and pending KYC alerts
- Order trend (area chart)
- Revenue trend (area chart)

### 2. Financial
Monetary performance analytics:
- Period revenue and Average Order Value (AOV)
- Daily revenue bar chart
- Payment status donut chart (PAID, PENDING, FAILED, UNPAID)

### 3. Marketplace
Transaction and product insights:
- Order lifecycle funnel (PLACED → COMPLETED)
- Product status distribution
- Top 10 products by quantity sold and revenue
- Vendor leaderboard (orders, rating, fulfillment rate)
- Low stock alerts table

### 4. Users
Platform growth and demographics:
- User role distribution donut chart
- Daily signup trend area chart
- Active vs inactive user pie chart
- Role breakdown table

### 5. Operations
Operational pipeline health:
- KYC verification status bar chart
- Dispute status donut chart
- Contract status pie chart
- Project status pie chart
- Contractor verification status pie chart

### 6. Real Estate
Property marketplace performance:
- Listing status donut chart
- Asset type distribution pie chart
- Inquiry trend area chart
- Appointment status bar chart

### 7. Geographic
Spatial intelligence summary:
- Entity count by type (vendors, projects, properties, orders)
- Coverage summary table with mapped entity counts
- Intended for future Leaflet map integration

### 8. Regulatory
Existing compliance reporting surface:
- Regulatory report listing (AML, VAT, Audit)
- Submission status tracking
- JSON export per report

---

## Date Range Filtering

All time-series dashboards support a global date range selector:
- **7D** — Last 7 days
- **30D** — Last 30 days (default)
- **90D** — Last 90 days
- **1Y** — Last 365 days

The selector is located in the Reports header and refreshes all active data when changed.

---

## Chart Types Used

| Chart Type | Used For |
|------------|----------|
| Area | Trends over time (orders, revenue, signups, inquiries) |
| Bar | Comparisons (appointments, entity counts) |
| Horizontal Bar | Funnels and pipelines (order status, KYC) |
| Donut | Proportional breakdowns (payments, disputes, roles, listings) |
| Pie | Status distributions (products, contracts, projects, contractors, asset types) |

---

## File Reference

### Backend
- `backend/reporting/analytics.py` — Aggregation logic
- `backend/reporting/views.py` — `AnalyticsViewSet`
- `backend/config/urls_v6.py` — Route registration

### Frontend
- `frontend/src/components/admin/ReportsSection.vue` — Main dashboard component
- `frontend/src/views/AdminDashboard.vue` — Admin shell (tab navigation)
- `frontend/src/main.js` — ApexCharts plugin registration

---

## Adding New Reports

1. **Backend:** Add a new function in `backend/reporting/analytics.py` and expose it via an `@action` in `AnalyticsViewSet`.
2. **Frontend:** Add a new sub-tab in `ReportsSection.vue`, fetch the endpoint, and render the chart/table.
3. **Documentation:** Update this file and `ADMIN_FUNCTIONALITY_STATUS.md`.
