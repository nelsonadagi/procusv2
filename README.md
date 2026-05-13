# 🏗️ Procus v2 — Construction Marketplace Platform

> A full-stack, multi-role construction industry marketplace connecting **Vendors**, **Contractors**, **Buyers**, **Investors**, and **Project Owners** on a single platform — powered by Django REST Framework and Vue 3.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-092E20?style=flat-square&logo=django)](https://www.djangoproject.com/)
[![Vue.js](https://img.shields.io/badge/Vue-3.x-4FC08D?style=flat-square&logo=vue.js)](https://vuejs.org/)
[![Vite](https://img.shields.io/badge/Vite-7.x-646CFF?style=flat-square&logo=vite)](https://vitejs.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=flat-square&logo=postgresql)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D?style=flat-square&logo=redis)](https://redis.io/)
[![Celery](https://img.shields.io/badge/Celery-5.6-37814A?style=flat-square&logo=celery)](https://docs.celeryq.dev/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker)](https://www.docker.com/)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Docker (Recommended)](#option-a-docker-recommended)
  - [Local Development](#option-b-local-development)
- [Environment Variables](#-environment-variables)
- [Backend Modules](#-backend-modules)
- [Frontend Views & Roles](#-frontend-views--roles)
- [API Overview](#-api-overview)
- [Admin Console](#-admin-console)
- [Design System](#-design-system)
- [Default Credentials](#-default-credentials)
- [Contributing](#-contributing)

---

## 🌍 Overview

**Procus v2** is a comprehensive B2B and B2C construction industry marketplace. It facilitates the full lifecycle of construction projects — from material procurement and contractor tendering, to contract execution, milestone tracking, escrow payments, and regulatory compliance.

### Key Capabilities

| Domain | Description |
|---|---|
| 🛒 **Catalogue** | Browse and purchase construction materials from verified vendors |
| 📋 **Tenders & Bids** | Post contracts/tenders; contractors submit competitive bids |
| 🏢 **Contractor Registry** | Verified contractor onboarding with capability classification |
| 📁 **Project Management** | Full project lifecycle from creation to milestone completion |
| 💳 **Escrow & Payments** | Secure escrow-backed payment release tied to milestone approvals |
| 📈 **Investment** | Secondary market and investment instruments |
| 🏦 **Banking & Finance** | Integrated financial tools for project financing |
| 📊 **Reporting** | Regulatory and compliance reporting dashboards |
| ⚙️ **Admin Console** | Full platform administration: users, config, roles, countries, master data |

### Structure
*   `frontend/`: Vue 3 + Vite app.
*   `backend/`: Django + DRF API.
*   `infra/`: Infrastructure configs.
*   `docs/`: Project documentation.

## 📚 Documentation

Detailed documentation for the entire platform is available in the [`docs/`](./docs) folder:

| Document | Description |
|---|---|
| 🏗️ [**Roadmap & Phases**](./docs/PHASES.md) | Six-phase development journey and module map |
| 📋 [**SRS**](./docs/SRS.md) | Software Requirements Specification |
| 🏛️ [**SDD**](./docs/SDD.md) | Software Design Document (Architecture) |
| 📖 [**User Guide**](./docs/USER_GUIDE.md) | Role-based workflows for all users |
| 🤝 [**Contributing**](./CONTRIBUTING.md) | Standards, commit conventions, and PR process |
| 🎨 [**Style Guide**](./frontend/FRONTEND_STYLE_GUIDE.md) | Frontend design system and UI tokens |

---

## 🗺️ Development Phases

The platform is built across **6 delivered phases**, each building upon the last. See the full breakdown in [`docs/PHASES.md`](./docs/PHASES.md).

| Phase | Name | Key Additions | Status |
|---|---|---|---|
| **1** | Materials Liquidity Engine | User accounts, vendor profiles, product catalogue, orders, payments, disputes | ✅ Done |
| **2** | Contracts & Execution Layer | Contractor registry, competitive bidding, contract lifecycle, milestone tracking | ✅ Done |
| **3** | Financial Infrastructure | Escrow fund holding, milestone-triggered releases, dispute arbitration, credit products | ✅ Done |
| **4** | Projects, Property & Capital | Top-level project entity, investor pledges, property listings, capital pipeline | ✅ Done |
| **5** | Regulated Investment & Government | KYC/AML compliance, binding agreements, public tenders, enterprise workflows | ✅ Done |
| **6** | Full Regulatory Integration & AI | Banking settlement, regulatory reporting, AI risk prediction, secondary market, ERP connectors | ✅ Done |

> 📖 **Full details** — goals, modules, data models, API endpoints, and frontend views for each phase: [`docs/PHASES.md`](./docs/PHASES.md)

---

## 🏛️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Client Browser                       │
│                    Vue 3 + Vite SPA (5173)                   │
│         Pinia State · Vue Router · Axios · Vanilla CSS       │
└────────────────────────────┬────────────────────────────────┘
                             │ HTTP / REST API
┌────────────────────────────▼────────────────────────────────┐
│                   Django REST Framework (8000)               │
│          DRF ViewSets · JWT Auth · CORS · django-filter      │
│                                                             │
│   ┌──────────┐  ┌──────────┐  ┌───────────┐  ┌──────────┐  │
│   │ accounts │  │ catalog  │  │contractors│  │ projects │  │
│   │  rbac    │  │ vendors  │  │   bids    │  │ contracts│  │
│   │ platform │  │ taxonomy │  │ milestones│  │  escrow  │  │
│   │ settings │  │compliance│  │  finance  │  │ banking  │  │
│   └──────────┘  └──────────┘  └───────────┘  └──────────┘  │
└────────┬──────────────────────────────────────┬─────────────┘
         │                                      │
┌────────▼────────┐                  ┌──────────▼──────────┐
│   PostgreSQL 15 │                  │      Redis 7         │
│   (Primary DB)  │                  │  (Cache + Broker)    │
└─────────────────┘                  └─────────────────────┘
                                              │
                              ┌───────────────▼──────────────┐
                              │    Celery Worker + Beat       │
                              │   (Async tasks & scheduling)  │
                              └───────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Backend
| Technology | Version | Purpose |
|---|---|---|
| Python | 3.10+ | Runtime |
| Django | 5.2 | Web framework |
| Django REST Framework | 3.16 | API layer |
| django-cors-headers | 4.9 | CORS management |
| django-filter | 25.2 | API filtering |
| Celery | 5.6 | Async task queue |
| PostgreSQL | 15 | Primary database |
| Redis | 7 | Message broker & cache |
| Pillow | latest | Image processing |
| PyYAML | latest | Configuration parsing |
| cryptography | latest | Security utilities |

### Frontend
| Technology | Version | Purpose |
|---|---|---|
| Vue 3 | 3.5 | UI framework |
| Vite | 7.2 | Build tool & Dev server |
| Vue Router | 5.0 | Client-side routing |
| Pinia | 3.0 | State management |
| Axios | 1.13 | HTTP client |
| Vanilla CSS | — | Styling (custom design system) |

### Infrastructure
| Technology | Purpose |
|---|---|
| Docker + Docker Compose | Service orchestration |
| PostgreSQL 15 | Persistent relational database |
| Redis 7 | Task queue broker & caching |

---

## 📁 Project Structure

```
procusv2/
├── backend/                    # Django REST API
│   ├── config/                 # Django project settings, URLs, Celery
│   │   ├── settings.py
│   │   ├── urls.py             # API v1 router
│   │   ├── celery.py
│   │   └── urls_v2 → v6.py    # Versioned URL configs
│   │
│   ├── accounts/               # User auth, registration, profiles
│   ├── rbac/                   # Role-based access control + audit logs
│   ├── platform_settings/      # Platform config, currencies, countries
│   ├── taxonomy/               # Master data — category classification
│   │
│   ├── catalog/                # Product/material catalogue
│   ├── vendors/                # Vendor onboarding & management
│   ├── contractors/            # Contractor registry & verification
│   ├── projects/               # Project lifecycle management
│   ├── bids/                   # Tender bidding engine
│   ├── contracts/              # Contract management
│   ├── milestones/             # Milestone tracking & approvals
│   ├── orders/                 # Order management
│   ├── payments/               # Payment processing
│   ├── escrow/                 # Escrow fund management
│   ├── finance/                # Financial instruments
│   ├── banking/                # Banking integrations
│   ├── investments/            # Investment & secondary market
│   ├── liquidity/              # Liquidity management
│   ├── risk/                   # Risk assessment
│   ├── scoring/                # Credit / contractor scoring
│   ├── compliance/             # Compliance tracking
│   ├── regulation/             # Regulatory reporting
│   ├── disputes/               # Dispute resolution
│   ├── reviews/                # Ratings & reviews
│   ├── reporting/              # Analytics & reports
│   ├── ai_engine/              # AI-powered features
│   ├── enterprise/             # Enterprise accounts
│   ├── government/             # Government procurement
│   ├── integrations/           # Third-party integrations
│   ├── logistics/              # Delivery & logistics
│   ├── property/               # Property management
│   │
│   ├── manage.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                   # Vue 3 + Vite SPA
│   ├── src/
│   │   ├── views/              # Page-level Vue components (20 views)
│   │   ├── components/         # Reusable UI components
│   │   │   └── ui/             # Button, Badge, Modal, Card, etc.
│   │   ├── styles/             # Design system CSS
│   │   │   ├── tokens.css      # CSS custom properties (design tokens)
│   │   │   ├── base.css        # Resets & element defaults
│   │   │   ├── layout.css      # Grid & flex utilities
│   │   │   └── components.css  # Reusable component classes
│   │   ├── stores/             # Pinia stores
│   │   ├── services/           # API service layer (Axios)
│   │   ├── router/             # Vue Router config
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile
│
├── infra/                      # Infrastructure configs
├── docs/                       # Extended project documentation
├── docker-compose.yml          # Full stack orchestration
├── .env.example                # Environment template
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) ≥ 24 (recommended)
- **OR** for local dev:
  - Python 3.10+
  - Node.js 18+ & npm
  - PostgreSQL 15
  - Redis 7

---

### Option A: Docker (Recommended)

The fastest way to get the entire stack running.

**1. Clone the repository**
```bash
git clone https://github.com/nelsonadagi/procusv2.git
cd procusv2
```

**2. Configure environment**
```bash
cp .env.example .env
# Edit .env with your values (see Environment Variables section)
```

**3. Start all services**
```bash
docker-compose up --build
```

This starts:
| Service | Port | Description |
|---|---|---|
| `frontend` | 5173 | Vue 3 dev server |
| `backend` | 8000 | Django API |
| `postgres` | 5432 | PostgreSQL database |
| `redis` | 6379 | Redis cache/broker |
| `celery-worker` | — | Async task worker |
| `celery-beat` | — | Scheduled task runner |

**4. Run initial setup** *(first time only)*
```bash
# In a separate terminal:
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
```

**5. Access the application**

| Service | URL |
|---|---|
| 🌐 Frontend App | http://localhost:5173 |
| 🔌 Backend API | http://localhost:8000/api/ |
| 🛡️ Django Admin | http://localhost:8000/admin/ |

---

### Option B: Local Development

#### Backend Setup

```bash
cd backend

# Create & activate virtual environment
python -m venv venv
source venv/bin/activate          # macOS/Linux
# venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment (set DATABASE_URL to your local Postgres)
cp ../.env.example ../.env

# Apply migrations
python manage.py migrate

# (Optional) Load seed data
python manage.py shell < seed_data.py

# Start dev server
python manage.py runserver
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

#### Start Celery (optional)

```bash
# Worker
celery -A config worker -l info

# Beat scheduler (separate terminal)
celery -A config beat -l info
```

---

## 🔐 Environment Variables

Copy `.env.example` to `.env` and fill in the values:

```env
# Database
DATABASE_URL=postgres://postgres:postgres@postgres:5432/marketplace

# Redis
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Django
DJANGO_SECRET_KEY=replace_this_with_a_long_random_secret_key
DEBUG=1                    # Set to 0 in production
ALLOWED_HOSTS=*            # Restrict in production

# Integrations
PAYMENT_PROVIDER_KEYS=placeholder
```

> ⚠️ **Never commit your `.env` file.** It is already included in `.gitignore`.

---

## 🧩 Backend Modules

The Django backend is organised into domain-specific apps:

| App | Responsibility |
|---|---|
| `accounts` | User registration, authentication, profile management |
| `rbac` | Role-based access control, permissions, audit log stream |
| `platform_settings` | Platform identity, currency rates, country configuration |
| `taxonomy` | Master data — taxonomy categories for materials, services, projects |
| `catalog` | Construction material/product listings |
| `vendors` | Vendor onboarding, verification, and product management |
| `contractors` | Contractor profiles, capability categories, verification queue |
| `projects` | Project creation, lifecycle management |
| `bids` | Tender posting, bid submission, and evaluation |
| `contracts` | Contract generation, approval, and lifecycle |
| `milestones` | Milestone definition, progress tracking, and approval workflows |
| `orders` | Material order processing |
| `payments` | Payment gateway integration, transaction records |
| `escrow` | Escrow fund holding and milestone-triggered releases |
| `finance` | Loan products, financing instruments |
| `banking` | Banking account integration |
| `investments` | Investment products and portfolio management |
| `liquidity` | Liquidity pool management |
| `risk` | Risk scoring and assessment engine |
| `scoring` | Contractor and project credit scoring |
| `compliance` | Regulatory compliance tracking |
| `regulation` | Government and industry regulatory reporting |
| `disputes` | Dispute filing, mediation, and resolution |
| `reviews` | Ratings and reviews for vendors and contractors |
| `reporting` | Analytics, dashboards, and business intelligence |
| `ai_engine` | AI-assisted recommendations, scoring, and automation |
| `enterprise` | Enterprise account management |
| `government` | Government procurement and tendering |
| `integrations` | Third-party service integrations |
| `logistics` | Delivery tracking and logistics management |
| `property` | Property listing and management |

---

## 🖥️ Frontend Views & Roles

The Vue SPA provides role-specific dashboards and shared views:

| View | Route | User Role |
|---|---|---|
| `Login.vue` | `/login` | All |
| `Register.vue` | `/register` | All |
| `AdminDashboard.vue` | `/admin` | Admin |
| `VendorDashboard.vue` | `/vendor` | Vendor |
| `BuyerDashboard.vue` | `/buyer` | Buyer |
| `ContractorDashboard.vue` | `/contractor` | Contractor |
| `ContractorRegistration.vue` | `/contractor/register` | Public |
| `InvestorDashboard.vue` | `/investor` | Investor |
| `OwnerDashboard.vue` | `/owner/dashboard` | Project Owner |
| `ProductList.vue` | `/products` | Buyer / All |
| `ProductDetail.vue` | `/products/:id` | Buyer / All |
| `ProjectList.vue` | `/projects` | All |
| `ProjectDetail.vue` | `/projects/:id` | All |
| `CreateProject.vue` | `/projects/new` | Owner |
| `ContractList.vue` | `/contracts` | All |
| `ContractDetail.vue` | `/contracts/:id` | All |
| `PostContract.vue` | `/contracts/new` | Project Owner / Admin |
| `ViewTenders.vue` | `/tenders` | Contractor |
| `SecondaryMarket.vue` | `/market` | Investor |
| `RegulatoryReports.vue` | `/reports` | Admin / Staff |

---

## 🔌 API Overview

Base URL: `http://localhost:8000/api/`

### Authentication
```
POST /api/accounts/register/       # New user registration
POST /api/token/                   # Obtain JWT token pair
POST /api/token/refresh/           # Refresh access token
```

### Core Resources
```
GET|POST   /api/catalog/products/
GET|POST   /api/contractors/
GET|POST   /api/projects/
GET|POST   /api/bids/
GET|POST   /api/contracts/
GET|POST   /api/milestones/
GET|POST   /api/orders/
GET|POST   /api/payments/
GET|POST   /api/escrow/
GET|POST   /api/taxonomy/categories/
```

### Platform Administration
```
GET|PATCH  /api/config/platform/
GET|POST   /api/config/currencies/
GET|POST   /api/config/countries/
GET|POST   /api/config/roles/
GET        /api/config/admin-users/
GET        /api/rbac/audit-logs/
GET        /api/accounts/management/
```

> 📖 Detailed API documentation: Access `/api/` in a browser for the DRF browsable API when `DEBUG=1`.

---

## 🛡️ Admin Console

The built-in **Admin Console** (`/admin` in the SPA) provides a secure, role-gated control panel:

| Section | Features |
|---|---|
| 📊 **Overview** | Live audit log stream, platform KPIs (escrow liquidity, active works, pending nodes, disputes) |
| 🛡️ **Verifications** | Contractor verification queue — review and approve applications |
| ⚙️ **Settings → Platform** | Name, branding, support contacts, regional defaults, brand colours |
| 💱 **Settings → Currency** | Add/remove currencies, live exchange rates relative to platform default |
| 👥 **Settings → Users** | View all users, toggle active status, reassign roles |
| 🔐 **Settings → Roles** | Manage Django permission groups used as platform roles |
| 🌍 **Settings → Countries** | Configure active countries, phone prefixes, set regional default |
| 🗂️ **Settings → Master Data** | Taxonomy categories (MATERIAL, SERVICE, PROJECT, PROPERTY, FINANCE, etc.) |

**User Roles**: `ADMIN` · `VENDOR` · `BUYER` · `CONTRACTOR` · `INVESTOR` · `PROJECT_OWNER` · `STAFF`

---

## 🎨 Design System

The frontend uses a **custom Vanilla CSS design system** — no utility frameworks.

### Structure (`frontend/src/styles/`)
| File | Purpose |
|---|---|
| `tokens.css` | CSS custom properties — colours, spacing, typography |
| `base.css` | Resets and element-level defaults |
| `layout.css` | Container, grid & flexbox helpers |
| `components.css` | Reusable component classes (`.btn`, `.card`, `.badge`) |

### Design Principles
- **Mobile-first**: Base styles for mobile, `@media (min-width: 768px)` for desktop
- **Semantic classes**: `.product-card` not inline utility soup
- **Scoped styles**: All Vue components use `<style scoped>`
- **Token-based**: No hardcoded hex values — always `var(--pz-color-*)` 
- **Spacing scale**: 4px increments — `--pz-space-1` (4px) through `--pz-space-16` (64px)

---

## 🔑 Default Credentials

> ⚠️ Change these immediately in any non-local environment.

| Role | Username | Password |
|---|---|---|
| Django Admin | `admin` | `adminpass` |
| Vendor | `vendor1` | `vendorpass` |

---

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/your-feature-name`
3. **Commit** your changes: `git commit -m "feat: add your feature"`
4. **Push** to your branch: `git push origin feature/your-feature-name`
5. **Open** a Pull Request against `main`

### Commit Convention
Follow [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` — New feature
- `fix:` — Bug fix
- `chore:` — Maintenance (deps, config, docs)
- `refactor:` — Code restructure, no behaviour change
- `docs:` — Documentation only

---

## 📄 License

This project is proprietary. All rights reserved.

---

<div align="center">
  <strong>Built for the construction industry 🏗️</strong><br/>
  <em>Procus v2 · © 2026</em>
</div>
