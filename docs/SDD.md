# Software Design Document (SDD)

## Procus v2 — Construction Marketplace Platform

| Field | Value |
|---|---|
| **Document Version** | 2.0 |
| **Status** | Approved |
| **Date** | 21 February 2026 |
| **Prepared by** | Engineering Team |
| **Repository** | https://github.com/nelsonadagi/procusv2 |
| **SRS Reference** | `docs/SRS.md` |

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [System Architecture Overview](#2-system-architecture-overview)
3. [Backend Design](#3-backend-design)
4. [Frontend Design](#4-frontend-design)
5. [Database Design](#5-database-design)
6. [API Design](#6-api-design)
7. [Authentication & Security Design](#7-authentication--security-design)
8. [Async Processing Design](#8-async-processing-design)
9. [Financial Transaction Design](#9-financial-transaction-design)
10. [AI Engine Design](#10-ai-engine-design)
11. [Infrastructure & Deployment Design](#11-infrastructure--deployment-design)
12. [Design Decisions & Trade-offs](#12-design-decisions--trade-offs)

---

## 1. Introduction

### 1.1 Purpose

This Software Design Document (SDD) describes the architecture, component design, data models, and interaction patterns for **Procus v2**. It bridges the requirements specified in the SRS with the actual implementation, giving developers, reviewers, and future maintainers a comprehensive understanding of how the system is built and why.

### 1.2 Scope

This document covers all six delivered phases of the platform:
- Django REST Framework backend (28 Django apps)
- Vue 3 + Vite single-page application (20 views)
- PostgreSQL 15 database schema
- Redis cache and Celery task infrastructure
- Docker Compose orchestration

### 1.3 Design Principles

The following principles governed all design decisions:

| Principle | Application |
|---|---|
| **Domain separation** | Each business domain is an independent Django app |
| **API-first** | All data flows through the REST API — no server-side rendering |
| **Atomic transactions** | All financial operations use database transactions |
| **Role-gated access** | Every endpoint enforces RBAC at the view level |
| **Thin views, fat models** | Business logic lives in models and service functions, not views |
| **Versioned API** | URL namespacing (`/api/v1/` → `/api/v6/`) for backward compatibility |
| **Mobile-first UI** | CSS design token system with responsive breakpoints |

---

## 2. System Architecture Overview

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client Layer                              │
│                                                                  │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │               Vue 3 SPA (Vite, Port 5173)               │   │
│   │   Vue Router │ Pinia Stores │ Axios │ Vanilla CSS        │   │
│   └────────────────────────┬────────────────────────────────┘   │
└────────────────────────────┼────────────────────────────────────┘
                             │ HTTPS / JWT Auth
                             │
┌────────────────────────────┼────────────────────────────────────┐
│                     Application Layer                            │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │         Django REST Framework (Port 8000)                │   │
│   │                                                          │   │
│   │  ViewSets ── Serializers ── Models ── Permissions        │   │
│   │                    │                                     │   │
│   │         28 Domain Apps (Phases 1–6)                       │   │
│   └────────┬───────────────────────────┬────────────────────┘   │
└────────────┼───────────────────────────┼────────────────────────┘
             │                           │
┌────────────▼───────────┐  ┌────────────▼────────────────────────┐
│    Data Layer           │  │      Async Layer                    │
│                         │  │                                      │
│  ┌──────────────────┐   │  │  ┌─────────────┐  ┌─────────────┐  │
│  │  PostgreSQL 15   │   │  │  │    Redis 7  │  │   Celery    │  │
│  │  (Primary DB)    │   │  │  │  (Broker +  │  │   Worker    │  │
│  └──────────────────┘   │  │  │   Cache)    │  │   + Beat    │  │
│                         │  │  └─────────────┘  └─────────────┘  │
└─────────────────────────┘  └─────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────────────────────┐
│                    External Services                             │
│   M-Pesa / Stripe │ SumSub / Onfido │ SAP / Oracle ERP         │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Request Flow

```
Browser
  │
  ├─ Static assets (HTML/JS/CSS) ──▶ Vite Dev Server / CDN
  │
  └─ API call (Axios)
       │
       ├─ [HTTP Request] ──────▶ Django WSGI / ASGI
       │                              │
       │                    ┌─────────▼─────────┐
       │                    │  URL Router        │
       │                    │  /api/v1/.../      │
       │                    └─────────┬─────────┘
       │                              │
       │                    ┌─────────▼─────────┐
       │                    │  JWTAuthentication │
       │                    │  + Permission Check│
       │                    └─────────┬─────────┘
       │                              │
       │                    ┌─────────▼─────────┐
       │                    │  ViewSet / APIView │
       │                    │  (Business Logic)  │
       │                    └─────────┬─────────┘
       │                              │
       │                    ┌─────────▼─────────┐
       │                    │  Serializer        │
       │                    │  (Validation)      │
       │                    └─────────┬─────────┘
       │                              │
       │                    ┌─────────▼─────────┐
       │                    │  Django ORM        │
       │                    │  (PostgreSQL)      │
       │                    └─────────┬─────────┘
       │                              │
       └─ [JSON Response] ◀───────────┘
```

---

## 3. Backend Design

### 3.1 Project Structure

```
backend/
├── config/                  # Django project configuration
│   ├── settings.py          # All settings (env-driven)
│   ├── urls.py              # API v1 root router
│   ├── urls_v2.py → v6.py   # Versioned URL configs
│   ├── celery.py            # Celery app initialisation
│   ├── asgi.py              # ASGI entrypoint
│   └── wsgi.py              # WSGI entrypoint
│
├── [app_name]/              # One directory per domain app
│   ├── models.py            # Database models
│   ├── serializers.py       # DRF serializers
│   ├── views.py             # ViewSets / APIViews
│   ├── urls.py              # App-level URL routing
│   ├── permissions.py       # Custom permission classes
│   ├── admin.py             # Django admin registration
│   ├── tasks.py             # Celery async tasks
│   └── migrations/          # Database migrations
│
├── manage.py
└── requirements.txt
```

### 3.2 Settings Architecture

Settings are entirely environment-driven via `.env`:

```python
# config/settings.py (pattern)
import dj_database_url
import os

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
DEBUG = os.environ.get('DEBUG', '0') == '1'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ['DATABASE_URL']
    )
}

CELERY_BROKER_URL = os.environ['CELERY_BROKER_URL']
CELERY_RESULT_BACKEND = os.environ['CELERY_RESULT_BACKEND']
```

### 3.3 App Registration (28 Apps)

```python
INSTALLED_APPS = [
    # Django internals
    'django.contrib.admin',
    'django.contrib.auth',
    ...

    # Third-party
    'rest_framework',
    'corsheaders',
    'django_filters',

    # Phase 1
    'accounts', 'catalog', 'orders', 'payments',
    'disputes', 'reviews', 'taxonomy',

    # Phase 2
    'contractors', 'contracts', 'bids', 'milestones',

    # Phase 3
    'escrow', 'finance', 'scoring',

    # Phase 4
    'projects', 'property', 'investments',

    # Phase 5
    'regulation', 'enterprise', 'government',
    'compliance', 'risk',

    # Phase 6
    'banking', 'reporting', 'ai_engine',
    'liquidity', 'integrations',

    # Cross-cutting
    'rbac', 'platform_settings',
]
```

### 3.4 URL Versioning Design

API versioning is achieved via URL namespace per phase:

```python
# config/urls.py
urlpatterns = [
    path('api/', include('config.urls')),      # v1 (base)
    path('api/v2/', include('config.urls_v2')),
    path('api/v3/', include('config.urls_v3')),
    path('api/v4/', include('config.urls_v4')),
    path('api/v5/', include('config.urls_v5')),
    path('api/v6/', include('config.urls_v6')),
]
```

Each versioned URL file includes only the routers relevant to that phase's additions.

### 3.5 ViewSet Pattern

All resource views follow DRF's `ModelViewSet` pattern:

```python
class ContractViewSet(ModelViewSet):
    queryset = Contract.objects.select_related('owner').prefetch_related('bids')
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['status', 'location']

    @action(detail=True, methods=['post'])
    def award(self, request, pk=None):
        """Award a specific bid on this contract."""
        # Business logic lives here
        ...
```

### 3.6 Permission Design

Custom permission classes enforce RBAC:

```python
class IsContractor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'CONTRACTOR'

class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user.role == 'ADMIN'
```

### 3.7 Domain App Inventory

| App | Phase | Key Models | Key ViewSets |
|---|---|---|---|
| `accounts` | 1 | `User`, `VendorProfile`, `Address` | `UserViewSet`, `VendorProfileViewSet` |
| `catalog` | 1 | `Product`, `ProductCategory` | `ProductViewSet` |
| `orders` | 1 | `Order`, `OrderItem` | `OrderViewSet` |
| `payments` | 1 | `Payment` | `PaymentViewSet` |
| `disputes` | 1,3 | `Dispute`, `EvidenceSubmission` | `DisputeViewSet` |
| `reviews` | 1 | `Review` | `ReviewViewSet` |
| `taxonomy` | 1 | `TaxonomyCategory` | `CategoryViewSet` |
| `rbac` | 1 | `AuditLog` | `AuditLogViewSet` |
| `platform_settings` | 1 | `PlatformConfig`, `Currency`, `Country` | `PlatformConfigView`, `CurrencyViewSet`, `CountryViewSet` |
| `contractors` | 2 | `Contractor`, `Certification` | `ContractorViewSet` |
| `contracts` | 2 | `Contract` | `ContractViewSet` |
| `bids` | 2 | `Bid` | `BidViewSet` |
| `milestones` | 2 | `Milestone`, `MilestonePayment` | `MilestoneViewSet` |
| `escrow` | 3 | `EscrowAccount`, `EscrowTransaction`, `EscrowRelease`, `EscrowHold` | `EscrowViewSet` |
| `finance` | 3 | `FinanceProduct`, `FinanceApplication` | `FinanceViewSet` |
| `scoring` | 3 | `ReliabilityScore` | `ScoringViewSet` |
| `projects` | 4 | `Project`, `ProjectRequirement`, `ProjectUpdate`, `ProjectContractLink` | `ProjectViewSet` |
| `property` | 4 | `PropertyListing`, `DevelopmentMetadata`, `PropertyProjectLink` | `PropertyViewSet` |
| `investments` | 4 | `InvestmentCommitment` | `InvestmentViewSet` |
| `regulation` | 5 | `InvestorProfile`, `InvestmentAgreement`, `InvestorReport` | `InvestorViewSet`, `AgreementViewSet` |
| `enterprise` | 5 | `Organization`, `ApprovalWorkflow`, `SupplierPerformance` | `OrganizationViewSet` |
| `government` | 5 | `PublicTender`, `AuditLog` (immutable) | `PublicTenderViewSet` |
| `compliance` | 5 | `KYCVerification`, `JurisdictionRule` | `KYCViewSet`, `JurisdictionViewSet` |
| `risk` | 5 | `RiskScore`, `ComplianceAlert` | `RiskViewSet` |
| `banking` | 6 | `BankAccount`, `SettlementTransaction` | `BankingViewSet` |
| `reporting` | 6 | `RegulatoryReport`, `TaxFiling` | `ReportingViewSet` |
| `ai_engine` | 6 | `PredictiveModel`, `UnderwritingPrediction` | `AIViewSet` |
| `liquidity` | 6 | `SecondaryTrade`, `StakeTransfer` | `LiquidityViewSet` |
| `integrations` | 6 | `ERPConnector`, `ExternalSystemSync` | `IntegrationViewSet` |

---

## 4. Frontend Design

### 4.1 Application Structure

```
frontend/src/
│
├── main.js                  # App entry point — mounts Vue, Pinia, Router
├── App.vue                  # Root component — layout shell + router-view
│
├── router/
│   └── index.js             # Route definitions + navigation guards
│
├── stores/
│   └── auth.js              # Pinia store: user state, JWT tokens, login/logout
│
├── services/
│   └── api.js               # Axios instance: base URL, JWT interceptor, refresh
│
├── views/                   # Page-level components (1 per route)
│   ├── Login.vue
│   ├── Register.vue
│   ├── AdminDashboard.vue
│   ├── VendorDashboard.vue
│   ├── BuyerDashboard.vue
│   ├── ContractorDashboard.vue
│   ├── ContractorRegistration.vue
│   ├── InvestorDashboard.vue
│   ├── OwnerDashboard.vue
│   ├── ProductList.vue
│   ├── ProductDetail.vue
│   ├── ProjectList.vue
│   ├── ProjectDetail.vue
│   ├── CreateProject.vue
│   ├── ContractList.vue
│   ├── ContractDetail.vue
│   ├── PostContract.vue
│   ├── ViewTenders.vue
│   ├── SecondaryMarket.vue
│   └── RegulatoryReports.vue
│
├── components/
│   └── ui/                  # Reusable UI primitives
│       ├── Button.vue        # size, variant props (primary/outline/danger)
│       ├── Badge.vue         # variant props (success/warning/primary/secondary)
│       ├── Modal.vue         # isOpen prop + close emit
│       ├── Card.vue          # Generic card container
│       └── ...
│
└── styles/                  # Design system CSS
    ├── tokens.css            # :root { --pz-color-*, --pz-space-* }
    ├── base.css              # Element resets and defaults
    ├── layout.css            # .pz-l-container, .pz-l-grid, .pz-l-flex
    ├── components.css        # .pz-card, .btn, .pz-terminal, etc.
    └── (imported via style.css → main.js)
```

### 4.2 Routing Design

Vue Router uses **hash-free history mode** with role-based navigation guards:

```javascript
// router/index.js
const routes = [
  { path: '/',               component: ProductList },
  { path: '/login',          component: Login },
  { path: '/register',       component: Register },
  { path: '/admin',          component: AdminDashboard,       meta: { role: 'ADMIN' } },
  { path: '/vendor',         component: VendorDashboard,      meta: { role: 'VENDOR' } },
  { path: '/buyer',          component: BuyerDashboard,       meta: { role: 'BUYER' } },
  { path: '/contractor',     component: ContractorDashboard,  meta: { role: 'CONTRACTOR' } },
  { path: '/investor',       component: InvestorDashboard,    meta: { role: 'INVESTOR' } },
  { path: '/owner',          component: OwnerDashboard,       meta: { role: 'PROJECT_OWNER' } },
  // ... shared routes (products, projects, contracts, tenders)
]

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  if (to.meta.role && auth.user?.role !== to.meta.role) {
    next('/login')
  } else {
    next()
  }
})
```

### 4.3 State Management (Pinia)

```javascript
// stores/auth.js
export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,         // { id, email, role, first_name, last_name }
    accessToken: null,
    refreshToken: null,
  }),
  actions: {
    async login(email, password) { ... },
    async logout() { ... },
    async refreshAccessToken() { ... },
  },
  persist: true,        // LocalStorage persistence
})
```

### 4.4 API Service Layer

A single Axios instance handles all API communication with automatic JWT injection and token refresh:

```javascript
// services/api.js
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: { 'Content-Type': 'application/json' }
})

// Inject JWT token on every request
api.interceptors.request.use(config => {
  const auth = useAuthStore()
  if (auth.accessToken) {
    config.headers.Authorization = `Bearer ${auth.accessToken}`
  }
  return config
})

// Auto-refresh on 401
api.interceptors.response.use(null, async error => {
  if (error.response?.status === 401) {
    await auth.refreshAccessToken()
    return api(error.config)  // Retry original request
  }
  return Promise.reject(error)
})
```

### 4.5 Design System Architecture

The CSS design system uses **CSS Custom Properties** (design tokens) as the single source of truth:

```css
/* styles/tokens.css */
:root {
  /* Colour palette */
  --pz-color-primary:         #FF6B2B;   /* Brand orange */
  --pz-color-savanna:         #2ECC71;   /* Success green */
  --pz-color-earth:           #E67E22;   /* Warning amber */
  --pz-color-concrete:        #95A5A6;   /* Muted text */
  --pz-color-limestone-white: #F8F9FA;   /* Background */

  /* Spacing scale (4px base) */
  --pz-space-1:  4px;
  --pz-space-2:  8px;
  --pz-space-4:  16px;
  --pz-space-6:  24px;
  --pz-space-8:  32px;
  --pz-space-12: 48px;
  --pz-space-16: 64px;

  /* Typography */
  --pz-font-mono: 'JetBrains Mono', monospace;
  --pz-font-display: 'Inter', sans-serif;
}
```

Component classes follow a **BEM-inspired** naming convention with the `pz-` prefix:

```
pz-[block]__[element]--[modifier]

Examples:
  .pz-admin-console__sidebar
  .pz-admin-console__sidebar--collapsed
  .pz-side-nav__item--active
  .pz-command-node
  .pz-terminal__line
```

### 4.6 Component API Design

Reusable UI components expose consistent prop interfaces:

```vue
<!-- Button.vue -->
<script setup>
defineProps({
  variant: { type: String, default: 'primary' },  // primary | outline | danger | secondary
  size:    { type: String, default: 'md' },        // sm | md | lg
  disabled: { type: Boolean, default: false },
  type:    { type: String, default: 'button' },
})
</script>

<!-- Badge.vue -->
<script setup>
defineProps({
  variant: { type: String, default: 'primary' },  // primary | success | warning | secondary
})
</script>

<!-- Modal.vue -->
<script setup>
defineProps({
  isOpen: { type: Boolean, required: true },
  title:  { type: String, required: true },
})
defineEmits(['close'])
</script>
```

### 4.7 View Architecture Pattern

Each view follows a consistent pattern:

```
┌────────────────────────────────────────────────┐
│  <template>                                     │
│    Role-specific layout (sidebar + main)        │
│    Tabs / sub-sections                          │
│    Data tables / cards                          │
│    Modals (create/edit)                         │
│  </template>                                    │
│                                                 │
│  <script setup>                                 │
│    ref / computed declarations                  │
│    onMounted → fetchData() (parallel API calls) │
│    Action handlers (CRUD operations)            │
│  </script>                                      │
│                                                 │
│  <style scoped>                                 │
│    Component-specific layout overrides          │
│    Uses design system tokens only               │
│  </style>                                       │
└────────────────────────────────────────────────┘
```

---

## 5. Database Design

### 5.1 Schema Philosophy

- **UUID primary keys** across all financial and identity models
- **Soft deletes** (is_active flag) preferred over hard deletes for user-facing entities
- **Decimal(15,2)** for all monetary amounts
- **Indexed ForeignKeys** for all join-heavy fields
- **`created_at` / `updated_at`** auto-managed timestamps on all models

### 5.2 Core Entity Relationship Diagram

```
accounts_user
    │
    ├── accounts_vendorprofile (1:1)
    │       └── catalog_product (1:N)
    │               └── orders_orderitem (1:N)
    │
    ├── contractors_contractor (1:1)
    │       └── bids_bid (1:N)
    │
    ├── projects_project (1:N, as owner)
    │       ├── projects_requirement (1:N)
    │       ├── projects_update (1:N)
    │       ├── investments_commitment (1:N)
    │       └── projects_contractlink (1:N)
    │
    └── regulation_investorprofile (1:1)
            ├── regulation_investmentagreement (1:N)
            └── liquidity_secondarytrade (1:N, as seller)

orders_order
    ├── payments_payment (1:1)
    └── disputes_dispute (1:1)

contracts_contract
    ├── bids_bid (1:N)
    ├── contracts_milestone (1:N)
    ├── escrow_account (1:1)
    └── projects_contractlink (1:1)

escrow_account
    ├── escrow_transaction (1:N)
    ├── escrow_release (1:N, via milestone)
    └── escrow_hold (1:1, during dispute)
```

### 5.3 Key Model Definitions

#### User Model (`accounts_user`)

```python
class User(AbstractBaseUser, PermissionsMixin):
    id            = UUIDField(primary_key=True, default=uuid4)
    email         = EmailField(unique=True)
    first_name    = CharField(max_length=150)
    last_name     = CharField(max_length=150)
    role          = CharField(choices=ROLE_CHOICES)
    # ROLE_CHOICES: ADMIN, VENDOR, BUYER, CONTRACTOR,
    #               INVESTOR, PROJECT_OWNER, STAFF
    is_active     = BooleanField(default=True)
    date_joined   = DateTimeField(auto_now_add=True)
    updated_at    = DateTimeField(auto_now=True)
```

#### Contract Model (`contracts_contract`)

```python
class Contract(Model):
    id               = UUIDField(primary_key=True)
    owner            = ForeignKey(User, on_delete=PROTECT)
    title            = CharField(max_length=255)
    description_scope = TextField()
    location         = CharField(max_length=255)
    budget_min       = DecimalField(max_digits=15, decimal_places=2)
    budget_max       = DecimalField(max_digits=15, decimal_places=2)
    status           = CharField(choices=[
                         'POSTED','BIDDING','AWARDED',
                         'IN_PROGRESS','COMPLETED','CANCELLED'
                       ])
    created_at       = DateTimeField(auto_now_add=True)
    updated_at       = DateTimeField(auto_now=True)
```

#### EscrowAccount Model (`escrow_escrowaccount`)

```python
class EscrowAccount(Model):
    id                = UUIDField(primary_key=True)
    contract          = OneToOneField(Contract, on_delete=PROTECT)
    buyer             = ForeignKey(User, on_delete=PROTECT)
    total_amount_held = DecimalField(max_digits=15, decimal_places=2)
    currency          = CharField(max_length=10, default='KES')
    status            = CharField(choices=['ACTIVE','RELEASED','CLOSED','FROZEN'])
    created_at        = DateTimeField(auto_now_add=True)
```

#### Platform Settings Models

```python
class PlatformConfig(Model):
    platform_name    = CharField(max_length=255)
    tagline          = CharField(max_length=255, blank=True)
    support_email    = EmailField()
    support_phone    = CharField(max_length=30)
    website          = URLField(blank=True)
    address          = TextField(blank=True)
    default_currency = CharField(max_length=10, default='KES')
    default_region   = CharField(max_length=10, default='KE')
    primary_color    = CharField(max_length=20, default='#FF6B2B')
    secondary_color  = CharField(max_length=20, default='#1A1A2E')
    # Singleton pattern — only one record permitted

class Currency(Model):
    currency_code    = CharField(max_length=10, unique=True)
    currency_name    = CharField(max_length=100)
    symbol           = CharField(max_length=10)
    rate_to_default  = DecimalField(max_digits=15, decimal_places=6)
    is_active        = BooleanField(default=True)

class Country(Model):
    iso_code         = CharField(max_length=3, unique=True)
    name             = CharField(max_length=100)
    flag_emoji       = CharField(max_length=10, blank=True)
    phone_prefix     = CharField(max_length=15)
    default_currency = CharField(max_length=10)
    is_active        = BooleanField(default=True)
    is_default       = BooleanField(default=False)
```

### 5.4 Database Indexes

Critical indexes for query performance:

```python
class Meta:
    indexes = [
        models.Index(fields=['status']),           # Contracts, Orders
        models.Index(fields=['owner']),            # Projects, Contracts
        models.Index(fields=['contractor']),       # Bids
        models.Index(fields=['created_at']),       # AuditLog, Orders
        models.Index(fields=['taxonomy_type']),    # TaxonomyCategory
        models.Index(fields=['is_active']),        # Products, Users, Countries
    ]
```

### 5.5 Migrations Strategy

- Each app maintains its own `migrations/` directory
- Migrations are generated with `python manage.py makemigrations [app_name]`
- Applied collectively with `python manage.py migrate`
- Schema changes requiring data migrations use `RunPython` operations
- Destructive migrations (column drops) require explicit review before deployment

---

## 6. API Design

### 6.1 Design Conventions

| Convention | Implementation |
|---|---|
| **Format** | JSON (`Content-Type: application/json`) |
| **Authentication** | `Authorization: Bearer <JWT>` |
| **Pagination** | `{ count, next, previous, results }` |
| **Errors** | `{ detail: "message" }` or `{ field: ["error"] }` |
| **HTTP Methods** | GET (list/retrieve), POST (create), PUT/PATCH (update), DELETE (destroy) |
| **Filtering** | `?field=value` (django-filter), `?search=term` (SearchFilter) |

### 6.2 API Version Map

| Version | Introduced Apps | Base Path |
|---|---|---|
| v1 | accounts, catalog, orders, payments, disputes, reviews, taxonomy, rbac, platform_settings | `/api/` |
| v2 | contractors, contracts, bids, milestones | `/api/v2/` |
| v3 | escrow, finance, scoring | `/api/v3/` |
| v4 | projects, property, investments | `/api/v4/` |
| v5 | regulation, enterprise, government, compliance, risk | `/api/v5/` |
| v6 | banking, reporting, ai_engine, liquidity, integrations | `/api/v6/` |

### 6.3 Key Endpoint Catalogue

#### Identity & Auth
```
POST   /api/accounts/register/         Register new user
POST   /api/token/                     Obtain JWT pair
POST   /api/token/refresh/             Refresh access token
GET    /api/accounts/management/       List all users (Admin)
POST   /api/config/admin-users/{id}/toggle_active/
POST   /api/config/admin-users/{id}/set_role/
```

#### Materials Marketplace
```
GET    /api/products/                  List products (filterable)
POST   /api/products/                  Create product (Vendor)
GET    /api/products/{id}/             Product detail
PATCH  /api/products/{id}/             Update product
GET    /api/orders/                    List orders
POST   /api/orders/                    Place order (Buyer)
PATCH  /api/orders/{id}/              Update order status (Vendor)
```

#### Contractor & Contracts
```
GET    /api/contractors/               List verified contractors
POST   /api/contractors/register/      Contractor onboarding
GET    /api/contracts/                 List contracts/tenders
POST   /api/contracts/                 Post new tender (Owner)
POST   /api/contracts/{id}/bids/       Submit bid (Contractor)
POST   /api/bids/{id}/award/           Award bid (Owner)
POST   /api/contracts/{id}/milestones/ Create milestone (Owner)
POST   /api/milestones/{id}/approve/   Approve milestone (Owner)
```

#### Escrow & Finance
```
POST   /api/escrow/deposit/            Fund escrow account
POST   /api/escrow-releases/trigger/   Trigger milestone release
GET    /api/disputes/                  List disputes
POST   /api/disputes/                  Open dispute
POST   /api/disputes/{id}/evidence/    Upload evidence
POST   /api/disputes/{id}/resolve/     Admin resolution
GET    /api/finance/products/          List finance products
POST   /api/finance/applications/      Apply for finance
GET    /api/scoring/                   View reliability score
```

#### Projects & Investment
```
GET    /api/projects/                  Project marketplace
POST   /api/projects/                  Create project (Owner)
GET    /api/projects/{id}/             Project detail
POST   /api/projects/{id}/requirements/ Add BoQ item
POST   /api/projects/{id}/commit/      Investor pledge
POST   /api/projects/{id}/link-contract/ Link contract
POST   /api/projects/{id}/updates/     Post update
GET    /api/property/                  Property listings
POST   /api/property/                  List property
```

#### Platform Admin
```
GET    /api/config/platform/           Get platform config
PATCH  /api/config/platform/           Update platform config
GET    /api/config/currencies/         List currencies
POST   /api/config/currencies/         Add currency
PATCH  /api/config/currencies/{id}/    Update currency rate
DELETE /api/config/currencies/{id}/    Remove currency
GET    /api/config/countries/          List countries
POST   /api/config/countries/          Add country
POST   /api/config/countries/{id}/set_default/
GET    /api/config/roles/              List roles/groups
POST   /api/config/roles/             Create role
DELETE /api/config/roles/{id}/         Delete role
GET    /api/rbac/audit-logs/           Audit log stream
GET    /api/taxonomy/categories/       List taxonomy
POST   /api/taxonomy/categories/       Add category
```

---

## 7. Authentication & Security Design

### 7.1 JWT Token Flow

```
Client                          Server
  │                               │
  ├── POST /api/token/             │
  │   { email, password }         │
  │                               ├── Validate credentials
  │                               ├── Issue access token (exp: 5min)
  │                               └── Issue refresh token (exp: 7 days)
  │◄─ { access, refresh } ────────┤
  │                               │
  ├── GET /api/resource/          │
  │   Authorization: Bearer <AT>  │
  │                               ├── Decode & verify AT
  │                               ├── Load user from AT claims
  │◄─ { data }  ──────────────────┤
  │                               │
  │ (AT expired)                  │
  ├── POST /api/token/refresh/    │
  │   { refresh: <RT> }           │
  │                               ├── Verify RT
  │◄─ { access: <new_AT> } ───────┤
```

### 7.2 RBAC Design

```
User.role ──▶ Custom Permission Class ──▶ Allow / Deny

Role Matrix:
┌─────────────┬───────┬────────┬──────────┬──────────────┬──────────┬──────────┐
│ Resource    │ Admin │ Vendor │   Buyer  │ Contractor   │  Owner   │ Investor │
├─────────────┼───────┼────────┼──────────┼──────────────┼──────────┼──────────┤
│ All Users   │  RW   │   -    │    -     │     -        │    -     │    -     │
│ Platform    │  RW   │   -    │    -     │     -        │    -     │    -     │
│ Products    │  RW   │  RW    │    R     │     R        │    R     │    R     │
│ Orders      │  RW   │  RW    │   RW     │     -        │    -     │    -     │
│ Contracts   │  RW   │   -    │    -     │    RW        │   RW     │    R     │
│ Bids        │  RW   │   -    │    -     │    RW        │    R     │    -     │
│ Projects    │  RW   │   -    │    -     │     R        │   RW     │    R     │
│ Escrow      │  RW   │   -    │    -     │     -        │   RW     │    -     │
│ Investments │  RW   │   -    │    -     │     -        │    -     │   RW     │
│ Reports     │   R   │   -    │    -     │     -        │    -     │    -     │
└─────────────┴───────┴────────┴──────────┴──────────────┴──────────┴──────────┘
R = Read, W = Write, - = No Access
```

### 7.3 Audit Log Design

All sensitive operations are captured by the RBAC audit system:

```python
class AuditLog(Model):
    id            = UUIDField(primary_key=True)
    actor         = ForeignKey(User, on_delete=SET_NULL, null=True)
    actor_name    = CharField(max_length=255)  # Denormalised for log integrity
    action        = CharField(max_length=100)  # 'CREATE', 'UPDATE', 'DELETE', 'APPROVE'
    resource_type = CharField(max_length=100)  # 'Contract', 'Bid', 'EscrowRelease'
    resource_id   = CharField(max_length=50)
    metadata      = JSONField(null=True)       # Before/after values
    timestamp     = DateTimeField(auto_now_add=True)
    ip_address    = GenericIPAddressField(null=True)

    class Meta:
        ordering = ['-timestamp']
        indexes  = [Index(fields=['-timestamp']), Index(fields=['actor'])]
```

Audit logging is triggered via Django signals on model `save()` and `delete()` events.

---

## 8. Async Processing Design

### 8.1 Celery Architecture

```
Django App ──► redis://redis:6379/0 (Broker) ──► Celery Worker
                                                      │
                                              ┌───────▼───────┐
                                              │ Task Execution │
                                              │  • Email send  │
                                              │  • Report gen  │
                                              │  • AI scoring  │
                                              │  • ERP sync    │
                                              └───────────────┘

Celery Beat ──► Scheduled Tasks (cron-like)
                  • Daily regulatory reports
                  • Reliability score recalculation
                  • Secondary market settlement
```

### 8.2 Task Registry

| Task | Trigger | Description |
|---|---|---|
| `send_bid_notification` | Bid submitted | Notify contract owner |
| `send_milestone_approval` | Milestone approved | Notify contractor |
| `calculate_reliability_score` | Contract completed | Update contractor score |
| `generate_regulatory_report` | Daily (Beat) | AML/SAR/Tax report generation |
| `sync_erp_data` | On demand | Push data to SAP/Oracle connector |
| `run_ai_prediction` | Finance application | Underwriting prediction |

### 8.3 Celery Configuration

```python
# config/celery.py
app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'generate-daily-report': {
        'task': 'reporting.tasks.generate_regulatory_report',
        'schedule': crontab(hour=2, minute=0),  # 02:00 daily
    },
    'recalculate-scores': {
        'task': 'scoring.tasks.batch_recalculate_scores',
        'schedule': crontab(hour=3, minute=0),  # 03:00 daily
    },
}
```

---

## 9. Financial Transaction Design

### 9.1 Critical Design Decisions

All escrow operations use **database-level transactions** to guarantee atomicity:

```python
from django.db import transaction

@transaction.atomic
def release_milestone_funds(milestone_id):
    """
    Atomically release escrow funds for an approved milestone.
    Rolls back entirely if any step fails.
    """
    milestone  = Milestone.objects.select_for_update().get(id=milestone_id)
    escrow     = EscrowAccount.objects.select_for_update().get(
                     contract=milestone.contract,
                     status='ACTIVE'
                 )

    # Guard: must not be frozen
    if EscrowHold.objects.filter(escrow_account=escrow).exists():
        raise ValidationError("Escrow is frozen due to an open dispute.")

    # Guard: sufficient funds
    if escrow.total_amount_held < milestone.amount:
        raise ValidationError("Insufficient escrow balance.")

    # Deduct funds
    escrow.total_amount_held -= milestone.amount
    escrow.save()

    # Create ledger entry
    EscrowTransaction.objects.create(
        escrow_account=escrow,
        type='RELEASE',
        amount=milestone.amount,
        milestone=milestone,
    )

    # Create release record
    EscrowRelease.objects.create(
        milestone=milestone,
        released_amount=milestone.amount,
        release_status='COMPLETED',
    )

    # Update milestone
    milestone.status = 'PAID'
    milestone.save()
```

### 9.2 Dispute Flow

```
Owner or Contractor opens Dispute
         │
         ▼
Dispute created (status: OPENED)
         │
         ▼
EscrowHold created → EscrowAccount.status = FROZEN
         │
         ▼
Admin reviews dispute → UNDER_REVIEW
         │
    ┌────┴────┐
    │         │
    ▼         ▼
RELEASE    REFUND
(to Ctr)   (to Owner)
    │         │
    └────┬────┘
         ▼
EscrowHold removed
EscrowAccount.status = ACTIVE (or CLOSED)
Dispute.status = RESOLVED_RELEASE / RESOLVED_REFUND
```

---

## 10. AI Engine Design

### 10.1 Architecture

```
Finance Application
        │
        ├── Feature Extraction ──▶ { credit_history, milestones_completed,
        │                            disputes_count, reliability_score, ... }
        │
        ├── POST /api/v6/ai-predictions/predict-default/
        │
        ▼
   AI Engine (ai_engine app)
        │
        ├── Load PredictiveModel from registry
        ├── Run inference ──▶ default_probability (0.0 – 1.0)
        │
        └── Create UnderwritingPrediction record
                │
                ▼
       Finance Application
          │
          ├── probability < 0.3 ──▶ AUTO_APPROVE
          ├── probability 0.3–0.7 ──▶ MANUAL_REVIEW
          └── probability > 0.7 ──▶ AUTO_REJECT
```

### 10.2 Data Models

```python
class PredictiveModel(Model):
    id           = UUIDField(primary_key=True)
    name         = CharField(max_length=255)
    version      = CharField(max_length=50)
    model_type   = CharField()          # 'DEFAULT_PREDICTION', 'FRAUD_DETECTION'
    artifact_url = URLField()           # Path to serialised model file
    is_active    = BooleanField()
    trained_at   = DateTimeField()

class UnderwritingPrediction(Model):
    id                  = UUIDField(primary_key=True)
    application         = ForeignKey(FinanceApplication, on_delete=PROTECT)
    model               = ForeignKey(PredictiveModel, on_delete=PROTECT)
    default_probability = DecimalField(max_digits=5, decimal_places=4)
    decision            = CharField()   # AUTO_APPROVE | MANUAL_REVIEW | AUTO_REJECT
    created_at          = DateTimeField(auto_now_add=True)
```

---

## 11. Infrastructure & Deployment Design

### 11.1 Docker Compose Service Map

```yaml
services:
  backend:        # Django + Gunicorn/runserver
  frontend:       # Vue 3 + Vite dev server
  postgres:       # PostgreSQL 15
  redis:          # Redis 7
  celery-worker:  # Celery task consumer
  celery-beat:    # Celery scheduled task scheduler

networks:
  marketplace-net:  # All services on shared internal network

volumes:
  postgres-data:    # Persistent PostgreSQL data
```

### 11.2 Service Dependencies

```
postgres ◄── backend
             ▲
redis    ◄───┤
             ├── celery-worker
             └── celery-beat

frontend ──► backend (API calls via VITE_API_URL)
```

### 11.3 Environment Configuration Reference

| Variable | Service | Required | Default |
|---|---|---|---|
| `DATABASE_URL` | backend, celery | ✅ | — |
| `REDIS_URL` | backend, celery | ✅ | — |
| `CELERY_BROKER_URL` | celery | ✅ | — |
| `CELERY_RESULT_BACKEND` | celery | ✅ | — |
| `DJANGO_SECRET_KEY` | backend | ✅ | — |
| `DEBUG` | backend | — | `0` |
| `ALLOWED_HOSTS` | backend | — | `*` |
| `PAYMENT_PROVIDER_KEYS` | backend | — | — |
| `VITE_API_URL` | frontend | — | `http://localhost:8000/api` |

### 11.4 Production Deployment Checklist

```
☐ Set DEBUG=0
☐ Set ALLOWED_HOSTS to production domain(s)
☐ Generate a new DJANGO_SECRET_KEY (50+ random chars)
☐ Use a managed PostgreSQL instance (not SQLite)
☐ Enable PostgreSQL SSL connection
☐ Configure Redis with password authentication
☐ Serve Django via Gunicorn (not runserver)
☐ Serve frontend via Nginx (pre-built static files)
☐ Enable HTTPS (TLS certificate via Let's Encrypt)
☐ Configure CORS_ALLOWED_ORIGINS to production domain
☐ Set up automated PostgreSQL backups
☐ Configure Celery with supervisord or systemd
☐ Enable application performance monitoring (APM)
```

---

## 12. Design Decisions & Trade-offs

### 12.1 Why Django REST Framework?

**Decision:** Use DRF over FastAPI or Flask.

**Rationale:**
- Mature ORM with complex relation support required by the domain model
- Built-in admin for rapid prototype configuration
- Django's migration system is battle-tested for evolving schemas
- DRF's serializer/viewset pattern reduces boilerplate for CRUD-heavy domains

**Trade-off:** DRF is synchronous by default; async operations delegated to Celery.

---

### 12.2 Why Vue 3 + Vite over React/Next.js?

**Decision:** Use Vue 3 with Vite SPA over a React framework.

**Rationale:**
- `<script setup>` composition API reduces boilerplate while remaining readable
- Pinia provides simpler, more ergonomic state than Redux
- Vite's HMR is significantly faster than webpack-based setups
- Vue's reactivity model aligns well with form-heavy dashboard UIs

**Trade-off:** Smaller ecosystem than React; less third-party component library choice.

---

### 12.3 Why Custom Vanilla CSS over Tailwind?

**Decision:** Build a custom CSS design system using CSS custom properties.

**Rationale:**
- Full control over every design token without framework constraints
- No build-time purge/scan complexity
- Enforces deliberate, semantic class naming (prevents utility soup)
- Design tokens can be dynamically overridden (future white-labelling requirement)

**Trade-off:** Higher initial setup cost; requires team CSS discipline.

---

### 12.4 Why API Versioning via URL Namespace?

**Decision:** Use URL-based versioning (`/api/v1/` → `/api/v6/`) rather than headers.

**Rationale:**
- URL versioning is visible, debuggable, and cacheable
- Enables gradual phase introduction without breaking existing clients
- Simpler to implement with DRF routers
- Mirrors the phase-based development roadmap

**Trade-off:** URL proliferation; clients must track which version exposes which resource.

---

### 12.5 Why Atomic Transactions for Financial Operations?

**Decision:** Wrap all escrow operations in `@transaction.atomic` with `select_for_update()`.

**Rationale:**
- Prevents double-spend in concurrent milestone approval scenario
- PostgreSQL row-level locking (`select_for_update`) prevents race conditions
- Database-level atomicity is more reliable than application-level checks

**Trade-off:** Reduced write throughput under heavy concurrent load; mitigated by connection pooling.

---

*End of SDD — Procus v2 v2.0 · 21 February 2026*
