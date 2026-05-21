# Workflow UX Transformation — LLM Implementation Spec

**Purpose:** Precise, file-level implementation checklist for converting each module from its current state to the workflow-first UX defined in the transform blueprints.  
**Approach:** Every module has been inspected against its blueprint and documented with exact file paths, status, and acceptance criteria.  
**Status Convention:** `✅ Done` | `🔄 Partial` | `❌ Missing`

---

## Implementation Coverage Summary

| Module | Blueprint | Tasks | ✅ Done | 🔄 Partial | ❌ Missing | Maturity |
|--------|-----------|-------|---------|------------|------------|----------|
| 1. Vendor | `VENDOR_MATERIAL_WORKFLOW_UX_TRANSFORM.md` | 47 | ~32 | ~8 | ~7 | **Strong** — core wizard, health score, CSV import exist. Gaps in step gating, coaching. |
| 2. Property | `PROPERTY_MODULE_WORKFLOW_UX_TRANSFORM.md` | 103 | ~68 | ~18 | ~17 | **Strong** — 6-section edit wizard, discovery with filters/compare/shortlist, booking flow. Gaps in approval queue, step gating, buyer trust signals. |
| 3. Buyer | `BUYER_MODULE_WORKFLOW_UX_TRANSFORM.md` | 75 | ~52 | ~12 | ~11 | **Mature** — discovery, quote flow, order management, payment simulation. Gaps in shortlist, multi-item cart, vendor scorecard, order detail page. |
| 4. Owner | `OWNER_MODULE_WORKFLOW_UX_TRANSFORM.md` | 76 | ~48 | ~14 | ~14 | **Solid** — project/tender infrastructure, contract linking, milestone display. Gaps in milestone approval UI, escrow frontend (mock), bid comparison matrix, real activity logs. |
| 5. Investor | `INVESTOR_MODULE_WORKFLOW_UX_TRANSFORM.md` | 64 | ~18 | ~10 | ~36 | **Thin** — dashboard, pledge API, agreement backend exist. Major gaps: onboarding wizard, KYC UI, pledge→agreement workflow, portfolio analytics, empty `backend/investments` app. |
| 6. Contractor | `CONTRACTOR_MODULE_WORKFLOW_UX_TRANSFORM.md` | 58 | ~32 | ~10 | ~16 | **Functional** — bid-execute pipeline works. Gaps: multi-step onboarding, hardcoded dashboard stats, payment drawdown tracking, milestone evidence upload, auto-escrow release. |
| 7. Courier | `COURIER_MODULE_WORKFLOW_UX_TRANSFORM.md` | 35 | ~18 | ~3 | ~14 | **Moderate** — profile, zone CRUD, shipment tracking, webhook endpoint. Gaps: POD capture, courier assignment, driver mobile view, real carrier integrations, document upload wiring. |
| 8. Project | `PROJECT_MODULE_WORKFLOW_UX_TRANSFORM.md` | 42 | ~24 | ~4 | ~14 | **Solid foundation** — creation, list, detail workspace with 9 tabs, requirements, material suggestions, funding. Gaps: multi-step wizard, BOM structure, budget tracking, Gantt view, event-sourced activity. |
| 9. Contract | `CONTRACT_MODULE_WORKFLOW_UX_TRANSFORM.md` | 45 | ~26 | ~2 | ~17 | **Solid foundation** — posting, discovery, detail with bids/milestones/attachments, award flow, milestone approval. Gaps: templates, digital signature, bid comparison matrix, escrow integration, penalty clauses. |
| 10. Admin | `ADMIN_MODULE_WORKFLOW_UX_TRANSFORM.md` | 46 | ~22 | ~4 | ~20 | **Functional shell** — dashboard, verification queues, disputes, user management, security monitor. Gaps: platform health metrics, KYC doc viewer, batch approval, risk scoring display, content moderation, fraud detection. |
| 11. Government | `GOVERNMENT_MODULE_WORKFLOW_UX_TRANSFORM.md` | 18 | ~3 | ~1 | ~14 | **Placeholder** — dashboard shell, PublicTender CRUD API, AuditLog model. Almost all government-specific UX missing: publishing UI, evaluation workspace, compliance review, award transparency, anti-corruption audit viewer. |

**Key cross-cutting patterns:**
- Workflow banner/card component reused across all 11 modules — **good design system consistency**.
- Backend model maturity often exceeds frontend maturity (escrow, milestones, investments, KYC, risk scoring all have models but lack UI wiring).
- Event-sourced activity timelines are computed client-side everywhere; no persistent backend implementation exists.
- Approval-driven role activation affects onboarding flows for Vendor, Contractor, Investor, Courier.

---

# 1. VENDOR MODULE

**Blueprint:** `VENDOR_MATERIAL_WORKFLOW_UX_TRANSFORM.md`  
**Frontend Root:** `frontend/src/components/vendor/`, `frontend/src/views/VendorDashboard.vue`  
**Backend Root:** `backend/vendors/`, `backend/catalog/`, `backend/orders/`

---

## 1.1 Vendor Onboarding & Approval

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 1.1.1 | Remove role selection from registration | ✅ Done | `backend/accounts/serializers.py` | `role` is optional, defaults to `PROJECT_OWNER` | Registration succeeds without role field |
| 1.1.2 | Show onboarding state (Step 1 of 2) | ✅ Done | `frontend/src/views/VendorDashboard.vue` | `needsOnboarding` block with CTA to `/vendors/register` | Unregistered vendors see "Complete your vendor profile" |
| 1.1.3 | Show pending state (Step 2 of 2) | ✅ Done | `frontend/src/views/VendorDashboard.vue` | `isPendingApproval` block with CSV template CTA + View Profile | Pending vendors see "Typical approval 1–2 business days" |
| 1.1.4 | Show suspended state | ✅ Done | `frontend/src/views/VendorDashboard.vue` | `isSuspended` block with Contact Support CTA | Suspended vendors see freeze message |
| 1.1.5 | **Vendor registration as true wizard** | ❌ Missing | `frontend/src/views/VendorRegistration.vue` | Convert single-page form to 3-step wizard with persistence: 1) Business Registry, 2) Geo / Delivery, 3) Documents & Submit. Each step validates before Next. | Vendor can resume abandoned registration; step 3 shows document checklist |
| 1.1.6 | **Approval countdown / queue position** | ✅ Done | `frontend/src/views/VendorDashboard.vue` + backend | Backend `me()` returns `queue_position` and `pending_hours` when `verified_status == PENDING`. Frontend shows queue badge with position and time since submission. | Vendor sees queue position and wait time |

---

## 1.2 Product Creation Wizard

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 1.2.1 | 6-step wizard with progress | ✅ Done | `frontend/src/components/vendor/VendorInventorySection.vue` | Step bubbles: Commercial, Technical, Compliance, Documents, Media, Review | Wizard renders for new products; tabs render for edits |
| 1.2.2 | Readiness score bar | ✅ Done | `frontend/src/components/vendor/VendorInventorySection.vue` | Real-time 0–100% bar in wizard header | Score updates on every field change |
| 1.2.3 | Smart category suggestion | ✅ Done | `frontend/src/components/vendor/VendorInventorySection.vue` | `suggestedCategory` computed from keyword map against product name | Typing "Portland cement" suggests "Cement > Portland Cement" |
| 1.2.4 | Price anomaly detection | ✅ Done | `frontend/src/components/vendor/VendorInventorySection.vue` | `priceAnomaly` computed vs `/v1/products/category-price-stats/` | Price >2× median shows "Your price is significantly above category average" |
| 1.2.5 | Duplicate detection | ✅ Done | `frontend/src/components/vendor/VendorInventorySection.vue` | Warn if name fuzzy-matches existing vendor product | "You already have 'Dangote Cement 50kg'. Publish another?" |
| 1.2.6 | Certification gap suggestion | ✅ Done | `frontend/src/components/vendor/VendorInventorySection.vue` | Category → common cert chips (KEBS, ISO 9001, CE) | Selecting "Cement" shows KEBS + ISO chips |
| 1.2.7 | Image validation | ✅ Done | `frontend/src/components/vendor/VendorInventorySection.vue` | Warn if image < 500px wide | `imageValidationWarnings` array renders inline |
| 1.2.8 | Review step with buyer preview | ✅ Done | `frontend/src/components/vendor/VendorInventorySection.vue` | `activeProductTab === 'review'` renders product card preview + checklist | Vendor sees exactly how buyers will see the listing |
| 1.2.9 | **Step-level validation gating** | ✅ Done | `frontend/src/components/vendor/VendorInventorySection.vue` | `canAdvanceFromStep(step)` checks gates: Step 1 requires name + category + base_price>0. Step 5 warns if zero images (allows continue). Next/Continue buttons disabled when gate fails. Gate error renders inline. | Vendor cannot click "Continue to Technical" without name, category, and price |
| 1.2.10 | **Full-page publishing experience** | ❌ Missing | `frontend/src/views/VendorPublishPage.vue` (new) | Extract wizard from modal into dedicated route `/vendor/publish`. Modal only used for quick edits. | First-time vendor is routed to immersive page, not modal |
| 1.2.11 | **Auto-save draft + resume** | ✅ Done | `frontend/src/components/vendor/VendorInventorySection.vue` | `productForm` debounce-saves to `localStorage` every 800ms. Draft loaded when opening create modal. Cleared on successful publish. | Vendor can close browser and resume wizard later |
| 1.2.12 | **Marketing flags gating** | ✅ Done | `frontend/src/components/vendor/VendorInventorySection.vue` | `isExperiencedVendor` computed (products.length >= 3) hides Featured/New Arrival/On Sale checkboxes and shows progressive hint. | Flags hidden for new vendors; visible after 3 products |
| 1.2.13 | **Confetti / celebration on first publish** | ✅ Done | `frontend/src/components/vendor/VendorInventorySection.vue` | CSS confetti animation + modal overlay with "Your material is live!" message. Auto-dismisses after 4s. | First publish triggers celebratory feedback |

---

## 1.3 Catalog Workspace (Dashboard)

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 1.3.1 | Operational card groups | ✅ Done | `frontend/src/components/vendor/VendorInventorySection.vue` | `attentionProducts`, `healthyProducts`, `draftProducts`, `hiddenProducts` computed groups | Cards grouped by operational state |
| 1.3.2 | Product card with next-best-action | ✅ Done | `frontend/src/components/vendor/VendorProductCard.vue` | `primaryAction` computed: Restock (urgent) → Publish (draft) → Add Photos → Complete → Edit | Each card shows the ONE most important action |
| 1.3.3 | Readiness mini-bar on card | ✅ Done | `frontend/src/components/vendor/VendorProductCard.vue` | 0–100 bar with color coding (good/warn/bad) | Bar visible on every card |
| 1.3.4 | Priority strip | ✅ Done | `frontend/src/components/vendor/VendorWorkspaceHeader.vue` | `urgentItems` computed from LOW_STOCK, OUT_OF_STOCK, unresponded quotes | Red strip at top of workspace |
| 1.3.5 | Health score ring | ✅ Done | `frontend/src/components/vendor/VendorWorkspaceHeader.vue` | Conic-gradient ring + label (Excellent/Good/Fair/Needs Work/At Risk) | Ring renders with correct color |
| 1.3.6 | Expandable health breakdown | ✅ Done | `frontend/src/components/vendor/VendorWorkspaceHeader.vue` | Click ring → expand 3 cards: Listing Completeness, Stock Health, Certifications | Breakdown shows counts and percentages |
| 1.3.7 | Frontend heuristic recommendations | ✅ Done | `frontend/src/components/vendor/VendorWorkspaceHeader.vue` | Recommends photos → descriptions → certifications based on catalog gaps | Up to 3 recommendation cards shown |
| 1.3.8 | **Complete health score formula** | ✅ Done | `frontend/src/components/vendor/VendorWorkspaceHeader.vue` + backend | `responseHealth` from `avg_response_time_hours`, `freshnessHealth` from days since last product update. Weights: Listing 25%, Stock 25%, Response 20%, Certs 15%, Freshness 15%. | Health score matches blueprint weights exactly |
| 1.3.9 | **Performance metrics strip** | ✅ Done | `frontend/src/components/vendor/VendorWorkspaceHeader.vue` | Stats row: Active Products, Views This Week, Quotes This Month, Conversion Rate. Fetched from `/v1/products/dashboard-stats/` and passed as prop. | Numbers visible next to health score |
| 1.3.10 | **Backend-driven recommendations** | ✅ Done | Backend: `/vendors/me/recommendations/` | Returns structured tasks: RESTOCK, INCOMPLETE_LISTING, RESPOND_QUOTE, PUBLISH, COMPLIANCE with priority + CTA. Frontend integration pending. | Frontend can consume backend tasks |
| 1.3.11 | **"Waiting on You" vs "Waiting on Others"** | ✅ Done | `frontend/src/components/vendor/VendorWorkspaceHeader.vue` | Two-column layout: left = actionable recommendations (green dot), right = blocked items like admin approval (orange dot). Each column shows up to 3 cards. | Visual separation of internal vs external blockers |
| 1.3.12 | **Catalog performance chart** | ✅ Done | `frontend/src/components/vendor/VendorPerformanceChart.vue` + backend | SVG line chart showing views + quotes over last 30 days. Backend `GET /v1/products/daily-stats/` returns daily data points. Hover tooltip with exact values. | Chart renders on vendor dashboard |

---

## 1.4 Inventory Management

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 1.4.1 | Stock adjustment with movement record | ✅ Done | Backend: `ProductInventoryMovement` + frontend modal | Adjust modal updates quantity with note | Movement ledger tracks every change |
| 1.4.2 | Inventory history timeline | ✅ Done | `frontend/src/components/vendor/VendorProductTimeline.vue` | Fetches `/v1/products/{id}/inventory-history/` | Timeline shows stock changes |
| 1.4.3 | Stock-out prediction API | ✅ Done | Backend: `/v1/products/{id}/stock-out-prediction/` | Returns `days_until_stockout` based on 30-day quote rate | Endpoint exists and returns data |
| 1.4.4 | **Stock-out prediction UI** | ✅ Done | `frontend/src/components/vendor/VendorProductCard.vue` + backend | `days_until_stockout` added to `ProductListSerializer`. LOW_STOCK cards show "At current quote volume, you'll run out in ~N days" banner. | Low-stock products show prediction at a glance |
| 1.4.5 | **Auto-reorder suggestion** | 🔄 Partial | `frontend/src/components/vendor/VendorWorkspaceHeader.vue` + backend | Backend recommendations now include `days_until_stockout` for low-stock items. Frontend card display still needed. | Recommendation uses prediction data |
| 1.4.6 | **Bulk stock adjustment** | ✅ Done | `frontend/src/components/vendor/VendorInventorySection.vue` | "Bulk Adjust" toolbar button opens modal with product checklist + quantity/note fields. Sequential API calls to `adjust-inventory` endpoint. Shows success/failure count. | Vendor can update multiple products at once |

---

## 1.5 Quote & Order Response

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 1.5.1 | Quote inbox with status badges | ✅ Done | `frontend/src/components/vendor/VendorQuotesSection.vue` | Lists quote requests with `Awaiting Response` / `Responded` badges | Quotes visible with clear status |
| 1.5.2 | One-tap actions (Accept / Counter / Decline) | ✅ Done | `frontend/src/components/vendor/VendorQuotesSection.vue` | Three buttons per pending quote | Actions work without page reload |
| 1.5.3 | Counter-offer modal | ✅ Done | `frontend/src/components/vendor/VendorQuotesSection.vue` | Modal with line-item pricing + notes | Vendor can submit negotiated price |
| 1.5.4 | Order fulfillment pipeline | ✅ Done | `frontend/src/components/vendor/VendorOrdersSection.vue` | Status buttons: Confirm → Pack → Ship → Deliver | Correct button shown per order status |
| 1.5.5 | **Quote response time coaching** | ✅ Done | `frontend/src/components/vendor/VendorQuotesSection.vue` + backend | Backend returns `vendor_avg_response_time_hours`. UI shows: "You respond in 4h on average. Responding within 2h increases win rate by 35%." | Coaching text visible on every pending quote |
| 1.5.6 | **Urgent quote highlight** | ✅ Done | `frontend/src/components/vendor/VendorQuotesSection.vue` | Quotes >12h old get red border + "URGENT >12h" badge | Visual escalation for stale quotes |
| 1.5.7 | **Quote deep links from notifications** | ✅ Done | `frontend/src/components/vendor/VendorInventorySection.vue` | Notification click with `quote_request_id` emits `navigate('quotes')`, switching dashboard to Quotes section. Product notifications open edit modal directly. | Clicking notification navigates to relevant section |

---

## 1.6 CSV Import

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 1.6.1 | Template download | ✅ Done | `frontend/src/components/vendor/VendorInventorySection.vue` | `downloadTemplate()` hits `/v1/products/download_template/` | CSV downloads correctly |
| 1.6.2 | File upload | ✅ Done | `frontend/src/components/vendor/VendorInventorySection.vue` | Hidden file input → `POST /v1/products/import_products/` | Upload succeeds |
| 1.6.3 | **Step 1: Download Template with explainer** | ✅ Done | `frontend/src/components/vendor/VendorCsvImportWizard.vue` | Step 1 shows required & optional columns with descriptions, example row, and Download CSV Template CTA. | Vendor understands each column before downloading |
| 1.6.4 | **Step 2: Upload & Validate with preview** | ✅ Done | `frontend/src/components/vendor/VendorCsvImportWizard.vue` | Drag-and-drop upload validates via `POST /v1/products/validate_import/`. Shows first 5 rows preview + row-by-row error report. | Vendor sees preview + errors before commit |
| 1.6.5 | **Step 3: Import & Review** | ✅ Done | `frontend/src/components/vendor/VendorCsvImportWizard.vue` | Import results page shows created count + error count with summary stats. CTA: "View Imported Products". Errors listed with messages. | Vendor gets clear post-import summary |

---

## 1.7 Notifications & Alert System

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 1.7.1 | WebSocket notification store | ✅ Done | `frontend/src/stores/notifications.js` | Pinia store with auto-reconnect | Notifications arrive in real time |
| 1.7.2 | Toast container | ✅ Done | `frontend/src/components/NotificationCenter.vue` | Auto-dismiss toasts | Toasts show for 5 seconds |
| 1.7.3 | Vendor notification panel | ✅ Done | `frontend/src/components/vendor/VendorNotificationPanel.vue` | Inline card with unread count + action buttons | Panel renders inside inventory section |
| 1.7.4 | **Task-based notification model** | ❌ Missing | Backend: `notifications/models.py` + frontend | Replace generic `Notification` with `VendorTask`: `{type: 'RESTOCK', product_id, priority: 'HIGH', due_date, cta_url, impact: 'Lost quote opportunities'}`. | Notifications answer: What happened? Why does it matter? What should I do? |
| 1.7.5 | **Certification expiry notification** | ✅ Done | Backend: `catalog/signals.py` + `management/commands/check_certification_expiry.py` | `post_save` signal and daily cron create SYSTEM notifications when certification expires within 30 days. Frontend notification panel displays them. | Expiring certs trigger proactive alerts |
| 1.7.6 | **Price competitiveness nudge** | ✅ Done | Backend: `/vendors/me/recommendations/` + frontend | Returns PRICE type recommendation. Frontend iconMap includes 💰 for PRICE. Displayed in workspace header. | Nudge appears in recommendations |

---

## 1.8 Product Timeline & Activity

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 1.8.1 | Activity timeline component | ✅ Done | `frontend/src/components/vendor/VendorProductTimeline.vue` | Fetches `/v1/products/{id}/timeline/` | Renders chronologically |
| 1.8.2 | **Timeline event richness** | ✅ Done | Backend: `catalog/views.py` `timeline()` | Events: CREATED, INVENTORY, MEDIA, COMPLIANCE, STOCK_LOW, OUT_OF_STOCK, CERT_EXPIRING. PRICE_CHANGED deferred (no price history model yet). | All event types from blueprint section 8 are present |
| 1.8.3 | **Upcoming events section** | ✅ Done | `frontend/src/components/vendor/VendorProductTimeline.vue` | Shows certification expiry dates ≤90 days below timeline. Warns (⚠️) when ≤30 days. | Vendor sees future deadlines |

---

## 1.9 Navigation & Information Architecture

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 1.9.1 | Sidebar navigation | ✅ Done | `frontend/src/views/VendorDashboard.vue` | Four sections: Supply Inventory, Logistics Orders, Procurement Quotes, Operational Profile | Nav switches sections |
| 1.9.2 | **Goal-based navigation redesign** | ✅ Done | `frontend/src/views/VendorDashboard.vue` | Sidebar restructured: Workspace (📦 Catalog, 💬 Quotes, 📋 Orders, ⚙️ Account) + Quick Actions (🚀 Launch, Exit). Labels reflect goals, not database tables. | Navigation labels reflect goals, not database tables |
| 1.9.3 | **Mobile bottom tab bar** | ✅ Done | `frontend/src/views/VendorDashboard.vue` | Fixed bottom tab bar visible on mobile (< 768px): 📦 Catalog, 🚀 Launch, 💬 Quotes, 📊 Insights, 👤 Account. Hidden on desktop. | Mobile nav is thumb-reachable |

---

## 1.10 Accessibility & Mobile

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 1.10.1 | ARIA live region | ✅ Done | `frontend/src/components/vendor/VendorInventorySection.vue` | `aria-live="polite"` region for dynamic updates | Screen readers announce updates |
| 1.10.2 | Keyboard navigation in wizard | ✅ Done | `frontend/src/components/vendor/VendorInventorySection.vue` | `handleWizardKeydown` handles ArrowRight/ArrowDown → next step, ArrowLeft/ArrowUp → previous step. Step gating (`canAdvanceFromStep`) prevents invalid navigation. | Wizard fully keyboard-navigable |
| 1.10.3 | **Color + text pairing** | ✅ Done | `frontend/src/components/vendor/VendorInventorySection.vue` + `VendorProductCard.vue` | Review checklist now uses dynamic ✅/⬜/⚠️ text indicators (not just CSS color). Inventory badges, priority strip, and flags all have text labels. | Every status has text label |
| 1.10.4 | **Field operations mode** | ✅ Done | `frontend/src/components/vendor/VendorInventorySection.vue` | Toggle button switches to field ops mode: larger fonts, bigger buttons/padding, thicker borders, higher contrast. Barcode scanner placeholder ready. | Warehouse staff can use app outdoors |
| 1.10.5 | **Offline queue for stock adjustments** | ✅ Done | `frontend/src/stores/offlineQueue.js` + `VendorInventorySection.vue` | Stock adjustments queued in localStorage when offline. Auto-sync on `online` event via `syncOfflineQueue()`. Success notification after sync. | No data loss in poor connectivity |

---

## 1.11 Backend API Gaps

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 1.11.1 | Vendor recommendations endpoint | ✅ Done | `backend/vendors/views.py` | `GET /vendors/me/recommendations/` returns aggregated task list with priorities | Frontend can consume structured recommendations |
| 1.11.2 | CSV validation endpoint | ✅ Done | `backend/catalog/views.py` | `POST /v1/products/validate_import/` parses CSV, returns `{valid_rows, total_rows, errors: [{row, message}]}` | Zero products created during validation |
| 1.11.3 | Dashboard stats enrichment | ✅ Done | `backend/catalog/views.py` | `/v1/products/dashboard-stats/` returns `active_products`, `views_this_week`, `quotes_this_month`, `conversion_rate`, `avg_response_time_hours`. | Returns full performance metrics |
| 1.11.4 | Vendor response time metric | ✅ Done | `backend/vendors/views.py` | `avg_response_time_hours` computed from `QuoteResponse.confirmed_at - QuoteRequest.requested_at` on `me()` endpoint. Also returns `unresponded_quotes_count`. | UI can display response coaching |
| 1.11.5 | Certification expiry signals | ✅ Done | `backend/catalog/signals.py` + `management/commands/check_certification_expiry.py` | `post_save` signal checks expiry on save. Daily management command `python manage.py check_certification_expiry` checks all certs and notifies vendors. | Proactive cert expiry alerts |

---

# 2. PROPERTY MODULE

**Blueprint:** `PROPERTY_MODULE_WORKFLOW_UX_TRANSFORM.md`  
**Frontend Root:** `frontend/src/components/property/`, `frontend/src/views/PropertyManagerDashboard.vue`, `frontend/src/views/PropertyEdit.vue`, `frontend/src/views/PropertyListing.vue`, `frontend/src/views/PropertyDetail.vue`  
**Backend Root:** `backend/property/`

---

## 2.1 Property Publishing & Listing Creation

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 2.1.1 | Multi-section edit wizard | ✅ Done | `frontend/src/views/PropertyEdit.vue` | 6 workflow sections: Listing Basics, Specification, Commercials, Readiness, Media & Documents, Ownership. Left nav rail with completion state. | Sections clickable, completion tracked |
| 2.1.2 | Draft auto-save | ✅ Done | `frontend/src/views/PropertyEdit.vue` | `localStorage` key `pz-property-edit-draft:${id}` stores form state. Restored on return. | Draft restored message shown |
| 2.1.3 | Workflow banner with blockers | ✅ Done | `frontend/src/views/PropertyEdit.vue` | `workflowCompletion` computed: completeCount, totalCount, percent, nextSectionId, blockers. Banner shows next recommended section. | Banner updates as sections are completed |
| 2.1.4 | Section-level blocker detection | ✅ Done | `frontend/src/views/PropertyEdit.vue` | `sectionNeedsAttention()` computes completeness per section. Blockers listed in banner. | Missing fields surfaced as chips |
| 2.1.5 | Property creation modal | ✅ Done | `frontend/src/views/PropertyManagerDashboard.vue` | `PUBLISH_PROPERTY_LISTING` modal with grouped form sections. POSTs to `/property/`. | Modal creates property with nested data |
| 2.1.6 | Media upload (images + documents) | ✅ Done | `frontend/src/views/PropertyManagerDashboard.vue` + `PropertyEdit.vue` | File input queues images/docs, uploads after property ID is returned. | Media attached to property |
| 2.1.7 | **Step-level validation gating** | ❌ Missing | `frontend/src/views/PropertyEdit.vue` | Add `canAdvanceToSection(sectionId)` function. Listing Basics requires title + location + price. Commercials requires asking_price. Publish button disabled until core fields complete. | Cannot navigate past incomplete required sections |
| 2.1.8 | **Readiness score in creation modal** | ❌ Missing | `frontend/src/views/PropertyManagerDashboard.vue` | Add real-time readiness meter (0–100) to creation modal based on filled fields. | Score visible during creation |
| 2.1.9 | **Template-based creation** | ❌ Missing | `frontend/src/views/PropertyManagerDashboard.vue` | Offer templates: Residential, Commercial, Land, Mixed-Use. Selecting template pre-fills common feature groups. | Template selection accelerates creation |
| 2.1.10 | **Map location picker** | ❌ Missing | `frontend/src/views/PropertyEdit.vue` | Replace text address fields with interactive map for lat/lng selection. Fallback to text. | Map shows property location, draggable pin |
| 2.1.11 | **Document categorization** | 🔄 Partial | `frontend/src/views/PropertyEdit.vue` | Files upload but lack structured categories (deed, floor plan, compliance cert). Add document type selector per file. | Each document labeled: Deed, Floor Plan, Compliance, etc. |

---

## 2.2 Property Discovery (Public Browsing)

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 2.2.1 | Search hero with full-text | ✅ Done | `frontend/src/views/PropertyListing.vue` | `EntryHero` queries title, place, feature, development profile. | Search returns relevant results |
| 2.2.2 | Rich filter rail | ✅ Done | `frontend/src/views/PropertyListing.vue` | 15+ filters: country, location, asset type, purpose, listing type, development stage, status, bedrooms, bathrooms, occupancy, condition, budget range, pricing strategy, financing ready, build ready. | All filters functional |
| 2.2.3 | Geo-radius search | ✅ Done | `frontend/src/views/PropertyListing.vue` | "Use My Location" + "Near Me" pill. Backend bounding-box filter on lat/lng. | Radius search returns nearby properties |
| 2.2.4 | Property cards with readiness | ✅ Done | `frontend/src/components/property/PropertyMarketCard.vue` | Card shows image, badges, price, location, bed/bath/stage, features, readiness bar, owner, actions. | Cards render consistently |
| 2.2.5 | Shortlist (heart icon) | ✅ Done | `frontend/src/views/PropertyListing.vue` | Persisted to `localStorage`. Heart toggle on cards. | Shortlist survives refresh |
| 2.2.6 | Compare (up to 4 properties) | ✅ Done | `frontend/src/views/PropertyListing.vue` | Compare modal with side-by-side table. Persisted to `localStorage`. | Comparison shows key specs |
| 2.2.7 | Workflow banner on search page | ✅ Done | `frontend/src/views/PropertyListing.vue` | `searchWorkflowSummary` + `searchWorkflowSteps`: Narrow → Compare → Open. | Buyers guided through discovery |
| 2.2.8 | **Filter guidance / empty state recovery** | ❌ Missing | `frontend/src/views/PropertyListing.vue` | If no results, show "Try broader filters" with specific suggestions: "Remove condition filter" or "Expand radius to 50km". | Empty state suggests filter changes |
| 2.2.9 | **Map view toggle** | ❌ Missing | `frontend/src/views/PropertyListing.vue` | Toggle between list view and map view. Map pins show price + type. | Map renders property pins |
| 2.2.10 | **Property card next-best-action for buyer** | ❌ Missing | `frontend/src/components/property/PropertyMarketCard.vue` | Card actions should vary by property state: `Book Visit` (if slots available), `Inquire` (if inquiries enabled), `Notify Me` (if no slots), `View Finance` (if financing allowed). | Action matches property capability |
| 2.2.11 | **Saved search alerts** | ❌ Missing | `frontend/src/views/PropertyListing.vue` + backend | "Save this search" button. Backend `SavedSearch` model emails when new matching properties are published. | User gets alert for new matches |

---

## 2.3 Property Detail Page

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 2.3.1 | Image slider / gallery | ✅ Done | `frontend/src/views/PropertyDetail.vue` | Multi-image slider with prev/next, dots, counter. Single image fallback. | Gallery navigable |
| 2.3.2 | Hero with price, location, badges | ✅ Done | `frontend/src/views/PropertyDetail.vue` | Title, asset_type badge, status badge, price, location, summary stats, features. | Key info above fold |
| 2.3.3 | Workflow banner (context-aware) | ✅ Done | `frontend/src/views/PropertyDetail.vue` | `workflowBanner` computed based on operator mode, visit ready, inquiry ready, finance ready. | Banner adapts to user role + property state |
| 2.3.4 | Operational readiness card | ✅ Done | `frontend/src/views/PropertyDetail.vue` | Score, next step, blockers count, unlocks. Blocker chips listed. | Health visible to operators |
| 2.3.5 | Quick actions strip | ✅ Done | `frontend/src/views/PropertyDetail.vue` | Dynamic CTA buttons based on workflow state. | Actions match capability |
| 2.3.6 | Tabbed content | ✅ Done | `frontend/src/views/PropertyDetail.vue` | Overview, Specs, Financials, Links tabs. | Content organized |
| 2.3.7 | Sidebar tabs (showings, status, inquiry, financing, operator) | ✅ Done | `frontend/src/views/PropertyDetail.vue` | Showings list, availability snapshot, inquiry form, financing application, operator feed. | All side tabs functional |
| 2.3.8 | Booking flow (slot picker + form) | ✅ Done | `frontend/src/views/PropertyDetail.vue` | Visitor selects slot from computed availability, fills form, POSTs `/property/appointments/`. | Booking creates appointment + chat room |
| 2.3.9 | Inquiry form | ✅ Done | `frontend/src/views/PropertyDetail.vue` | full_name, email, phone, inquiry_type, message. POSTs `/property/inquiries/`. | Inquiry creates thread + notifies operators |
| 2.3.10 | Financing application hook | ✅ Done | `frontend/src/views/PropertyDetail.vue` | Financing tab links to `/v3/finance/applications/`. | Finance flow accessible |
| 2.3.11 | Activity timeline | ✅ Done | `frontend/src/views/PropertyDetail.vue` | `PropertyActivityTimeline` rendered with `propertyTimeline` computed from status + inquiries + appointments + projects. | Timeline visible on detail page |
| 2.3.12 | Suggested materials cross-sell | ✅ Done | `frontend/src/views/PropertyDetail.vue` | Fetches `/v1/products/` and shows up to 3 products in "Suggested Materials". | Products shown for renovation/development properties |
| 2.3.13 | **Buyer trust signals** | ❌ Missing | `frontend/src/views/PropertyDetail.vue` | Show owner/manager verification badge, response time average, inquiry response rate, listing freshness ("Updated 3 days ago"). | Buyer can assess trust before contacting |
| 2.3.14 | **"Notify me when available"** | ❌ Missing | `frontend/src/views/PropertyDetail.vue` | If property has no visit slots OR is not ACTIVE, show "Notify me when available" email capture. Backend `PropertyInterest` model. | Buyer can register interest on blocked properties |
| 2.3.15 | **Similar properties recommendation** | ❌ Missing | `frontend/src/views/PropertyDetail.vue` + backend | Backend endpoint `/property/{id}/similar/` returns 3 properties by same asset_type + location + price range. | Similar properties shown below fold |
| 2.3.16 | **Project linkage CTA** | 🔄 Partial | `frontend/src/views/PropertyDetail.vue` | `POST /property/<id>/link-project/` exists but CTA is not prominent. Surface "Link to Project" when property is development-ready. | Project linkage visible to owner |
| 2.3.17 | **Visit slot availability real-time** | 🔄 Partial | `frontend/src/views/PropertyDetail.vue` | Slots computed from windows minus bookings, but no real-time SSE/WebSocket update when slot is taken. | Slot availability updates without refresh |

---

## 2.4 Property Manager / Owner Dashboard

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 2.4.1 | Dashboard shell with sidebar | ✅ Done | `frontend/src/views/PropertyManagerDashboard.vue` | `DashboardShell` with sections: listings, availability, leads, appointments, verification. | Sections switch correctly |
| 2.4.2 | Workflow banner (4 steps) | ✅ Done | `frontend/src/views/PropertyManagerDashboard.vue` | Create Listing → Publish Availability → Respond to Leads → Link to Project. Steps dynamically marked done/active. | Banner reflects portfolio state |
| 2.4.3 | Operations snapshot | ✅ Done | `frontend/src/views/PropertyManagerDashboard.vue` | Urgent actions count + health summary (healthy / needs attention / blocked). Overview metrics clickable. | Snapshot surfaces priorities |
| 2.4.4 | Managed properties table | ✅ Done | `frontend/src/views/PropertyManagerDashboard.vue` | Row per property: title, availability toggles, commercial, readiness, action link. | Table navigates to detail/edit |
| 2.4.5 | Property health score | ✅ Done | `frontend/src/views/PropertyManagerDashboard.vue` | `getPropertyHealthScore(item)` 0–100 based on title, location, price, description, media, inquiry/appointment enabled, pricing strategy, development stage, ownership. | Score accurate per property |
| 2.4.6 | Health labels | ✅ Done | `frontend/src/views/PropertyManagerDashboard.vue` | `getPropertyHealth(item)` returns Ready / Nearly Ready / Needs Work / Blocked. | Label matches score |
| 2.4.7 | Workspace health score | ✅ Done | `frontend/src/views/PropertyManagerDashboard.vue` | `workspaceHealthScore` averages all managed properties. | Portfolio health visible |
| 2.4.8 | Urgent actions computed | ✅ Done | `frontend/src/views/PropertyManagerDashboard.vue` | `urgentActions` lists: complete listing, review leads, review appointments (max 3). | Actions prioritized by severity |
| 2.4.9 | Notification panel + timeline tabs | ✅ Done | `frontend/src/views/PropertyManagerDashboard.vue` | `PropertyNotificationPanel` + `PropertyActivityTimeline` in tabbed card. | Alerts and timeline switchable |
| 2.4.10 | Leads grid | ✅ Done | `frontend/src/views/PropertyManagerDashboard.vue` | Incoming inquiries with name, property, inquiry_type. | Leads visible |
| 2.4.11 | Appointments list | ✅ Done | `frontend/src/views/PropertyManagerDashboard.vue` | Scheduled appointments with property title and datetime. | Appointments visible |
| 2.4.12 | **Role-based dashboard variants** | ✅ Done | `frontend/src/views/PropertyManagerDashboard.vue` | Reused for `/property-manager/dashboard`, `/agent/dashboard`, `/surveyor/dashboard`. Capabilities vary by role. | Agent can create, surveyor cannot |
| 2.4.13 | **Goal-based navigation redesign** | ❌ Missing | `frontend/src/views/PropertyManagerDashboard.vue` | Rename sections: Publish Property → Review Leads → Book Visits → Check Finance Readiness → Link to Project. | Navigation labels reflect intent |
| 2.4.14 | **Portfolio performance metrics** | ❌ Missing | `frontend/src/views/PropertyManagerDashboard.vue` + backend | Add stats: total views, inquiries this month, appointments booked, conversion rate. Fetch from backend analytics. | Metrics strip visible |
| 2.4.15 | **Property grouping by operational state** | ❌ Missing | `frontend/src/views/PropertyManagerDashboard.vue` | Group properties: Needs Attention (incomplete/blockers), Active & Healthy, Drafts, Archived. Not raw table. | Cards grouped by health |
| 2.4.16 | **Next-best-action recommendations** | ❌ Missing | `frontend/src/views/PropertyManagerDashboard.vue` | Recommendation cards: "Add visit slots to [Property] — buyers cannot book yet", "Respond to inquiry from [Name] — waiting 2 days", "Upload deed to unlock finance review". | Recommendations consume backend tasks |
| 2.4.17 | **Bulk actions** | ❌ Missing | `frontend/src/views/PropertyManagerDashboard.vue` | Checkbox select properties → bulk publish/unpublish, bulk archive, bulk assign manager. | Multi-property operations |
| 2.4.18 | **Approval queue UI** | ❌ Missing | `frontend/src/views/PropertyManagerDashboard.vue` or new admin view | Admin/surveyor sees pending properties with Approve/Reject/Request Changes actions + notes. | Approval workflow has dedicated UI |

---

## 2.5 Inquiry & Appointment Management

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 2.5.1 | Inquiry creation with auto chat room | ✅ Done | Backend: `PropertyInquiryViewSet` | Creating inquiry auto-creates `ChatRoom` with owner + manager + visitor. | Chat thread ready immediately |
| 2.5.2 | Appointment booking with auto chat room | ✅ Done | Backend: `PropertyAppointmentViewSet` | Booking auto-creates `ChatRoom` with participants. | Chat thread ready immediately |
| 2.5.3 | Availability windows | ✅ Done | Backend: `PropertyAvailabilityWindow` + frontend modal | Manager publishes recurring windows. Slots computed as windows minus bookings. | Slots visible to public |
| 2.5.4 | Operator notification on inquiry/appointment | ✅ Done | Backend: `notify_property_operators()` | Sends `Notification.Type.SYSTEM` to owner/manager. | Operators notified |
| 2.5.5 | Inquiry status tracking | 🔄 Partial | Backend: `PropertyInquiry.status` | Status field exists but workflow states (NEW → IN_PROGRESS → RESPONDED → CLOSED) may not be fully enforced. | Clear status lifecycle |
| 2.5.6 | **Inquiry response time coaching** | ❌ Missing | `frontend/src/views/PropertyManagerDashboard.vue` | Show "You respond in X hours on average" and "Responding within 24h increases conversion by Y%". | Coaching visible on leads tab |
| 2.5.7 | **Overdue inquiry escalation** | ❌ Missing | `frontend/src/views/PropertyManagerDashboard.vue` + backend | Inquiry > 48h old gets red highlight + "Urgent — buyer may go elsewhere" banner. Auto-notification to manager. | Stale inquiries visually escalated |
| 2.5.8 | **Appointment confirmation flow** | 🔄 Partial | Backend: `PropertyAppointment.status` | Status exists but no explicit "Confirm Booking" action in operator UI. Add Confirm / Reschedule / Cancel buttons. | Operator can manage bookings |
| 2.5.9 | **Visit outcome capture** | ❌ Missing | `frontend/src/views/PropertyManagerDashboard.vue` | After visit, operator records outcome: Interested / Not Interested / Follow-up Required. Updates lead status. | Visit result tracked |

---

## 2.6 Timeline & Notifications

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 2.6.1 | Activity timeline component | ✅ Done | `frontend/src/components/property/PropertyActivityTimeline.vue` | Accepts `events` prop, renders chronologically with variant styling (success/warn/info). | Timeline renders events |
| 2.6.2 | Frontend-computed timeline | ✅ Done | `frontend/src/views/PropertyDetail.vue` + `PropertyManagerDashboard.vue` | `propertyTimeline` computed from status + inquiries + appointments + linked projects. | Timeline populates from related data |
| 2.6.3 | Notification panel component | ✅ Done | `frontend/src/components/property/PropertyNotificationPanel.vue` | Accepts `notifications` prop, renders unread count, icons, titles, messages, CTAs. | Panel renders alerts |
| 2.6.4 | Frontend-computed notifications | ✅ Done | `frontend/src/views/PropertyManagerDashboard.vue` | `propertyNotifications` computed from inquiries (unread), appointments, low-health properties. | Notifications populates from data |
| 2.6.5 | **Backend event-sourced timeline** | ❌ Missing | Backend: new `PropertyEvent` model | Persist events: `PROPERTY_CREATED`, `PUBLISHED`, `INQUIRY_RECEIVED`, `INQUIRY_REPLIED`, `SLOT_ADDED`, `VISIT_BOOKED`, `FINANCE_REVIEW_STARTED`, `PROJECT_LINKED`, `ARCHIVED`. | Timeline survives page refresh |
| 2.6.6 | **Persistent notification model** | ❌ Missing | Backend: extend `Notification` or create `PropertyNotification` | Store property-specific notifications with read status, deep links, action metadata. | Notifications persist across sessions |
| 2.6.7 | **Real-time notification delivery** | 🔄 Partial | `frontend/src/stores/notifications.js` | WebSocket exists but property-specific events may not push through same channel. Ensure `notify_property_operators` pushes to WebSocket. | Notifications arrive in real time |

---

## 2.7 Empty States & Guided States

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 2.7.1 | No properties empty state | ✅ Done | `frontend/src/views/PropertyManagerDashboard.vue` | `EmptyState` component: icon 🏠, title "No properties yet", description, next-step, action CTA. | Guided empty state |
| 2.7.2 | No appointments empty state | ✅ Done | `frontend/src/views/PropertyManagerDashboard.vue` | `EmptyState` component: icon 🗓, title "No appointments yet". | Guided empty state |
| 2.7.3 | No search results empty state | ✅ Done | `frontend/src/views/PropertyListing.vue` | Reset action visible. | User can clear filters |
| 2.7.4 | **No inquiries guided state** | ❌ Missing | `frontend/src/views/PropertyManagerDashboard.vue` | Replace generic empty with: "No one has contacted this property yet. Add media, improve description, publish availability." + CTA "Improve Listing". | Empty state teaches recovery |
| 2.7.5 | **No visit slots guided state** | ❌ Missing | `frontend/src/views/PropertyManagerDashboard.vue` | "Visitors cannot book yet. Publish visit slots so interested buyers can act now." + CTA "Add Visit Slots". | Empty state teaches recovery |
| 2.7.6 | **Unverified account blocker** | ❌ Missing | `frontend/src/views/PropertyManagerDashboard.vue` | If user lacks `property:list_property` permission, show blocker: "Your account is not verified yet. Start verification to publish." | Clear permission blocker |

---

## 2.8 Blocking & Validation UX

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 2.8.1 | Missing required fields blocker | 🔄 Partial | `frontend/src/views/PropertyEdit.vue` | Blockers listed in workflow banner but publish action is not explicitly gated. Disable publish CTA until core fields complete. | Cannot publish incomplete listing |
| 2.8.2 | No visit availability warning | ❌ Missing | `frontend/src/views/PropertyDetail.vue` (buyer view) | If `appointment_enabled=true` but no slots published, show "Buyers cannot book a visit until a slot is published." to owner. Buyer sees "No slots available — contact owner instead." | Blocker explained to both sides |
| 2.8.3 | Pending moderation state | 🔄 Partial | Backend: `PropertyListing.status` | `DRAFT` exists but no explicit moderation queue. Add `PENDING_REVIEW` status. Admin must approve before `ACTIVE`. | Moderation workflow enforced |
| 2.8.4 | Incomplete documents for finance | ❌ Missing | `frontend/src/views/PropertyDetail.vue` | If `financing_allowed=true` but missing deed/compliance docs, show "Finance review blocked until required files uploaded." | Finance blocker contextual |
| 2.8.5 | Invalid transition messages | ❌ Missing | Backend serializers + frontend | If user tries invalid status change (e.g., `DRAFT` → `SOLD`), return human message: "This property cannot move to Sold yet. Publish it first." | Human-friendly error |

---

## 2.9 Backend API Gaps

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 2.9.1 | Property analytics endpoint | ❌ Missing | `backend/property/views.py` | `GET /property/analytics/` returns views, inquiries, appointments, conversion rate per property or portfolio. | Frontend can render performance metrics |
| 2.9.2 | Similar properties endpoint | ❌ Missing | `backend/property/views.py` | `GET /property/{id}/similar/` returns 3 properties matching asset_type, location radius, price range. | Detail page shows recommendations |
| 2.9.3 | Property event log endpoint | ❌ Missing | `backend/property/views.py` | `GET /property/{id}/events/` returns persisted `PropertyEvent` records. | Timeline survives refresh |
| 2.9.4 | Manager response time metric | ❌ Missing | `backend/property/views.py` | Compute avg hours from `PropertyInquiry.created_at` to first reply in associated `ChatRoom`. | Dashboard shows response coaching |
| 2.9.5 | Approval workflow endpoint | ❌ Missing | `backend/property/views.py` | `POST /property/{id}/moderate/` with `decision: approve|reject|request_changes` + `notes`. Changes status and notifies owner. | Admin can moderate listings |
| 2.9.6 | Saved search endpoint | ❌ Missing | `backend/property/views.py` | `POST /property/saved-searches/` stores filter params. Cron checks new properties against saved searches, emails matches. | Buyers get new listing alerts |
| 2.9.7 | Property recommendation endpoint | ❌ Missing | `backend/property/views.py` | `GET /property/manager/recommendations/` returns structured tasks: incomplete listings, stale inquiries, missing slots, etc. | Dashboard consumes backend recommendations |

---

## 2.10 Cross-Module Integration

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 2.10.1 | Property → Project linkage | 🔄 Partial | Backend: `PropertyProjectLink` + frontend | Model and endpoint exist but CTA is buried. Surface prominently when property is development-ready. | One-click project creation from property |
| 2.10.2 | Property → Procurement (materials) | ✅ Done | `frontend/src/views/PropertyDetail.vue` | "Suggested Materials" fetches `/v1/products/`. | Products shown for relevant properties |
| 2.10.3 | Property → Financing | ✅ Done | `frontend/src/views/PropertyDetail.vue` | Financing tab links to finance applications. | Finance flow accessible |
| 2.10.4 | Property → Delivery/Logistics | ❌ Missing | `backend/property/models.py` + `projects` | When property is linked to active project with material orders, show delivery status in property timeline. | Delivery continuity |
| 2.10.5 | Property → Disputes | ❌ Missing | Backend + frontend | If booking/inquiry conflict arises, create dispute linked to property record. Timeline captures evidence. | Dispute linked to property |
| 2.10.6 | Property → Notifications | 🔄 Partial | Backend: `notify_property_operators()` | Sends SYSTEM notification but not through persistent property-specific channel. Route through `PropertyNotification`. | All property events notify correctly |

---

## 2.11 Mobile & Accessibility

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 2.11.1 | Responsive cards and layout | ✅ Done | `frontend/src/components/property/PropertyMarketCard.vue` | Grid collapses to single column on mobile. | Mobile layout works |
| 2.11.2 | Filter modal on mobile | ✅ Done | `frontend/src/views/PropertyListing.vue` | Filters open in modal on mobile. | Mobile filter UX functional |
| 2.11.3 | **Mobile bottom navigation** | ❌ Missing | `frontend/src/views/PropertyManagerDashboard.vue` | Bottom tabs: [📦 Portfolio] [🚀 Publish] [💬 Leads] [📅 Visits] [👤 Account]. | Thumb-reachable nav |
| 2.11.4 | **Sticky primary CTA on edit** | ❌ Missing | `frontend/src/views/PropertyEdit.vue` | On mobile, "Save Changes" button sticks to bottom of viewport during editing. | CTA always accessible |
| 2.11.5 | **Offline draft save** | 🔄 Partial | `frontend/src/views/PropertyEdit.vue` | `localStorage` draft exists but no offline indicator or sync queue. Show "Saved locally — will sync when online" badge. | User knows draft status |
| 2.11.6 | **Camera capture for media** | ❌ Missing | `frontend/src/views/PropertyEdit.vue` | Direct camera capture button for property photos. Auto-compress. | Field photography supported |

---

# 3. BUYER MODULE

**Blueprint:** `BUYER_MODULE_WORKFLOW_UX_TRANSFORM.md`  
**Frontend Root:** `frontend/src/views/BuyerDashboard.vue`, `frontend/src/views/ProductList.vue`, `frontend/src/views/ProductDetail.vue`  
**Backend Root:** `backend/orders/`, `backend/accounts/`, `backend/projects/`

---

## 3.1 Buyer Dashboard & Workspace

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 3.1.1 | Dashboard shell with sidebar | ✅ Done | `frontend/src/views/BuyerDashboard.vue` | `DashboardShell` with sections: My Orders, Quote Requests, Delivery Addresses, My Profile. | Sections switch correctly |
| 3.1.2 | Workflow banner | ✅ Done | `frontend/src/views/BuyerDashboard.vue` | Contextual banner: guest → register, no addresses → add hub, no quotes → browse, pending orders → track. | Banner adapts to buyer state |
| 3.1.3 | Quick stats | ✅ Done | `frontend/src/views/BuyerDashboard.vue` | Orders count, Quotes count, Hubs count. | Stats visible in header |
| 3.1.4 | Role activation cards | ✅ Done | `frontend/src/views/BuyerDashboard.vue` | Cards to activate Owner, Vendor, Contractor, Investor workspaces. | Cross-role navigation |
| 3.1.5 | Guest buyer support | ✅ Done | `frontend/src/views/BuyerDashboard.vue` | Dashboard accessible without auth, prompts to sign in for saving. | Guest experience graceful |
| 3.1.6 | **Goal-based navigation redesign** | ❌ Missing | `frontend/src/views/BuyerDashboard.vue` | Rename sections: Track Orders → Manage Quotes → Delivery Hubs → Saved Items → Reorder History. | Navigation reflects buyer intent |
| 3.1.7 | **Buyer performance analytics** | ❌ Missing | `frontend/src/views/BuyerDashboard.vue` + backend | Add charts: monthly spend, top vendors, average quote response time, order fulfillment rate. | Analytics visible |
| 3.1.8 | **Reorder from history** | ❌ Missing | `frontend/src/views/BuyerDashboard.vue` | "Reorder" button on completed orders. Pre-fills quote request with same items + quantities. | One-click reorder |
| 3.1.9 | **Saved searches** | ❌ Missing | `frontend/src/views/BuyerDashboard.vue` + backend | List of saved searches with "Run again" button. New matches trigger notification. | Buyer can rerun searches |

---

## 3.2 Product Discovery (Marketplace)

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 3.2.1 | Search hero | ✅ Done | `frontend/src/views/ProductList.vue` | `EntryHero` with full-text search. | Search functional |
| 3.2.2 | Rich filter rail | ✅ Done | `frontend/src/views/ProductList.vue` | Location (country, county, subcounty, radius), category, certification, origin, price range, sort, inventory status, delivery region, toggles (in-stock only, verified only). | All filters functional |
| 3.2.3 | Geo-proximity search | ✅ Done | `frontend/src/views/ProductList.vue` | "Use My Location" + radius dropdown. Backend distance sort. | Near-me search works |
| 3.2.4 | Workflow banner on search | ✅ Done | `frontend/src/views/ProductList.vue` | Steps: Search → Compare → Quote → Order. Metrics: visible products, compare queue, active filters. | Buyers guided through discovery |
| 3.2.5 | Product grid with cards | ✅ Done | `frontend/src/views/ProductList.vue` | Grid/list toggle, skeleton loading, pagination/infinite scroll. | Products render efficiently |
| 3.2.6 | **Compare queue (ephemeral)** | ✅ Done | `frontend/src/views/ProductList.vue` | Bottom sticky bar, max 4 products, comparison modal with side-by-side specs. | Comparison works per session |
| 3.2.7 | **Trust signals on cards** | 🔄 Partial | `frontend/src/views/ProductList.vue` | Cards show price + stock status. Missing: vendor health score, response time, cert count. | Buyer can assess trust at glance |
| 3.2.8 | **Shortlist / Favorites** | ❌ Missing | `frontend/src/views/ProductList.vue` + `ProductDetail.vue` + backend | Heart icon on cards and detail. Backend `BuyerShortlist` model: `{buyer, product, added_at, notes}`. | Items persist across sessions |
| 3.2.9 | **Persistent comparison** | ❌ Missing | Backend: `BuyerComparison` model + frontend | Save compare sets to backend. Name them (e.g., "Cement Options"). Reopen later. | Comparisons survive refresh |
| 3.2.10 | **Filter guidance on no results** | ❌ Missing | `frontend/src/views/ProductList.vue` | If zero results, suggest: "Try removing certification filter" or "Expand radius to 50km". | Empty state teaches recovery |
| 3.2.11 | **Vendor discovery page** | ❌ Missing | `frontend/src/views/VendorDirectory.vue` (new) | Browse vendors by category, location, rating. View vendor profile with catalog, health score, response time. | Buyers can discover by supplier |
| 3.2.12 | **Price history indicator** | ❌ Missing | `frontend/src/views/ProductList.vue` + backend | Backend tracks price changes. Show "Price dropped 10% this month" badge. | Buyers spot deals |

---

## 3.3 Product Detail Page

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 3.3.1 | Image gallery | ✅ Done | `frontend/src/views/ProductDetail.vue` | Main image + thumbnail strip. | Gallery navigable |
| 3.3.2 | Trust strip | ✅ Done | `frontend/src/views/ProductDetail.vue` | Verified Supplier badge, certification count, Featured, New Arrival. | Trust signals visible |
| 3.3.3 | Price + bulk pricing | ✅ Done | `frontend/src/views/ProductDetail.vue` | Base price, bulk price, unit, currency. | Pricing clear |
| 3.3.4 | Quantity selector | ✅ Done | `frontend/src/views/ProductDetail.vue` | Minus/plus buttons with min/max bounds. | Quantity control works |
| 3.3.5 | Request Quote CTA | ✅ Done | `frontend/src/views/ProductDetail.vue` | Disabled if OUT_OF_STOCK. Posts to `/orders/quote-requests/`. | Quote request functional |
| 3.3.6 | Certifications banner | ✅ Done | `frontend/src/views/ProductDetail.vue` | Lists certification name, issuing body, status. | Certs prominent |
| 3.3.7 | Specification tabs | ✅ Done | `frontend/src/views/ProductDetail.vue` | Overview, Specs, Logistics tabs. | Content organized |
| 3.3.8 | **Vendor scorecard** | ❌ Missing | `frontend/src/views/ProductDetail.vue` | Expandable vendor card: health score, avg response time, fulfillment rate, total reviews, rating. | Buyer can assess vendor |
| 3.3.9 | **"Notify me when available"** | ❌ Missing | `frontend/src/views/ProductDetail.vue` + backend | If OUT_OF_STOCK, show email capture: "Notify me when [Product] is back in stock." Backend `ProductInterest` model. | Buyer registers interest |
| 3.3.10 | **"Find similar materials"** | ❌ Missing | `frontend/src/views/ProductDetail.vue` + backend | Below fold, show 3 similar products by category + price range. Endpoint: `/v1/products/{id}/similar/`. | Alternatives visible |
| 3.3.11 | **Add to shortlist** | ❌ Missing | `frontend/src/views/ProductDetail.vue` | Heart toggle next to quote button. Syncs with `BuyerShortlist`. | Shortlist from detail page |
| 3.3.12 | **Price anomaly flag for buyer** | ❌ Missing | `frontend/src/views/ProductDetail.vue` | If price is >20% below category median, show "Price is unusually low — verify quality with vendor." | Buyer warned of suspicious pricing |
| 3.3.13 | **Delivery cost estimator** | 🔄 Partial | `frontend/src/views/ProductDetail.vue` | Shows delivery regions but no cost calculation. Add logistics calculator based on buyer's default address. | Estimated delivery cost visible |

---

## 3.4 Quote Request Flow

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 3.4.1 | Single-product quote request | ✅ Done | `frontend/src/views/ProductDetail.vue` + `frontend/src/views/ProductList.vue` | POST `/orders/quote-requests/` with product + quantity. | Quote created |
| 3.4.2 | Quote request from comparison | ✅ Done | `frontend/src/views/ProductList.vue` | "Quote" button in comparison modal. | Quote from compare works |
| 3.4.3 | Buyer quote inbox | ✅ Done | `frontend/src/views/BuyerDashboard.vue` | Lists quote requests with status badges. Shows vendor responses with price + delivery fee. | Quotes visible |
| 3.4.4 | Accept & checkout | ✅ Done | `frontend/src/views/BuyerDashboard.vue` | Opens checkout modal with payment gateway selection. Posts `/orders/quote-requests/{id}/checkout/`. | Order created from accepted quote |
| 3.4.5 | **Multi-item quote cart** | ❌ Missing | `frontend/src/views/ProductList.vue` + `frontend/src/views/BuyerDashboard.vue` + backend | "Add to Quote Cart" button. Cart sidebar shows multiple items. One quote request with multiple `QuoteItem`s. | Buyer can bundle materials in one request |
| 3.4.6 | **Quote request from project BOM** | ❌ Missing | `frontend/src/views/ProjectDetail.vue` + backend | "Request Quotes for Materials" button on project. Auto-creates quote request from all MATERIAL requirements. | Project → procurement seamless |
| 3.4.7 | **Quote expiration warning** | ❌ Missing | `frontend/src/views/BuyerDashboard.vue` | If `QuoteResponse.expires_at` is within 24h, show "This quote expires soon — accept or it will lapse." | Urgency communicated |
| 3.4.8 | **Quote response time estimate** | ❌ Missing | `frontend/src/views/BuyerDashboard.vue` | Show "Vendor typically responds in X hours" when quote is pending. | Buyer knows expected wait |

---

## 3.5 Order Placement & Tracking

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 3.5.1 | Order table | ✅ Done | `frontend/src/views/BuyerDashboard.vue` | Table: Order ID, Vendor, Amount, Payment Status, Fulfillment Status, Actions. | Orders visible |
| 3.5.2 | Order actions | ✅ Done | `frontend/src/views/BuyerDashboard.vue` | Confirm Delivery, Rate Vendor, Cancel Order, Simulate Payment, Track Delivery, Chat, Dispute. | Actions context-aware |
| 3.5.3 | Checkout modal | ✅ Done | `frontend/src/views/BuyerDashboard.vue` | Payment gateway selection, order summary, confirm. | Checkout functional |
| 3.5.4 | Delivery tracking modal | ✅ Done | `frontend/src/views/BuyerDashboard.vue` | `LogisticsTracker` with shipment events. | Tracking visible |
| 3.5.5 | Post-order rating | ✅ Done | `frontend/src/views/BuyerDashboard.vue` | Rating modal posts to `/reviews/ratings/`. | Rating captured |
| 3.5.6 | Order chat | ✅ Done | `frontend/src/views/BuyerDashboard.vue` | `ChatWindow` opens per-order chat room. | Buyer-vendor chat accessible |
| 3.5.7 | **Order detail page** | ❌ Missing | `frontend/src/views/OrderDetail.vue` (new) | Dedicated order page: timeline, items, payments, tracking map, chat thread, documents. | Deep-linkable order view |
| 3.5.8 | **Fulfillment timeline** | 🔄 Partial | `frontend/src/views/BuyerDashboard.vue` | Status badges shown but no visual timeline (PLACED → CONFIRMED → PACKING → SHIPPED → DELIVERED → COMPLETED). | Timeline visualizes progress |
| 3.5.9 | **Delayed delivery escalation** | ❌ Missing | `frontend/src/views/BuyerDashboard.vue` + backend | If `estimated_delivery_at` passed + status not DELIVERED, show "Your order is delayed. Contact support or view recovery options." | Delays proactively surfaced |
| 3.5.10 | **Bulk order actions** | ❌ Missing | `frontend/src/views/BuyerDashboard.vue` | Checkbox select orders → bulk download invoices, bulk track. | Multi-order operations |

---

## 3.6 Shortlist, Comparison & Decision Support

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 3.6.1 | Ephemeral compare queue | ✅ Done | `frontend/src/views/ProductList.vue` | Max 4 products, sticky bottom bar, comparison modal. | Compare works per session |
| 3.6.2 | **Persistent shortlist** | ❌ Missing | Backend: `BuyerShortlist` model + frontend | Heart icon on cards/detail. Saved to backend. Dashboard section: "Saved Items". | Shortlist persists |
| 3.6.3 | **Persistent comparison sets** | ❌ Missing | Backend: `BuyerComparison` model + frontend | Save compare sets with name. Reopen from dashboard. | Comparisons survive refresh |
| 3.6.4 | **Decision matrix scoring** | ❌ Missing | `frontend/src/views/ProductList.vue` | In comparison modal, highlight best value (lowest price per unit), fastest delivery, highest cert count. | Comparison aids decision |
| 3.6.5 | **Quote comparison matrix** | ❌ Missing | `frontend/src/views/BuyerDashboard.vue` | If multiple vendors responded to same quote request, show matrix: Vendor | Price | Delivery | Response Time | Certifications | Rating. | Buyers compare responses side-by-side |

---

## 3.7 Project / BOM Integration

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 3.7.1 | Project creation | ✅ Done | `frontend/src/views/CreateProject.vue` | Form: title, description, location, budget, funding flag. | Project created |
| 3.7.2 | Project detail workspace | ✅ Done | `frontend/src/views/ProjectDetail.vue` | Tabs: Overview, Requirements, Contracts, Milestones, Funding, Documents, Updates, Risks, Activity. | Project workspace functional |
| 3.7.3 | Material suggestions from project | ✅ Done | `frontend/src/components/projects/ProjectMaterialSuggestions.vue` | Fetches `/v4/projects/{id}/suggest-products/` based on MATERIAL requirements. | Products suggested |
| 3.7.4 | **Structured BOM builder** | ❌ Missing | `frontend/src/views/ProjectDetail.vue` + backend | Replace plain-text requirements with structured BOM: item name, quantity, unit, spec, category. Auto-match to catalog products. | BOM is structured and actionable |
| 3.7.5 | **Convert BOM to quote request** | ❌ Missing | `frontend/src/views/ProjectDetail.vue` + backend | "Request Quotes for All Materials" button. Creates multi-item quote request from BOM. | One-click procurement from project |
| 3.7.6 | **Link orders to projects** | ❌ Missing | Backend: `Order.project` FK + frontend | When placing order from project-linked quote, auto-associate order with project. Show order in project timeline. | Project tracks procurement |

---

## 3.8 Backend API Gaps

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 3.8.1 | Buyer shortlist endpoints | ❌ Missing | `backend/accounts/views.py` or new app | `GET/POST/DELETE /accounts/shortlist/` CRUD for `BuyerShortlist`. | Frontend can save/retrieve shortlist |
| 3.8.2 | Buyer comparison endpoints | ❌ Missing | `backend/accounts/views.py` | `GET/POST/DELETE /accounts/comparisons/` CRUD for `BuyerComparison`. | Frontend can save compare sets |
| 3.8.3 | Product similar endpoint | ❌ Missing | `backend/catalog/views.py` | `GET /v1/products/{id}/similar/` returns 3 products by category + price range. | Detail page shows alternatives |
| 3.8.4 | Product interest / notify endpoint | ❌ Missing | `backend/catalog/views.py` | `POST /v1/products/{id}/notify-me/` creates `ProductInterest` with email. | Back-in-stock notifications |
| 3.8.5 | Buyer analytics endpoint | ❌ Missing | `backend/orders/views.py` | `GET /orders/buyer-analytics/` returns spend by month, top vendors, avg quote response time, fulfillment rate. | Dashboard renders charts |
| 3.8.6 | Quote cart / multi-item quote | ❌ Missing | `backend/orders/views.py` | `POST /orders/quote-requests/` already accepts items array, but frontend doesn't build multi-item carts. Ensure backend validates multi-item properly. | Multi-item quotes work end-to-end |
| 3.8.7 | Saved search endpoints | ❌ Missing | `backend/catalog/views.py` | `POST /v1/products/saved-searches/` stores filter params. Cron emails matches. | Buyers get new listing alerts |

---

## 3.9 Mobile & Accessibility

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 3.9.1 | Responsive filter modal | ✅ Done | `frontend/src/views/ProductList.vue` | Filters collapse to modal on mobile. | Mobile filter UX works |
| 3.9.2 | Responsive product grid | ✅ Done | `frontend/src/views/ProductList.vue` | Grid adjusts columns based on viewport. | Mobile layout works |
| 3.9.3 | **Sticky quote cart on mobile** | ❌ Missing | `frontend/src/views/ProductList.vue` | Bottom sheet showing quote cart items with "Request Quote" button. | Cart always accessible |
| 3.9.4 | **Mobile bottom nav** | ❌ Missing | `frontend/src/views/BuyerDashboard.vue` | Bottom tabs: [🔍 Discover] [💬 Quotes] [📦 Orders] [❤️ Saved] [👤 Account]. | Thumb-reachable nav |
| 3.9.5 | **Swipe actions on orders** | ❌ Missing | `frontend/src/views/BuyerDashboard.vue` | Swipe left on order: Track. Swipe right: Chat. | Quick mobile actions |

---

# 4. OWNER MODULE

**Blueprint:** `OWNER_MODULE_WORKFLOW_UX_TRANSFORM.md`  
**Frontend Root:** `frontend/src/views/OwnerDashboard.vue`, `frontend/src/views/CreateProject.vue`, `frontend/src/views/ProjectDetail.vue`, `frontend/src/views/PostContract.vue`, `frontend/src/views/ContractDetail.vue`  
**Backend Root:** `backend/projects/`, `backend/contracts/`, `backend/bids/`, `backend/milestones/`, `backend/escrow/`

---

## 4.1 Owner Dashboard & Workspace

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 4.1.1 | Dashboard shell with sidebar | ✅ Done | `frontend/src/views/OwnerDashboard.vue` | `DashboardShell` with sections: Overview, My Properties, Quote Requests, Payments, Activity Logs. | Sections switch correctly |
| 4.1.2 | Workflow banner | ✅ Done | `frontend/src/views/OwnerDashboard.vue` | Contextual banner adapts to project/quote state. | Banner guides owner |
| 4.1.3 | Quick stats | ✅ Done | `frontend/src/views/OwnerDashboard.vue` | Projects count, Quote Requests count, Portfolio Updates count. | Stats visible |
| 4.1.4 | Projects tab | ✅ Done | `frontend/src/views/OwnerDashboard.vue` | Stats cards (Total Investment, Active Projects, Funding Projects), Active Project Units list, Recent Project Updates table. | Projects visible |
| 4.1.5 | Properties tab | ✅ Done | `frontend/src/views/OwnerDashboard.vue` | Lazy-loaded `PropertiesSection` with `scope="mine"`. | Properties visible |
| 4.1.6 | Quotes tab | ✅ Done | `frontend/src/views/OwnerDashboard.vue` | Quote request list with items and vendor responses. | Quotes trackable |
| 4.1.7 | Quick actions | ✅ Done | `frontend/src/views/OwnerDashboard.vue` | Start New Project, Post a Tender, Exit Dashboard. | Actions in sidebar |
| 4.1.8 | **Escrow/Payments tab (real data)** | ❌ Missing | `frontend/src/views/OwnerDashboard.vue` + backend | Currently hardcoded mock data. Replace with real fetch from `/escrow/`. Show: Total Escrow, Pending Releases, Completed Releases, Transaction History. | Real financial data |
| 4.1.9 | **Activity Logs tab (real data)** | ❌ Missing | `frontend/src/views/OwnerDashboard.vue` + backend | Currently hardcoded mock logs. Replace with real activity feed from persistent event log. | Real activity timeline |
| 4.1.10 | **Goal-based navigation** | ❌ Missing | `frontend/src/views/OwnerDashboard.vue` | Rename: Overview → My Projects, Quote Requests → Procurement, Payments → Escrow & Releases, Activity Logs → Timeline. | Navigation reflects intent |
| 4.1.11 | **Portfolio health snapshot** | ❌ Missing | `frontend/src/views/OwnerDashboard.vue` | Card showing: projects on track, projects at risk, overdue milestones, pending releases, open bids. | Health visible at glance |
| 4.1.12 | **Urgent actions strip** | ❌ Missing | `frontend/src/views/OwnerDashboard.vue` | Priority strip: "Milestone waiting approval", "Bid deadline in 2 days", "Escrow release pending". | Urgent items surfaced first |

---

## 4.2 Project Creation

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 4.2.1 | Project creation form | ✅ Done | `frontend/src/views/CreateProject.vue` | Fields: title, description, location (map picker), estimated budget, funding required checkbox. | Project created successfully |
| 4.2.2 | Workflow banner | ✅ Done | `frontend/src/views/CreateProject.vue` | 4-step banner: Project basics → Location → Budget → Submit. | Banner guides creation |
| 4.2.3 | Live preview sidebar | ✅ Done | `frontend/src/views/CreateProject.vue` | Shows owner, status, location, budget, and "What happens next" explainer. | Preview updates live |
| 4.2.4 | **True multi-step wizard** | ❌ Missing | `frontend/src/views/CreateProject.vue` or new `ProjectCreateWizard.vue` | Extract to reusable wizard component with step persistence. Steps: 1) Scope & Basics, 2) Location & Site, 3) Budget & Timeline, 4) Team & Documents, 5) Review & Publish. | Wizard saves draft between steps |
| 4.2.5 | **Project templates** | ❌ Missing | `frontend/src/views/CreateProject.vue` | Offer templates: Residential Build, Commercial Development, Infrastructure, Renovation. Template pre-fills description, requirements categories, typical milestones. | Templates accelerate creation |
| 4.2.6 | **Document upload on creation** | ❌ Missing | `frontend/src/views/CreateProject.vue` | Allow attaching site plans, permits, feasibility studies during creation. | Documents attached at creation |
| 4.2.7 | **Team invitation on creation** | ❌ Missing | `frontend/src/views/CreateProject.vue` + backend | Invite project manager, engineer, QS by email. Backend sends invitation links. | Team assembled during setup |

---

## 4.3 Project Workspace (ProjectDetail.vue)

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 4.3.1 | Hero section | ✅ Done | `frontend/src/views/ProjectDetail.vue` | Cover image, title, description, status badge, budget, location, summary stats. | Hero informative |
| 4.3.2 | Workflow banner | ✅ Done | `frontend/src/views/ProjectDetail.vue` | Contextual next actions based on project state. | Banner adapts |
| 4.3.3 | Overview tab | ✅ Done | `frontend/src/views/ProjectDetail.vue` | Execution state, progress %, health signals. | Overview visible |
| 4.3.4 | Requirements tab | ✅ Done | `frontend/src/views/ProjectDetail.vue` | Add/remove material/contractor/service requirements. | Requirements manageable |
| 4.3.5 | Contracts tab | ✅ Done | `frontend/src/views/ProjectDetail.vue` | Link/unlink contracts by ID. | Contracts linked |
| 4.3.6 | Milestones tab | ✅ Done | `frontend/src/views/ProjectDetail.vue` | View milestones from linked contracts. | Milestones visible |
| 4.3.7 | Funding tab | ✅ Done | `frontend/src/views/ProjectDetail.vue` | Committed vs target bar, pledge form, commitments list. | Funding trackable |
| 4.3.8 | Updates tab | ✅ Done | `frontend/src/views/ProjectDetail.vue` | Post project updates (owner only). Timeline of updates. | Updates publishable |
| 4.3.9 | Risks tab | ✅ Done | `frontend/src/views/ProjectDetail.vue` | Computed risk assessment: requirements missing, no contracts, funding thin, no updates. | Risks surfaced |
| 4.3.10 | Activity tab | ✅ Done | `frontend/src/views/ProjectDetail.vue` | Combined feed: creation, contracts, commitments, updates. | Activity visible |
| 4.3.11 | Sidebar summary | ✅ Done | `frontend/src/views/ProjectDetail.vue` | Project Summary card, Quick Actions, Invest card (if funding open). | Sidebar informative |
| 4.3.12 | Material suggestions | ✅ Done | `frontend/src/components/projects/ProjectMaterialSuggestions.vue` | Suggests catalog products matching MATERIAL requirements. | Suggestions functional |
| 4.3.13 | **Milestone approval UI** | ❌ Missing | `frontend/src/views/ProjectDetail.vue` + `ContractDetail.vue` | Owner sees "Approve Milestone" button when contractor marks complete. Calls `POST /milestones/{id}/approve/`. Triggers escrow release. | Approval workflow complete |
| 4.3.14 | **Escrow status panel** | ❌ Missing | `frontend/src/views/ProjectDetail.vue` | Show: Total escrowed, Released to date, Pending release, Next release amount + milestone. | Financial status visible |
| 4.3.15 | **Payment release action** | ❌ Missing | `frontend/src/views/ProjectDetail.vue` + backend | "Release Payment" button next to approved milestone. Calls `POST /escrow-release/trigger/`. Confirmation modal shows amount + recipient. | Payment release actionable |
| 4.3.16 | **Gantt / timeline visualization** | ❌ Missing | `frontend/src/views/ProjectDetail.vue` | Visual timeline showing milestones, dependencies, current date, completion %. | Project schedule visualized |
| 4.3.17 | **Budget vs. actual tracking** | ❌ Missing | `frontend/src/views/ProjectDetail.vue` + backend | Track: Estimated budget, Committed spend (awarded contracts + orders), Released payments, Remaining budget. Warn if over budget. | Budget health visible |
| 4.3.18 | **Document upload directly to project** | ❌ Missing | `frontend/src/views/ProjectDetail.vue` + backend | Documents tab allows upload (not just viewing contract attachments). Categorized: Plans, Permits, Reports, Photos. | Project document library |
| 4.3.19 | **Change order management** | ❌ Missing | `frontend/src/views/ProjectDetail.vue` + backend | Track contract amendments: scope changes, budget changes, timeline changes. Approval workflow for changes. | Changes managed formally |
| 4.3.20 | **Procurement from requirements** | ❌ Missing | `frontend/src/views/ProjectDetail.vue` | "Request Quotes for All Materials" button. Converts MATERIAL requirements to multi-item quote request. | One-click procurement |

---

## 4.4 Tender Posting & Contract Management

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 4.4.1 | Tender posting form | ✅ Done | `frontend/src/views/PostContract.vue` | Fields: title, scope, location, category, budget min/max, bid deadline, start/end dates, image, payment terms, eligibility. | Tender posted successfully |
| 4.4.2 | Workflow banner | ✅ Done | `frontend/src/views/PostContract.vue` | 4-step banner: Write brief → Classify → Confirm commercials → Broadcast. | Banner guides posting |
| 4.4.3 | Live preview sidebar | ✅ Done | `frontend/src/views/PostContract.vue` | Shows tender summary and "What happens next". | Preview updates live |
| 4.4.4 | Contract detail workspace | ✅ Done | `frontend/src/views/ContractDetail.vue` | Hero, workflow banner, tabs: Overview, Bids, Milestones, Files, Reviews. | Workspace functional |
| 4.4.5 | Bid list (owner view) | ✅ Done | `frontend/src/views/ContractDetail.vue` | Lists received bids with contractor, timeline, cost, message. Shortlist and Award buttons. | Bids visible |
| 4.4.6 | Bid submission (contractor view) | ✅ Done | `frontend/src/views/ContractDetail.vue` | Submit bid form with cost, timeline, message. | Bids submittable |
| 4.4.7 | Shortlist & Award | ✅ Done | `frontend/src/views/ContractDetail.vue` | Shortlist button, Award button (rejects others, updates contract). | Award workflow functional |
| 4.4.8 | Milestone creation | ✅ Done | `frontend/src/views/ContractDetail.vue` | Owner can add milestones to contract. | Milestones creatable |
| 4.4.9 | **Tender templates** | ❌ Missing | `frontend/src/views/PostContract.vue` | Offer templates: Construction, Supply, Design-Build, Consultancy. Pre-fills scope structure, typical milestones, standard payment terms. | Templates accelerate posting |
| 4.4.10 | **Bid comparison matrix** | ❌ Missing | `frontend/src/views/ContractDetail.vue` | Side-by-side table: Contractor | Price | Timeline | Experience | Certifications | Rating | Notes. Highlight best value. | Comparison aids decision |
| 4.4.11 | **Bid scoring rubric** | ❌ Missing | `frontend/src/views/ContractDetail.vue` | Owner scores bids 1–5 on: Price, Timeline, Quality, Experience. Weighted total auto-calculated. | Objective bid evaluation |
| 4.4.12 | **Invite-only tender** | ❌ Missing | `frontend/src/views/PostContract.vue` + backend | "Invite Specific Contractors" option. Select from vendor directory. Only invited contractors see tender. | Private tenders supported |
| 4.4.13 | **Tender cloning** | ❌ Missing | `frontend/src/views/ContractDetail.vue` | "Duplicate Tender" button. Copies all fields, resets status to DRAFT, clears bids. | Repeat tenders fast |
| 4.4.14 | **Bid deadline reminders** | ❌ Missing | `frontend/src/views/ContractDetail.vue` + backend | Show countdown: "Bid deadline in 3 days." Auto-notify invited contractors 24h before deadline. | Urgency communicated |

---

## 4.5 Milestone & Escrow Management

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 4.5.1 | Milestone backend model | ✅ Done | `backend/milestones/models.py` | `Milestone`: title, description, amount, due_date, status (PENDING, COMPLETED, APPROVED, PAID). | Model exists |
| 4.5.2 | Milestone completion API | ✅ Done | `backend/milestones/views.py` | `POST /milestones/{id}/complete/` (contractor marks complete). | Completion functional |
| 4.5.3 | Milestone approval API | ✅ Done | `backend/milestones/views.py` | `POST /milestones/{id}/approve/` (owner approves, auto-completes contract, returns PENDING_RELEASE). | Approval functional |
| 4.5.4 | Escrow backend model | ✅ Done | `backend/escrow/models.py` | `EscrowAccount`, `EscrowTransaction`, `EscrowRelease`, `EscrowHold`. Fully modeled. | Model exists |
| 4.5.5 | Escrow deposit API | ✅ Done | `backend/escrow/views.py` | `POST /escrow/deposit/` funds escrow for contract. | Deposit functional |
| 4.5.6 | Escrow release trigger API | ✅ Done | `backend/escrow/views.py` | `POST /escrow-release/trigger/` releases funds for milestone. | Release functional |
| 4.5.7 | **Milestone approval UI** | ❌ Missing | `frontend/src/views/ContractDetail.vue` + `ProjectDetail.vue` | Owner sees "Approve" button when milestone status is COMPLETED. Confirmation modal with amount. On approval, show "Payment release initiated". | Frontend uses backend API |
| 4.5.8 | **Escrow deposit UI** | ❌ Missing | `frontend/src/views/ContractDetail.vue` | "Fund Escrow" button. Modal: amount, payment method, confirmation. Calls `/escrow/deposit/`. | Deposit actionable |
| 4.5.9 | **Escrow balance display** | ❌ Missing | `frontend/src/views/ContractDetail.vue` + `ProjectDetail.vue` | Show: Total in escrow, Available, Held (disputes), Released to date. | Balance visible |
| 4.5.10 | **Transaction history** | ❌ Missing | `frontend/src/views/OwnerDashboard.vue` | Real transaction table: Date, Type (Deposit/Release/Refund), Amount, Milestone, Status. | History accurate |
| 4.5.11 | **Dispute hold notifications** | ❌ Missing | `frontend/src/views/OwnerDashboard.vue` + backend | If `EscrowHold` exists, show banner: "Payment release blocked pending dispute resolution." | Holds surfaced |
| 4.5.12 | **Milestone progress photos** | ❌ Missing | `frontend/src/views/ContractDetail.vue` + backend | Contractor uploads progress photos when marking milestone complete. Owner reviews photos before approval. | Evidence-based approval |

---

## 4.6 Backend API Gaps

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 4.6.1 | Project analytics endpoint | ❌ Missing | `backend/projects/views.py` | `GET /v4/projects/{id}/analytics/` returns budget vs actual, milestone progress %, risk score. | Dashboard renders charts |
| 4.6.2 | Owner activity log endpoint | ❌ Missing | `backend/projects/views.py` or new app | `GET /owner/activity/` returns event-sourced activity across projects, contracts, quotes, escrow. | Activity feed real |
| 4.6.3 | Escrow overview endpoint | ❌ Missing | `backend/escrow/views.py` | `GET /escrow/overview/` returns totals: held, released, pending, disputed. | Dashboard shows real escrow |
| 4.6.4 | Bid comparison endpoint | ❌ Missing | `backend/bids/views.py` | `GET /contracts/{id}/bid-comparison/` returns structured bid data for matrix rendering. | Frontend comparison easy |
| 4.6.5 | Project document endpoints | ❌ Missing | `backend/projects/views.py` | `POST/GET/DELETE /v4/projects/{id}/documents/` CRUD for project document library. | Document library functional |
| 4.6.6 | Change order endpoints | ❌ Missing | `backend/contracts/views.py` | `POST /contracts/{id}/change-orders/` with scope/budget/timeline changes. Approval workflow. | Changes managed |

---

## 4.7 Mobile & Accessibility

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 4.7.1 | Responsive layout | ✅ Done | `frontend/src/views/OwnerDashboard.vue` | Grid adjusts for mobile. | Mobile layout works |
| 4.7.2 | Workflow banners responsive | ✅ Done | Various views | Banners stack on mobile. | Mobile banners readable |
| 4.7.3 | **Mobile bottom nav** | ❌ Missing | `frontend/src/views/OwnerDashboard.vue` | Bottom tabs: [📂 Projects] [📋 Tenders] [💰 Escrow] [🔔 Alerts] [👤 Account]. | Thumb-reachable nav |
| 4.7.4 | **Milestone approval one-tap** | ❌ Missing | `frontend/src/views/ContractDetail.vue` | Mobile-optimized card: milestone name, amount, photo thumbnail, [Approve] [Request Changes]. | Quick mobile approval |
| 4.7.5 | **Offline draft for project creation** | ❌ Missing | `frontend/src/views/CreateProject.vue` | Auto-save form to `localStorage`. Sync when online. | No data loss |

---

# 5. INVESTOR MODULE

**Blueprint:** `INVESTOR_MODULE_WORKFLOW_UX_TRANSFORM.md`  
**Frontend Root:** `frontend/src/views/InvestorDashboard.vue`, `frontend/src/views/ProjectList.vue`, `frontend/src/views/ProjectDetail.vue`, `frontend/src/views/FinanceApplication.vue`, `frontend/src/views/SecondaryMarket.vue`  
**Backend Root:** `backend/regulation/`, `backend/projects/`, `backend/compliance/`, `backend/finance/`, `backend/banking/`

---

## 5.1 Investor Dashboard & Workspace

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 5.1.1 | Dashboard shell | ✅ Done | `frontend/src/views/InvestorDashboard.vue` | Hero stats: Total Committed, Active Projects, Pending Pledges, Open Applications. Workflow path card. Four tabs: Portfolio, Agreements, Applications, Accounts. | Dashboard renders |
| 5.1.2 | Workflow path | ✅ Done | `frontend/src/views/InvestorDashboard.vue` | 4 stages: SETUP → DISCOVER → ACTION → ACTIVE. Adapts to investor state. | Banner guides investor |
| 5.1.3 | Compliance sidebar | ✅ Done | `frontend/src/views/InvestorDashboard.vue` | Shows KYC status, Accreditation status, Jurisdiction. | Compliance visible |
| 5.1.4 | Quick actions | ✅ Done | `frontend/src/views/InvestorDashboard.vue` | Initialize investor profile, Start application, Link bank account. | Actions accessible |
| 5.1.5 | Portfolio tab | ✅ Done | `frontend/src/views/InvestorDashboard.vue` | Lists agreements with amount, status, signed date. | Portfolio visible |
| 5.1.6 | Applications tab | ✅ Done | `frontend/src/views/InvestorDashboard.vue` | Lists finance applications with status. | Applications trackable |
| 5.1.7 | Accounts tab | ✅ Done | `frontend/src/views/InvestorDashboard.vue` | Embeds `BankAccountManager`. Bank accounts + settlement history. | Banking functional |
| 5.1.8 | **Portfolio analytics charts** | ❌ Missing | `frontend/src/views/InvestorDashboard.vue` + backend | Add charts: committed over time, returns by project, cash flow timeline, allocation by asset type. | Analytics visualized |
| 5.1.9 | **IRR / return metrics** | ❌ Missing | `frontend/src/views/InvestorDashboard.vue` + backend | Calculate and display estimated IRR, total returns, unrealized gains. | Returns visible |
| 5.1.10 | **Investor notification center** | ❌ Missing | `frontend/src/views/InvestorDashboard.vue` + backend | Alerts: new opportunity match, pledge accepted, milestone paid, KYC reminder, report available. | Investor stays informed |
| 5.1.11 | **Goal-based navigation** | ❌ Missing | `frontend/src/views/InvestorDashboard.vue` | Rename tabs: Portfolio → My Investments, Agreements → Legal & Contracts, Applications → Financing, Accounts → Banking & Settlement. | Navigation reflects intent |
| 5.1.12 | **Investor opportunity shortlist** | ❌ Missing | `frontend/src/views/InvestorDashboard.vue` + backend | "Watchlist" tab. Saved projects with funding status updates. | Investor tracks opportunities |

---

## 5.2 Investor Onboarding & KYC

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 5.2.1 | Investor profile model | ✅ Done | `backend/regulation/models.py` | `InvestorProfile`: kyc_status, accreditation_status, jurisdiction. | Model exists |
| 5.2.2 | Onboard API | ✅ Done | `backend/regulation/views.py` | `POST /v5/investors/onboard/` creates profile. | Onboarding functional |
| 5.2.3 | KYC model & admin approval | ✅ Done | `backend/compliance/models.py` | `KYCVerification`: document_type, document_number, document_url, status. Admin approve/reject actions. | KYC workflow backend exists |
| 5.2.4 | **Investor onboarding wizard** | ❌ Missing | `frontend/src/views/InvestorOnboarding.vue` (new) + router | Multi-step wizard: 1) Intent & Jurisdiction, 2) Identity Upload (ID, passport, selfie), 3) Accreditation Questionnaire (income, net worth, experience), 4) Bank Account Linking, 5) Risk Acknowledgement & Terms. Route: `/investor/onboard`. | Investor can complete KYC self-service |
| 5.2.5 | **Investor KYC submission UI** | ❌ Missing | `frontend/src/views/InvestorDashboard.vue` or wizard | Document upload form: select document type, upload file, enter document number. Posts to `/compliance/kyc-verifications/`. | Investor uploads docs without admin intervention |
| 5.2.6 | **KYC status tracker** | ❌ Missing | `frontend/src/views/InvestorDashboard.vue` | Visual tracker: Submitted → Under Review → Verified / Rejected. If rejected, show reason + re-upload CTA. | Status transparent |
| 5.2.7 | **Accreditation workflow UI** | ❌ Missing | `frontend/src/views/InvestorDashboard.vue` | Questionnaire: annual income, net worth, investment experience, risk tolerance. Auto-determines accreditation level. | Accreditation self-assessed |

---

## 5.3 Opportunity Discovery

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 5.3.1 | Project discovery with funding filter | ✅ Done | `frontend/src/views/ProjectList.vue` | Filter by `status=FUNDING_OPEN`, budget range, location. Cards show budget, requirements, progress. | Opportunities discoverable |
| 5.3.2 | "Funding Open" badge | ✅ Done | `frontend/src/views/ProjectList.vue` | Badge shown when `project.funding_required`. | Funding status visible |
| 5.3.3 | Project detail funding tab | ✅ Done | `frontend/src/views/ProjectDetail.vue` | Committed vs target bar, progress %, pledge input, "Commit capital" button. | Pledge functional |
| 5.3.4 | **Investor-centric filters** | ❌ Missing | `frontend/src/views/ProjectList.vue` + backend | Add filters: Minimum Commitment, Expected Yield, Risk Rating, Asset Type, Funding Stage, Days Remaining. | Investor can filter by return profile |
| 5.3.5 | **Risk scoring display** | ❌ Missing | `frontend/src/views/ProjectList.vue` + `ProjectDetail.vue` + backend | Backend `risk` app computes score. Show: Risk Rating (Low/Medium/High), Risk Factors (requirements missing, no contracts, thin funding). | Risk transparent |
| 5.3.6 | **Opportunity shortlist / watchlist** | ❌ Missing | `frontend/src/views/ProjectList.vue` + backend | Star icon on project cards. Backend `InvestorWatchlist` model. Dashboard "Watchlist" tab shows saved projects with status updates. | Investor tracks opportunities |
| 5.3.7 | **Comparable opportunity view** | ❌ Missing | `frontend/src/views/ProjectList.vue` | Compare up to 3 funding opportunities side-by-side: Budget, Committed %, Risk, Expected Timeline, Owner Track Record. | Comparison aids selection |
| 5.3.8 | **Deal room / data room** | ❌ Missing | `frontend/src/views/ProjectDetail.vue` | Dedicated "Investor Data Room" tab: financial projections, site plans, permits, feasibility studies, team bios. Access gated by KYC status. | Due diligence materials organized |

---

## 5.4 Pledge, Commitment & Agreement Flow

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 5.4.1 | Pledge API | ✅ Done | `backend/projects/views.py` | `POST /v4/projects/{id}/commit/` creates `InvestmentCommitment` with `PLEDGED` status. Validates amount and budget cap. | Pledge backend functional |
| 5.4.2 | Commitments list API | ✅ Done | `backend/projects/views.py` | `GET /v4/projects/{id}/commitments/` lists pledges. | Commitments retrievable |
| 5.4.3 | Agreement model | ✅ Done | `backend/regulation/models.py` | `InvestmentAgreement`: project, investor, amount, status (DRAFT/SIGNED/FUNDED/CANCELLED), signed_at. | Model exists |
| 5.4.4 | Agreement signing API | ✅ Done | `backend/regulation/views.py` | `POST /v5/agreements/{id}/sign/` sets status SIGNED. | Signing functional |
| 5.4.5 | Agreement list in dashboard | ✅ Done | `frontend/src/views/InvestorDashboard.vue` | Portfolio tab shows agreements with status. | Agreements visible |
| 5.4.6 | **Pledge → Agreement conversion workflow** | ❌ Missing | `frontend/src/views/InvestorDashboard.vue` + backend | When investor pledges, auto-create draft agreement. Investor reviews terms, signs digitally. Status flow: PLEDGED → DRAFT → SIGNED → FUNDED. | End-to-end pledge workflow |
| 5.4.7 | **Investor pledge management** | ❌ Missing | `frontend/src/views/InvestorDashboard.vue` + backend | List all pledges. Allow cancel (before SIGNED), modify amount (before FUNDED). | Investor controls commitments |
| 5.4.8 | **Agreement terms preview** | ❌ Missing | `frontend/src/views/InvestorDashboard.vue` | Before signing, show agreement terms: investment amount, expected return, exit terms, risk disclosures. | Terms transparent |
| 5.4.9 | **Digital signature capture** | ❌ Missing | `frontend/src/views/InvestorDashboard.vue` | Signature pad or checkbox with OTP confirmation for agreement execution. | Signature legally meaningful |
| 5.4.10 | **Funding call / capital call** | ❌ Missing | `frontend/src/views/InvestorDashboard.vue` + backend | When project reaches funding threshold, notify investor: "Your commitment of KES X is now due." Payment link to escrow. | Capital calls automated |

---

## 5.5 Portfolio Tracking & Returns

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 5.5.1 | Agreement status tracking | ✅ Done | `frontend/src/views/InvestorDashboard.vue` | Shows DRAFT, SIGNED, FUNDED, CANCELLED statuses. | Status visible |
| 5.5.2 | **Investment transaction API** | ❌ Missing | `backend/regulation/views.py` | `InvestmentTransaction` model exists but no viewset. Expose: `GET /v5/transactions/` with filtering by agreement. | Transactions retrievable |
| 5.5.3 | **Investor report API** | ❌ Missing | `backend/regulation/views.py` | `InvestorReport` model exists but no viewset. Expose: `GET /v5/reports/` with period filtering. | Reports retrievable |
| 5.5.4 | **Cash flow timeline** | ❌ Missing | `frontend/src/views/InvestorDashboard.vue` | Visual timeline: Commitment → Funding → Milestone Payments → Returns → Exit. Show dates and amounts. | Cash flow clear |
| 5.5.5 | **Portfolio performance charts** | ❌ Missing | `frontend/src/views/InvestorDashboard.vue` | Line chart: committed capital over time. Bar chart: returns by project. Pie chart: allocation by asset type/location. | Performance visualized |
| 5.5.6 | **Downloadable statements** | ❌ Missing | `frontend/src/views/InvestorDashboard.vue` + backend | "Download Statement" button. PDF/CSV with all transactions, agreements, returns for selected period. | Statements exportable |
| 5.5.7 | **Milestone-linked returns** | ❌ Missing | `frontend/src/views/InvestorDashboard.vue` + backend | When project milestone is approved and payment released, show investor's share of return in dashboard. | Returns linked to progress |

---

## 5.6 Secondary Market

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 5.6.1 | Secondary market UI stub | ⚠️ Partial | `frontend/src/views/SecondaryMarket.vue` | Filter bar, grid of trades fetched from `/v6/secondary-trades/`. Buy/Sell modals present. | UI renders |
| 5.6.2 | **Trade execution backend** | ❌ Missing | `backend/investments/` (empty app) or new app | `SecondaryTrade` model: seller, buyer, agreement, price, status. APIs: list, create, accept, settle. | Trades executable |
| 5.6.3 | **Trade execution frontend** | ❌ Missing | `frontend/src/views/SecondaryMarket.vue` | Wire up `confirmBuy` / `confirmSell` to real API. Show trade status: Open → Matched → Settled. | Buy/sell functional |
| 5.6.4 | **Seller listing flow** | ❌ Missing | `frontend/src/views/InvestorDashboard.vue` | "Sell Stake" button on agreement. Set asking price (discount/premium to original). List on secondary market. | Stakes sellable |

---

## 5.7 Finance Applications

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 5.7.1 | Finance application form | ✅ Done | `frontend/src/views/FinanceApplication.vue` | Select product, target type, amount, purpose, description. Product summary sidebar. Eligibility checklist. | Application submittable |
| 5.7.2 | Finance product API | ✅ Done | `backend/finance/views.py` | `FinanceProduct` model + viewset. Products listable. | Products retrievable |
| 5.7.3 | Application status tracking | ✅ Done | `frontend/src/views/InvestorDashboard.vue` | Applications tab shows status. | Status trackable |
| 5.7.4 | **Application decision workflow** | ❌ Missing | `frontend/src/views/InvestorDashboard.vue` + backend | Show decision: Approved / Rejected / Needs More Info. If approved, show terms and acceptance CTA. If rejected, show reason. | Decision transparent |
| 5.7.5 | **Application document upload** | ❌ Missing | `frontend/src/views/FinanceApplication.vue` | Upload supporting docs: bank statements, business registration, tax returns. Categorized per product requirements. | Documents attached |

---

## 5.8 Backend API Gaps

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 5.8.1 | Investment transaction viewset | ❌ Missing | `backend/regulation/views.py` | `InvestmentTransactionViewSet` for `GET /v5/transactions/`. | Transactions exposed |
| 5.8.2 | Investor report viewset | ❌ Missing | `backend/regulation/views.py` | `InvestorReportViewSet` for `GET /v5/reports/`. | Reports exposed |
| 5.8.3 | Investor analytics endpoint | ❌ Missing | `backend/regulation/views.py` | `GET /v5/investors/analytics/` returns portfolio summary, committed, returned, active agreements count. | Dashboard renders analytics |
| 5.8.4 | Investor watchlist endpoints | ❌ Missing | `backend/regulation/views.py` or `backend/projects/views.py` | `GET/POST/DELETE /v5/watchlist/` CRUD for `InvestorWatchlist`. | Watchlist functional |
| 5.8.5 | Secondary trade backend | ❌ Missing | `backend/investments/models.py` + `views.py` | Build out empty `investments` app. `SecondaryTrade` model + viewset. | Secondary market executable |
| 5.8.6 | Risk scoring endpoint | ❌ Missing | `backend/risk/views.py` | `GET /risk/projects/{id}/score/` returns risk rating + factors. | Frontend displays risk |
| 5.8.7 | Capital call endpoints | ❌ Missing | `backend/regulation/views.py` | `POST /v5/agreements/{id}/call-capital/` triggers funding due notification + payment link. | Capital calls automated |

---

## 5.9 Mobile & Accessibility

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 5.9.1 | Responsive dashboard | ✅ Done | `frontend/src/views/InvestorDashboard.vue` | Grid adjusts for mobile. | Mobile layout works |
| 5.9.2 | **Mobile bottom nav** | ❌ Missing | `frontend/src/views/InvestorDashboard.vue` | Bottom tabs: [🔍 Deals] [📊 Portfolio] [📋 Applications] [🔔 Alerts] [👤 Profile]. | Thumb-reachable nav |
| 5.9.3 | **Mobile document upload** | ❌ Missing | `frontend/src/views/InvestorOnboarding.vue` | Camera capture for ID/passport photos. Auto-crop and compress. | KYC upload from mobile |
| 5.9.4 | **Portfolio swipe cards** | ❌ Missing | `frontend/src/views/InvestorDashboard.vue` | Swipeable investment cards showing key metrics. Swipe up for details, down for archive. | Quick mobile review |

---

# 6. CONTRACTOR MODULE

**Blueprint:** `CONTRACTOR_MODULE_WORKFLOW_UX_TRANSFORM.md`  
**Frontend Root:** `frontend/src/views/ContractorDashboard.vue`, `frontend/src/views/ContractorRegistration.vue`, `frontend/src/views/ViewTenders.vue`, `frontend/src/views/ContractDetail.vue`, `frontend/src/views/ContractList.vue`  
**Backend Root:** `backend/contractors/`, `backend/bids/`, `backend/contracts/`, `backend/milestones/`, `backend/escrow/`

---

## 6.1 Contractor Onboarding & Verification

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 6.1.1 | Single-page registration form | ✅ Done | `frontend/src/views/ContractorRegistration.vue` | Fields: company name, location picker, service category multi-select, terms checkbox. Posts to `/contractors/register/`. | Profile created |
| 6.1.2 | Dashboard onboarding state | ✅ Done | `frontend/src/views/ContractorDashboard.vue` | If no profile → "Complete Contractor Onboarding" CTA. If pending → pending state. | States handled |
| 6.1.3 | Admin approval backend | ✅ Done | `backend/contractors/views.py` | `POST /contractors/{id}/approve/` grants CONTRACTOR role. `POST /contractors/{id}/reject/` revokes. | Approval functional |
| 6.1.4 | **Multi-step onboarding wizard** | ❌ Missing | `frontend/src/views/ContractorRegistration.vue` or new `ContractorOnboardingWizard.vue` | Steps: 1) Business Info (name, reg number, tax ID), 2) Services & Coverage (categories, service radius, regions), 3) Certifications & Licenses (upload certs, expiry dates), 4) Portfolio & References (past projects, client refs), 5) Review & Submit. | Wizard with step persistence |
| 6.1.5 | **Certification upload UI** | ❌ Missing | `frontend/src/views/ContractorRegistration.vue` + backend | Document upload: trade license, safety cert, insurance, tax clearance. Backend `ContractorCertification` model exists but unused. | Certs attached to profile |
| 6.1.6 | **Verification progress tracker** | ❌ Missing | `frontend/src/views/ContractorDashboard.vue` | Visual tracker: Profile Submitted → Documents Under Review → Verified / Rejected. Show estimated approval time. | Status transparent |
| 6.1.7 | **Service radius configuration** | ❌ Missing | `frontend/src/views/ContractorRegistration.vue` + backend | Map-based radius selector. Show coverage area. Backend field exists but no UI. | Coverage visible |

---

## 6.2 Contractor Dashboard & Workspace

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 6.2.1 | Dashboard shell | ✅ Done | `frontend/src/views/ContractorDashboard.vue` | `DashboardShell` with sidebar: Active Bids, Active Jobs, Posted Tenders, Business Profile. | Sections switchable |
| 6.2.2 | Workflow card | ✅ Done | `frontend/src/views/ContractorDashboard.vue` | Stage logic: SETUP → PENDING → BIDDING → ACTIVE. | Banner adapts |
| 6.2.3 | Command nodes (stats) | 🔄 Partial | `frontend/src/views/ContractorDashboard.vue` | Stats cards render but values are **hardcoded**: Active Proposals, Awarded Jobs, Bid Success Rate 74%, System Rating 4.9. | Stats show real data |
| 6.2.4 | Active bids table | ✅ Done | `frontend/src/views/ContractorDashboard.vue` | Table: project, date, price, status. | Bids trackable |
| 6.2.5 | Active jobs cards | 🔄 Partial | `frontend/src/views/ContractorDashboard.vue` | Cards show but completion is **hardcoded at 45%**. No real progress calculation. | Progress reflects reality |
| 6.2.6 | Business profile view | ✅ Done | `frontend/src/views/ContractorDashboard.vue` | Read-only profile display. | Profile visible |
| 6.2.7 | **Real analytics backend** | ❌ Missing | `backend/bids/views.py` + frontend | Compute: bid success rate (awarded / total bids), avg bid value, on-time completion rate, client rating. | Dashboard shows real stats |
| 6.2.8 | **Active job execution workspace** | ❌ Missing | `frontend/src/views/ContractorJobWorkspace.vue` (new) | Dedicated page per awarded contract: milestone checklist, progress upload, chat, documents, payment status. Not generic ContractDetail. | Contractor has execution-focused UI |
| 6.2.9 | **Payment drawdown tracking** | ❌ Missing | `frontend/src/views/ContractorDashboard.vue` + backend | Card showing: Total Contract Value, Paid to Date, Pending Approval, Next Milestone Amount, Next Payment Date. | Cash flow visible |
| 6.2.10 | **Urgent actions strip** | ❌ Missing | `frontend/src/views/ContractorDashboard.vue` | Priority alerts: "Milestone due in 2 days", "Bid deadline tomorrow", "Payment pending approval for 5 days". | Urgent items surfaced |
| 6.2.11 | **Goal-based navigation** | ❌ Missing | `frontend/src/views/ContractorDashboard.vue` | Rename: Active Bids → Find & Bid, Active Jobs → My Jobs, Posted Tenders → Tenders I Posted, Business Profile → Company & Certs. | Navigation reflects intent |

---

## 6.3 Tender Discovery & Bid Submission

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 6.3.1 | Tender discovery grid | ✅ Done | `frontend/src/views/ViewTenders.vue` + `ContractList.vue` | Grid/list toggle, filters (status, location, budget), search. | Tenders discoverable |
| 6.3.2 | Bid submission form | ✅ Done | `frontend/src/views/ContractDetail.vue` | Form: proposed_cost, proposed_timeline_days, message. Posts to `/contracts/{id}/bids/`. | Bid submittable |
| 6.3.3 | Bid status tracking | ✅ Done | `frontend/src/views/ContractDetail.vue` | Contractor sees own bid status: SUBMITTED / SHORTLISTED / AWARDED / REJECTED. | Status visible |
| 6.3.4 | Chat integration | ✅ Done | `frontend/src/views/ContractDetail.vue` | Chat modal for contractor-owner communication. | Chat accessible |
| 6.3.5 | **Dedicated bid workspace** | ❌ Missing | `frontend/src/views/ContractorBidWorkspace.vue` (new) | Full-page bid preparation: read scope, download attachments, prepare line-item BOQ, write proposal, review & submit. | Bid preparation immersive |
| 6.3.6 | **Bid templates / BOQ builder** | ❌ Missing | `frontend/src/views/ContractorBidWorkspace.vue` | Line-item breakdown: item, quantity, unit, rate, amount. Auto-total. Save as template for future bids. | Bids structured |
| 6.3.7 | **Bid withdrawal** | ❌ Missing | `frontend/src/views/ContractorDashboard.vue` + backend | "Withdraw Bid" button before deadline. Backend permission `bids:withdraw_bid` exists but unused. | Withdrawal functional |
| 6.3.8 | **Bid edit / resubmit** | ❌ Missing | `frontend/src/views/ContractorDashboard.vue` | If rejected, "Edit & Resubmit" button. Pre-fills previous bid data. | Rejection recovery |
| 6.3.9 | **Bid deadline reminders** | ❌ Missing | `frontend/src/views/ContractorDashboard.vue` + backend | Countdown on bid: "Closes in 2 days." Notification 24h before deadline. | Urgency communicated |
| 6.3.10 | **Tender recommendations** | ❌ Missing | `frontend/src/views/ContractorDashboard.vue` + backend | "Recommended for you" based on service categories, location radius, past bids. | Discovery personalized |

---

## 6.4 Milestone Execution & Progress

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 6.4.1 | Milestone list | ✅ Done | `frontend/src/views/ContractDetail.vue` | Lists milestones: title, due date, amount, status badge. | Milestones visible |
| 6.4.2 | Mark complete | ✅ Done | `frontend/src/views/ContractDetail.vue` | "Mark Complete" button if `status === PENDING`. Calls `POST /milestones/{id}/complete/`. | Completion functional |
| 6.4.3 | Auto-contract status advance | ✅ Done | `backend/milestones/views.py` | Completing first milestone auto-advances contract AWARDED → IN_PROGRESS. | Status syncs |
| 6.4.4 | **Progress evidence upload** | ❌ Missing | `frontend/src/views/ContractDetail.vue` + backend | Upload photos, videos, documents when marking complete. Backend `Milestone` needs attachment FK. | Evidence-based completion |
| 6.4.5 | **Progress percentage slider** | ❌ Missing | `frontend/src/views/ContractDetail.vue` | Slider 0–100% per milestone. Partial completion tracked. | Granular progress |
| 6.4.6 | **Milestone comment thread** | ❌ Missing | `frontend/src/views/ContractDetail.vue` + backend | Comments per milestone: contractor posts update, owner asks question, contractor replies. | Communication threaded |
| 6.4.7 | **Cross-job milestone aggregation** | ❌ Missing | `frontend/src/views/ContractorDashboard.vue` | Dashboard shows: "3 milestones due this week", "2 pending approval", "1 overdue". | Portfolio view of execution |
| 6.4.8 | **Project timeline / Gantt** | ❌ Missing | `frontend/src/views/ContractDetail.vue` | Visual timeline: milestones as bars, current date line, dependencies, completion %. | Schedule visualized |

---

## 6.5 Payment & Escrow (Contractor View)

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 6.5.1 | Escrow backend models | ✅ Done | `backend/escrow/models.py` | `EscrowAccount`, `EscrowTransaction`, `EscrowRelease`, `EscrowHold`. | Models exist |
| 6.5.2 | Milestone approval backend | ✅ Done | `backend/milestones/views.py` | Owner approves → COMPLETED → APPROVED. Returns `PENDING_RELEASE`. | Approval functional |
| 6.5.3 | **Contractor payment status view** | ❌ Missing | `frontend/src/views/ContractorDashboard.vue` + backend | Card per job: Total Value, Paid, Pending, Held in Escrow, Next Payout Amount + Date. | Cash flow visible |
| 6.5.4 | **Milestone approval → escrow release integration** | ❌ Missing | `backend/milestones/views.py` | `MilestoneViewSet.approve()` should auto-call `EscrowReleaseViewSet.trigger()` if escrow balance sufficient. | Payment release automated |
| 6.5.5 | **Payment history** | ❌ Missing | `frontend/src/views/ContractorDashboard.vue` + backend | Table: Date, Milestone, Amount, Status (Pending / Released / Disputed). | History accurate |
| 6.5.6 | **Payment notification** | ❌ Missing | `frontend/src/views/ContractorDashboard.vue` + backend | Notification: "Payment of KES X released for [Milestone] on [Contract]." | Contractor notified of payouts |
| 6.5.7 | **Retention/hold management** | ❌ Missing | `frontend/src/views/ContractorDashboard.vue` + backend | Show retention amount (e.g., 10% held until final completion). Release retention on contract closeout. | Retention transparent |

---

## 6.6 Workforce & Equipment (New Capability)

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 6.6.1 | Workforce tracking | ❌ Missing | `backend/contractors/models.py` + frontend | `Crew` model: name, role, skills, daily_rate, availability. `CrewAssignment` links crew to contract. | Crew manageable |
| 6.6.2 | Equipment tracking | ❌ Missing | `backend/contractors/models.py` + frontend | `Equipment` model: name, type, rental/owned, daily_cost, availability. `EquipmentAssignment` links to contract. | Equipment trackable |
| 6.6.3 | **Crew scheduler** | ❌ Missing | `frontend/src/views/ContractorDashboard.vue` | Calendar view: crew assigned to which job on which days. Conflict detection. | Scheduling visualized |
| 6.6.4 | **Equipment utilization** | ❌ Missing | `frontend/src/views/ContractorDashboard.vue` | Utilization % per asset. Idle equipment highlighted. | Efficiency tracked |

---

## 6.7 Backend API Gaps

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 6.7.1 | Contractor analytics endpoint | ❌ Missing | `backend/bids/views.py` | `GET /contractors/analytics/` returns bid success rate, total awarded value, on-time rate, avg rating. | Dashboard real stats |
| 6.7.2 | Bid withdrawal endpoint | ❌ Missing | `backend/bids/views.py` | `POST /bids/{id}/withdraw/` sets status WITHDRAWN. Permission `bids:withdraw_bid` exists. | Withdrawal functional |
| 6.7.3 | Milestone attachment endpoints | ❌ Missing | `backend/milestones/views.py` | `POST /milestones/{id}/attachments/` upload evidence. `GET /milestones/{id}/attachments/` list. | Evidence attachable |
| 6.7.4 | Contractor certification endpoints | ❌ Missing | `backend/contractors/views.py` | `POST/GET/DELETE /contractors/me/certifications/` CRUD for `ContractorCertification`. | Certs manageable |
| 6.7.5 | Auto-escrow release on approval | ❌ Missing | `backend/milestones/views.py` | On `approve()`, check escrow balance, auto-trigger release if sufficient. | Payment automated |
| 6.7.6 | Contractor payment history endpoint | ❌ Missing | `backend/escrow/views.py` | `GET /escrow/contractor-payments/` filtered by contractor profile. | Payments retrievable |
| 6.7.7 | Workforce/equipment endpoints | ❌ Missing | `backend/contractors/views.py` | CRUD for `Crew` and `Equipment`. | Resources manageable |

---

## 6.8 Mobile & Accessibility

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 6.8.1 | Responsive dashboard | ✅ Done | `frontend/src/views/ContractorDashboard.vue` | Grid adjusts for mobile. | Mobile layout works |
| 6.8.2 | **Mobile bottom nav** | ❌ Missing | `frontend/src/views/ContractorDashboard.vue` | Bottom tabs: [🔍 Tenders] [📋 Bids] [🏗 Jobs] [💰 Payments] [👤 Profile]. | Thumb-reachable nav |
| 6.8.3 | **Milestone photo capture** | ❌ Missing | `frontend/src/views/ContractDetail.vue` | Camera capture for progress photos. Auto-attach to milestone completion. | Field reporting from mobile |
| 6.8.4 | **Offline progress save** | ❌ Missing | `frontend/src/views/ContractDetail.vue` | Save milestone progress locally when offline. Sync when connection returns. | No data loss on site |

---

# 7. COURIER MODULE

**Blueprint:** `COURIER_MODULE_WORKFLOW_UX_TRANSFORM.md`  
**Frontend Root:** `frontend/src/views/CourierDashboard.vue`, `frontend/src/components/courier/CourierProfileSection.vue`, `frontend/src/components/courier/CourierPricingSection.vue`, `frontend/src/components/courier/CourierApiSection.vue`, `frontend/src/components/courier/CourierShipmentsSection.vue`, `frontend/src/components/logistics/LogisticsTracker.vue`  
**Backend Root:** `backend/logistics/`, `backend/orders/`

---

## 7.1 Courier Onboarding & Profile

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 7.1.1 | Courier dashboard shell | ✅ Done | `frontend/src/views/CourierDashboard.vue` | `DashboardShell` with sections: Profile, Pricing Zones, API Config, Active Shipments. | Sections switchable |
| 7.1.2 | Profile section form | ✅ Done | `frontend/src/components/courier/CourierProfileSection.vue` | Fields: company name, reg no, tax PIN, website, email, phone, location via `LocationInterface`. | Profile editable |
| 7.1.3 | Approval gating | ✅ Done | `frontend/src/views/CourierDashboard.vue` | Workflow banner handles DRAFT → PENDING → APPROVED states. | States handled |
| 7.1.4 | Document upload UI (unwired) | 🔄 Partial | `frontend/src/components/courier/CourierProfileSection.vue` | UI for LICENSE, INSURANCE, REGISTRATION upload exists but `uploadDocument()` only updates local state. No backend endpoint called. | Upload UI renders |
| 7.1.5 | **Document upload backend wiring** | ❌ Missing | `frontend/src/components/courier/CourierProfileSection.vue` + backend | Wire `uploadDocument()` to `POST /logistics/couriers/{id}/documents/` or multipart POST. Backend `CourierDocument` model exists but no upload endpoint. | Documents persist |
| 7.1.6 | **Courier registration route** | ❌ Missing | `frontend/src/router/index.js` | Add `/courier/register` route. Currently only `/courier/dashboard` exists. | Registration discoverable |
| 7.1.7 | **Onboarding wizard** | ❌ Missing | `frontend/src/views/CourierOnboarding.vue` (new) | Multi-step: 1) Company Info, 2) Vehicle & Fleet, 3) Coverage Zones, 4) Documents & Certs, 5) Review & Submit. | Guided onboarding |
| 7.1.8 | **Admin courier approval UI** | ❌ Missing | `frontend/src/components/admin/AdminCourierReview.vue` (new) | Admin sees pending courier list. Can review uploaded docs, approve/reject with notes. | Approval workflow complete |

---

## 7.2 Delivery Zones & Pricing

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 7.2.1 | Pricing zone CRUD | ✅ Done | `frontend/src/components/courier/CourierPricingSection.vue` | Full CRUD for `RADIUS` and `POLYGON` zones. Map-based center selection. Base cost + per-kg rate. | Zones manageable |
| 7.2.2 | Pricing rules | ✅ Done | `frontend/src/components/courier/CourierPricingSection.vue` | Rules: base_cost, per_kg_cost, express/same-day multipliers. | Rules configurable |
| 7.2.3 | Cost calculator | ✅ Done | `frontend/src/components/logistics/LogisticsCalculator.vue` | Zone + weight → cost estimate via `/logistics/pricing-zones/calculate/`. | Calculator functional |
| 7.2.4 | **Zone import/export** | ❌ Missing | `frontend/src/components/courier/CourierPricingSection.vue` | Import zones from CSV (name, center_lat, center_lng, radius, base_cost, per_kg_cost). Export current zones. | Bulk zone management |
| 7.2.5 | **Zone overlap detection** | ❌ Missing | `frontend/src/components/courier/CourierPricingSection.vue` + backend | Warn if two zones overlap. Highlight conflict on map. | Overlaps prevented |

---

## 7.3 Shipment Management

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 7.3.1 | Shipment auto-creation | ✅ Done | `backend/orders/views.py` | When vendor marks order `SHIPPED`, auto-creates `Shipment` + tracking number + initial `TrackingEvent`. | Shipment created |
| 7.3.2 | Shipment list | ✅ Done | `frontend/src/components/courier/CourierShipmentsSection.vue` | Table: tracking number, destination, status badge. | Shipments visible |
| 7.3.3 | Tracking API | ✅ Done | `backend/logistics/views.py` | `GET /logistics/shipments/{id}/track/` returns live tracking + history. | Tracking retrievable |
| 7.3.4 | Tracking UI (public) | ✅ Done | `frontend/src/components/logistics/LogisticsTracker.vue` | Leaflet map with 5s polling, event timeline. | Tracking visualized |
| 7.3.5 | Webhook endpoint | ✅ Done | `backend/logistics/views.py` | `POST /logistics/webhooks/update/{carrier_code}/` receives carrier status updates. | Webhooks functional |
| 7.3.6 | **Courier assignment / accept-reject** | ❌ Missing | `frontend/src/components/courier/CourierShipmentsSection.vue` + backend | New shipment appears as "New Assignment". Courier can Accept or Reject with reason. On accept, `Shipment.courier` set. | Assignment explicit |
| 7.3.7 | **Proof of Delivery (POD)** | ❌ Missing | `frontend/src/components/courier/CourierShipmentsSection.vue` + backend | On delivery: signature pad capture, recipient photo, ID verification checkbox, notes. Backend `Shipment` needs `pod_signature`, `pod_photo`, `pod_recipient_name` fields. | Delivery provable |
| 7.3.8 | **Failed delivery recovery** | ❌ Missing | `frontend/src/components/courier/CourierShipmentsSection.vue` + backend | If recipient unavailable: "Failed Delivery" button. Reason: No one home / Wrong address / Refused. Reschedule option. | Recovery path clear |
| 7.3.9 | **Route optimization** | ❌ Missing | `frontend/src/components/courier/CourierShipmentsSection.vue` + backend | Multi-stop route: optimize order of pickups/drop-offs by distance/time. Show estimated route time. | Route efficient |
| 7.3.10 | **Courier mobile / driver view** | ❌ Missing | `frontend/src/views/CourierDriverView.vue` (new) | Mobile-optimized: large buttons, current stop, next stop, swipe to update status, camera for POD. | Driver-friendly UI |
| 7.3.11 | **Real carrier integrations** | ❌ Missing | `backend/logistics/services.py` | Currently returns mock data. Integrate with G4S/DHL/Sendy APIs for real tracking. | Tracking accurate |
| 7.3.12 | **Courier earnings tracking** | ❌ Missing | `frontend/src/views/CourierDashboard.vue` + backend | Card: Earnings This Week, Completed Deliveries, Pending Payment, Average Delivery Time. | Earnings visible |

---

## 7.4 API Configuration

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 7.4.1 | API config UI | ✅ Done | `frontend/src/components/courier/CourierApiSection.vue` | Form: base URL, API key, webhook URL, endpoint mapping. | Form renders |
| 7.4.2 | **API config persistence** | ❌ Missing | `frontend/src/components/courier/CourierApiSection.vue` + backend | Currently saves to `localStorage` only. Wire to `POST /logistics/couriers/{id}/api_config/`. Backend `CourierApiConfig` model exists but no ViewSet exposure. | Config persists |
| 7.4.3 | **API config validation** | ❌ Missing | `frontend/src/components/courier/CourierApiSection.vue` | "Test Connection" button. Validates API key against carrier sandbox. | Connection verified |

---

## 7.5 Backend API Gaps

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 7.5.1 | Courier document upload endpoint | ❌ Missing | `backend/logistics/views.py` | `POST /logistics/couriers/{id}/documents/` handles multipart upload. Creates `CourierDocument` records. | Documents persist |
| 7.5.2 | Courier API config endpoint | ❌ Missing | `backend/logistics/views.py` | `POST/GET /logistics/couriers/{id}/api_config/` CRUD for `CourierApiConfig`. | Config exposed |
| 7.5.3 | Shipment assignment endpoint | ❌ Missing | `backend/logistics/views.py` | `POST /logistics/shipments/{id}/accept/` / `reject/` with reason. | Assignment explicit |
| 7.5.4 | POD upload endpoint | ❌ Missing | `backend/logistics/views.py` | `POST /logistics/shipments/{id}/pod/` accepts signature image, photo, recipient name. Updates `Shipment` POD fields. | POD captured |
| 7.5.5 | Failed delivery endpoint | ❌ Missing | `backend/logistics/views.py` | `POST /logistics/shipments/{id}/fail/` with reason, reschedule date. | Failures tracked |
| 7.5.6 | Courier analytics endpoint | ❌ Missing | `backend/logistics/views.py` | `GET /logistics/couriers/analytics/` returns delivery count, on-time rate, earnings, avg delivery time. | Dashboard real stats |
| 7.5.7 | Route optimization endpoint | ❌ Missing | `backend/logistics/views.py` | `POST /logistics/shipments/optimize-route/` accepts list of shipment IDs, returns optimized order. | Route optimized |

---

## 7.6 Mobile & Accessibility

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 7.6.1 | Responsive dashboard | ✅ Done | `frontend/src/views/CourierDashboard.vue` | Grid adjusts for mobile. | Mobile layout works |
| 7.6.2 | **Driver mobile view** | ❌ Missing | `frontend/src/views/CourierDriverView.vue` | Large buttons, swipe actions, camera integration, GPS tracking. Offline queue for status updates. | Driver-optimized |
| 7.6.3 | **Barcode/QR scanner** | ❌ Missing | `frontend/src/views/CourierDriverView.vue` | Scan package barcode to confirm pickup/delivery. Match against shipment tracking number. | Scanning functional |
| 7.6.4 | **Voice notes for failures** | ❌ Missing | `frontend/src/views/CourierDriverView.vue` | Record voice note when delivery fails (faster than typing). Attach to failed delivery record. | Field reporting fast |

---

# 8. PROJECT MODULE

**Blueprint:** `PROJECT_MODULE_WORKFLOW_UX_TRANSFORM.md`  
**Frontend Root:** `frontend/src/views/CreateProject.vue`, `frontend/src/views/ProjectList.vue`, `frontend/src/views/ProjectDetail.vue`, `frontend/src/components/projects/ProjectMaterialSuggestions.vue`  
**Backend Root:** `backend/projects/`

---

## 8.1 Project Creation & Onboarding

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 8.1.1 | Project creation form | ✅ Done | `frontend/src/views/CreateProject.vue` | Single form: title, description, location, budget, funding flag. | Project shell creates |
| 8.1.2 | Workflow banner on creation | ✅ Done | `frontend/src/views/CreateProject.vue` | Stage-aware guidance: DRAFT → LOCATION → BUDGET → READY. Scroll-to-field actions. | Banner guides user |
| 8.1.3 | Workflow steps indicator | ✅ Done | `frontend/src/views/CreateProject.vue` | 4 steps: Project basics, Location, Budget and funding, Submit shell. | Steps visible |
| 8.1.4 | Location picker integration | ✅ Done | `frontend/src/views/CreateProject.vue` | Uses `LocationInterface` with map. | Location settable |
| 8.1.5 | **Multi-step creation wizard** | ❌ Missing | `frontend/src/views/ProjectCreateWizard.vue` (new) | Step 1: Project Identity, Step 2: Scope & Requirements, Step 3: Budget & Funding, Step 4: Team & Timeline, Step 5: Review & Publish. | Guided creation |
| 8.1.6 | **Project templates** | ❌ Missing | `frontend/src/views/ProjectCreateWizard.vue` + backend | Templates: Residential Build, Commercial Development, Infrastructure, Renovation. Pre-fill requirements and phases. | Templates accelerate setup |
| 8.1.7 | **Project phase model** | ❌ Missing | `backend/projects/models.py` | `ProjectPhase` model: name, order, start_date, end_date, status. Linked to `Project`. | Phases trackable |
| 8.1.8 | **Draft auto-save** | ❌ Missing | `frontend/src/views/CreateProject.vue` | Auto-save form to localStorage every 30s. Restore on return. | No lost work |

---

## 8.2 Project Discovery & Portfolio

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 8.2.1 | Project list page | ✅ Done | `frontend/src/views/ProjectList.vue` | Grid/list view, search, filters (country, status, budget range). | Projects browsable |
| 8.2.2 | Workflow banner on list | ✅ Done | `frontend/src/views/ProjectList.vue` | EMPTY → DISCOVERY → FUNDING states. | Banner contextual |
| 8.2.3 | Project cards with progress | ✅ Done | `frontend/src/views/ProjectList.vue` | Progress bar derived from status (LISTED:15%, FUNDING_OPEN:35%, EXECUTION_STARTED:70%, COMPLETED:100%). | Progress visible |
| 8.2.4 | Filter sidebar | ✅ Done | `frontend/src/views/ProjectList.vue` | Country, lifecycle stage, budget min/max. | Filters functional |
| 8.2.5 | Empty state | ✅ Done | `frontend/src/views/ProjectList.vue` | `EmptyState` component with CTA. | Empty state helpful |
| 8.2.6 | Proximity search | ✅ Done | `backend/projects/views.py` | `latitude`/`longitude`/`radius_km` params with GIS distance annotation. | Nearby projects findable |
| 8.2.7 | **Project portfolio analytics for owner** | ❌ Missing | `frontend/src/views/OwnerDashboard.vue` + backend | Total projects, active projects, total budget, funding raised, avg completion rate. | Portfolio visible |
| 8.2.8 | **Project compare** | ❌ Missing | `frontend/src/views/ProjectList.vue` | Select 2-3 projects, compare: budget, progress, requirements, funding side-by-side. | Comparison possible |
| 8.2.9 | **Project bookmark/watchlist** | ❌ Missing | `frontend/src/views/ProjectList.vue` + backend | Heart icon to save project. `ProjectBookmark` model. | Projects trackable |

---

## 8.3 Project Workspace (Detail Page)

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 8.3.1 | Project detail shell | ✅ Done | `frontend/src/views/ProjectDetail.vue` | Hero with cover image, breadcrumb, status badge, budget display. | Detail page renders |
| 8.3.2 | Tab navigation | ✅ Done | `frontend/src/views/ProjectDetail.vue` | 9 tabs: Overview, Requirements, Contracts, Milestones, Funding, Documents, Updates, Risks, Activity. | Tabs switchable |
| 8.3.3 | Workflow banner on detail | ✅ Done | `frontend/src/views/ProjectDetail.vue` | SCOPE → PROCUREMENT → FUNDING → UPDATE → EXECUTION stages. Contextual CTAs open relevant tabs. | Next step visible |
| 8.3.4 | Workflow steps | ✅ Done | `frontend/src/views/ProjectDetail.vue` | 4 steps: Define scope, Link procurement, Track funding, Publish progress. | Progress tracked |
| 8.3.5 | Summary stats | ✅ Done | `frontend/src/views/ProjectDetail.vue` | Budget, Requirements, Contracts, Funding, Milestones, Updates. | Stats visible |
| 8.3.6 | Sidebar summary | ✅ Done | `frontend/src/views/ProjectDetail.vue` | Status, budget, funding, linked contracts, active milestones. Quick actions. | Sidebar informative |
| 8.3.7 | Health signals | ✅ Done | `frontend/src/views/ProjectDetail.vue` | Execution state, funding %, contracts count, issues flagged. | Health visible |
| 8.3.8 | Risk assessment (computed) | ✅ Done | `frontend/src/views/ProjectDetail.vue` | Computed risks: no requirements, no contracts, funding thin, no updates. | Risks flagged |
| 8.3.9 | Activity feed (computed) | 🔄 Partial | `frontend/src/views/ProjectDetail.vue` | Client-side computed from project events. Not event-sourced or persistent. | Feed renders |
| 8.3.10 | **Event-sourced activity feed** | ❌ Missing | `backend/projects/models.py` + frontend | `ProjectActivityEvent` model with actor, action, timestamp. Feed loads from DB. | Activity persistent |
| 8.3.11 | **Project document upload** | ❌ Missing | `frontend/src/views/ProjectDetail.vue` + backend | Direct upload to project (drawings, permits, specs). `ProjectDocument` model. | Documents attachable |
| 8.3.12 | **Project team/roles** | ❌ Missing | `frontend/src/views/ProjectDetail.vue` + backend | `ProjectMember` model: user, role (PM, Engineer, Accountant), permissions. | Team manageable |
| 8.3.13 | **Gantt/timeline view** | ❌ Missing | `frontend/src/views/ProjectDetail.vue` | Visual timeline: phases, milestones, dependencies. Drag to reschedule. | Timeline visual |
| 8.3.14 | **Project status transitions** | ❌ Missing | `frontend/src/views/ProjectDetail.vue` + backend | Validated transitions: LISTED → FUNDING_OPEN (requirements check) → EXECUTION_STARTED (contracts linked) → COMPLETED (milestones done). | Transitions gated |

---

## 8.4 Requirements & Procurement

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 8.4.1 | Requirements CRUD | ✅ Done | `frontend/src/views/ProjectDetail.vue` + backend | Add/remove requirements: type (MATERIAL/CONTRACTOR/SERVICE), description, quantity. | Requirements manageable |
| 8.4.2 | Material suggestions | ✅ Done | `frontend/src/components/projects/ProjectMaterialSuggestions.vue` | Matches MATERIAL requirements to catalog products via `/projects/{id}/suggest-products/`. | Suggestions relevant |
| 8.4.3 | Quote from suggestion | ✅ Done | `frontend/src/components/projects/ProjectMaterialSuggestions.vue` | "Request Quote" button creates quote request for matched product. | Quote actionable |
| 8.4.4 | **BOM structure (hierarchical)** | ❌ Missing | `backend/projects/models.py` + frontend | `BillOfMaterials` model: parent requirement, child items, quantities, unit costs. Tree view in UI. | BOM structured |
| 8.4.5 | **Bulk quote request from requirements** | ❌ Missing | `frontend/src/views/ProjectDetail.vue` + backend | "Request quotes for all materials" button. Creates quote requests for all MATERIAL requirements. | Procurement automated |
| 8.4.6 | **Requirement status tracking** | ❌ Missing | `backend/projects/models.py` + frontend | Each requirement: PENDING → QUOTED → ORDERED → DELIVERED. Status visible in list. | Procurement tracked |
| 8.4.7 | **Vendor assignment per requirement** | ❌ Missing | `backend/projects/models.py` + frontend | Link requirement to awarded vendor/contractor. Show vendor name and contact. | Vendors assigned |
| 8.4.8 | **Requirement cost tracking** | ❌ Missing | `frontend/src/views/ProjectDetail.vue` | Estimated vs quoted vs actual cost per requirement. Budget variance calculation. | Costs tracked |

---

## 8.5 Contracts & Milestones

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 8.5.1 | Contract linking | ✅ Done | `frontend/src/views/ProjectDetail.vue` + backend | Link contract by ID. Unlink. View linked contract details. | Contracts linked |
| 8.5.2 | Milestone display (aggregated) | ✅ Done | `frontend/src/views/ProjectDetail.vue` | Milestones from all linked contracts shown in single list. Contract title badge. | Milestones visible |
| 8.5.3 | Milestone creation from project | ✅ Done | `frontend/src/views/ProjectDetail.vue` | Form: select linked contract, title, description, amount, due date. POSTs to `/contracts/{id}/milestones/`. | Milestones creatable |
| 8.5.4 | **Milestone approval within project workspace** | ❌ Missing | `frontend/src/views/ProjectDetail.vue` + backend | "Approve" button on milestone card. Updates milestone status, triggers escrow release. | Approval in-context |
| 8.5.5 | **Milestone progress evidence** | ❌ Missing | `frontend/src/views/ProjectDetail.vue` + backend | Contractor uploads photos/documents to milestone. Owner reviews before approval. | Evidence reviewable |
| 8.5.6 | **Milestone payment status** | ❌ Missing | `frontend/src/views/ProjectDetail.vue` | Show: Pending → Approved → Paid. Link to escrow transaction. | Payment tracked |
| 8.5.7 | **Contract award from project** | ❌ Missing | `frontend/src/views/ProjectDetail.vue` + backend | Create tender/contract directly from project requirements. Auto-link on award. | Award streamlined |
| 8.5.8 | **Bid comparison within project** | ❌ Missing | `frontend/src/views/ProjectDetail.vue` | Compare bids for linked contracts: price, timeline, contractor rating. | Bids comparable |

---

## 8.6 Funding & Investment

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 8.6.1 | Funding progress bar | ✅ Done | `frontend/src/views/ProjectDetail.vue` | Committed vs target with percentage. | Progress visible |
| 8.6.2 | Investment pledge | ✅ Done | `frontend/src/views/ProjectDetail.vue` + backend | Non-owner can pledge amount. Budget validation prevents over-commitment. | Pledge functional |
| 8.6.3 | Commitment list | ✅ Done | `frontend/src/views/ProjectDetail.vue` | Lists pledges with investor name, amount, status, date. | Commitments visible |
| 8.6.4 | **Pledge confirmation workflow** | ❌ Missing | `frontend/src/views/ProjectDetail.vue` + backend | Pledge → Agreement → Payment. Status transitions with notifications. | Funding formalized |
| 8.6.5 | **Funding deadline / target date** | ❌ Missing | `backend/projects/models.py` + frontend | `funding_deadline` field. Countdown display. Auto-close funding on date. | Deadline enforced |
| 8.6.6 | **Investor data room** | ❌ Missing | `frontend/src/views/ProjectDetail.vue` | Restricted documents for investors: financials, permits, contracts. Access control. | Data room secure |
| 8.6.7 | **Project financing application** | 🔄 Partial | `frontend/src/views/ProjectDetail.vue` | `applyForFinance()` posts to `/v3/finance/applications/`. No UI visible in current tabs for this. | Finance accessible |

---

## 8.7 Budget & Analytics

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 8.7.1 | Estimated budget display | ✅ Done | `frontend/src/views/ProjectDetail.vue` | Budget shown in hero, sidebar, summary stats. | Budget visible |
| 8.7.2 | **Budget vs actual tracking** | ❌ Missing | `backend/projects/models.py` + frontend | Track committed costs from contracts, actual spend from orders/milestones. Variance display. | Variance visible |
| 8.7.3 | **Burn rate chart** | ❌ Missing | `frontend/src/views/ProjectDetail.vue` | Line chart: budget consumed over time. Projected completion cost. | Burn rate visible |
| 8.7.4 | **Earned value metrics** | ❌ Missing | `backend/projects/models.py` + frontend | SPI (Schedule Performance Index), CPI (Cost Performance Index). | Performance measured |
| 8.7.5 | **Slippage detection** | ❌ Missing | `frontend/src/views/ProjectDetail.vue` + backend | Alert when milestone due dates pass without completion. Early warning banner. | Slippage detected |
| 8.7.6 | **Project health score** | ❌ Missing | `frontend/src/views/ProjectDetail.vue` + backend | Composite score: budget variance, schedule variance, requirement coverage, update recency. | Health quantified |

---

## 8.8 Backend API Gaps

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 8.8.1 | Project phase endpoints | ❌ Missing | `backend/projects/views.py` | CRUD for `ProjectPhase`. `GET /projects/{id}/phases/`. | Phases manageable |
| 8.8.2 | Project document endpoints | ❌ Missing | `backend/projects/views.py` | `POST/GET /projects/{id}/documents/` multipart upload. | Documents manageable |
| 8.8.3 | Project team endpoints | ❌ Missing | `backend/projects/views.py` | `POST/GET/DELETE /projects/{id}/members/`. Role-based access. | Team manageable |
| 8.8.4 | Activity event endpoints | ❌ Missing | `backend/projects/views.py` | `GET /projects/{id}/activity/`. Event-sourced with pagination. | Activity persistent |
| 8.8.5 | Budget tracking endpoints | ❌ Missing | `backend/projects/views.py` | `GET /projects/{id}/budget/` returns estimated, committed, actual, variance. | Budget trackable |
| 8.8.6 | Project analytics endpoint | ❌ Missing | `backend/projects/views.py` | `GET /projects/{id}/analytics/` returns health score, burn rate, SPI, CPI. | Analytics available |
| 8.8.7 | Status transition endpoint | ❌ Missing | `backend/projects/views.py` | `POST /projects/{id}/transition/` with target status, validates prerequisites. | Transitions controlled |

---

## 8.9 Mobile & Accessibility

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 8.9.1 | Responsive project list | ✅ Done | `frontend/src/views/ProjectList.vue` | Grid collapses to single column on mobile. Filters accessible. | Mobile layout works |
| 8.9.2 | Responsive project detail | ✅ Done | `frontend/src/views/ProjectDetail.vue` | Tabs become scrollable or dropdown on mobile. Sidebar stacks below. | Mobile layout works |
| 8.9.3 | **Field operations mode** | ❌ Missing | `frontend/src/views/ProjectDetail.vue` | Large buttons for site use. Offline queue for updates. GPS tagging. | Field-friendly |
| 8.9.4 | **Voice notes for updates** | ❌ Missing | `frontend/src/views/ProjectDetail.vue` | Record audio update instead of typing. Attach to project updates. | Fast field reporting |

---

# 9. CONTRACT MODULE

**Blueprint:** `CONTRACT_MODULE_WORKFLOW_UX_TRANSFORM.md`  
**Frontend Root:** `frontend/src/views/ContractList.vue`, `frontend/src/views/ContractDetail.vue`, `frontend/src/views/PostContract.vue`, `frontend/src/views/ViewTenders.vue`  
**Backend Root:** `backend/contracts/`, `backend/bids/`, `backend/milestones/`

---

## 9.1 Contract Creation & Posting

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 9.1.1 | Contract posting form | ✅ Done | `frontend/src/views/PostContract.vue` | Form: title, location, category, currency, budget min/max, scope, payment terms, eligibility, bid deadline, start/end dates, featured image. | Contract posts |
| 9.1.2 | Workflow banner on posting | ✅ Done | `frontend/src/views/PostContract.vue` | Stage-aware guidance with scroll-to-field actions. | Banner guides user |
| 9.1.3 | Workflow steps indicator | ✅ Done | `frontend/src/views/PostContract.vue` | 4 steps: Core Brief, Commercial Terms, Timing & Attachments, Review & Post. | Steps visible |
| 9.1.4 | Completeness tracker | ✅ Done | `frontend/src/views/PostContract.vue` | `briefCompletion` computed from filled fields. | Progress visible |
| 9.1.5 | **Contract templates** | ❌ Missing | `frontend/src/views/PostContract.vue` + backend | Templates: Construction, Renovation, Supply, Professional Services. Pre-fill scope, payment terms, eligibility. | Templates accelerate posting |
| 9.1.6 | **Clause library / customizable terms** | ❌ Missing | `frontend/src/views/PostContract.vue` + backend | Standard clauses: force majeure, dispute resolution, termination, IP. Checkbox to include. | Terms customizable |
| 9.1.7 | **Draft auto-save** | ❌ Missing | `frontend/src/views/PostContract.vue` | Auto-save to localStorage. Restore on return. | No lost work |
| 9.1.8 | **Bulk tender posting** | ❌ Missing | `frontend/src/views/PostContract.vue` + backend | CSV import: multiple tenders with shared terms. Batch validate and create. | Bulk posting possible |

---

## 9.2 Contract Discovery & List

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 9.2.1 | Contract list page | ✅ Done | `frontend/src/views/ContractList.vue` | Grid/list view, search, filters (status, country, budget range, sort). | Contracts browsable |
| 9.2.2 | Workflow banner on list | ✅ Done | `frontend/src/views/ContractList.vue` | Contextual guidance for owner/contractor. | Banner relevant |
| 9.2.3 | Filter sidebar | ✅ Done | `frontend/src/views/ContractList.vue` | Status, country, CapEx range, sort by. | Filters functional |
| 9.2.4 | Filter chips | ✅ Done | `frontend/src/views/ContractList.vue` | Active filters shown as removable chips. | Filters manageable |
| 9.2.5 | Results metrics strip | ✅ Done | `frontend/src/views/ContractList.vue` | Visible tenders count. | Count visible |
| 9.2.6 | **Bid deadline urgency** | ❌ Missing | `frontend/src/views/ContractList.vue` | "Closes in X days" / "Closes today" / "Closed" badge with color coding. | Urgency visible |
| 9.2.7 | **Contract compare** | ❌ Missing | `frontend/src/views/ContractList.vue` | Select 2-3 contracts, compare: budget, timeline, location, bids received. | Comparison possible |
| 9.2.8 | **Saved tender alerts** | ❌ Missing | `frontend/src/views/ContractList.vue` + backend | "Notify me of similar tenders" — email alert on matching new tenders. | Alerts functional |

---

## 9.3 Contract Detail & Workspace

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 9.3.1 | Contract detail shell | ✅ Done | `frontend/src/views/ContractDetail.vue` | Hero with image, breadcrumb, status badge, budget range, location. | Detail page renders |
| 9.3.2 | Tab navigation | ✅ Done | `frontend/src/views/ContractDetail.vue` | 4 tabs: Overview, Bids, Milestones, Attachments. | Tabs switchable |
| 9.3.3 | Workflow banner on detail | ✅ Done | `frontend/src/views/ContractDetail.vue` | DRAFT → BIDDING → AWARDED → EXECUTION → COMPLETED stages. Contextual CTAs. | Next step visible |
| 9.3.4 | Workflow steps | ✅ Done | `frontend/src/views/ContractDetail.vue` | 4 steps: Publish tender, Review bids, Award/start execution, Track close-out. | Progress tracked |
| 9.3.5 | Summary stats | ✅ Done | `frontend/src/views/ContractDetail.vue` | Budget, deadline, status, bids, milestones, files. | Stats visible |
| 9.3.6 | Procurement snapshot | ✅ Done | `frontend/src/views/ContractDetail.vue` | Category, bid deadline, start date, completion date, currency. | Snapshot visible |
| 9.3.7 | Timeline steps | ✅ Done | `frontend/src/views/ContractDetail.vue` | Bid window, start, finish with state indicators. | Timeline visible |
| 9.3.8 | Sidebar quick view | ✅ Done | `frontend/src/views/ContractDetail.vue` | Status, category, owner, deadline. Bid form for contractors. Management buttons for owner. | Sidebar actionable |
| 9.3.9 | **Activity/event log** | ❌ Missing | `backend/contracts/models.py` + frontend | `ContractActivityEvent` model. Persistent audit trail: published, bid received, awarded, milestone updated. | History complete |
| 9.3.10 | **Contract document generation** | ❌ Missing | `frontend/src/views/ContractDetail.vue` + backend | Generate PDF from contract terms, scope, payment terms, clauses. Downloadable. | Document generated |
| 9.3.11 | **Contract versioning/amendments** | ❌ Missing | `backend/contracts/models.py` + frontend | `ContractVersion` model. Track changes to scope, budget, dates. Show diff. | Changes tracked |
| 9.3.12 | **Digital signature** | ❌ Missing | `frontend/src/views/ContractDetail.vue` + backend | E-signature integration (DocuSign/HelloSign). Status: PENDING_SIGNATURE → SIGNED. | Signatures digital |

---

## 9.4 Bid Management

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 9.4.1 | Bid submission | ✅ Done | `frontend/src/views/ContractDetail.vue` + backend | Contractor submits: proposed cost, timeline, message. `POST /contracts/{id}/bids/`. | Bids submit |
| 9.4.2 | Bid viewing (owner) | ✅ Done | `frontend/src/views/ContractDetail.vue` + backend | Owner sees all bids. Contractor sees own bid only. Sealed bidding. | Bids visible to owner |
| 9.4.3 | Bid shortlisting | ✅ Done | `frontend/src/views/ContractDetail.vue` + backend | "Shortlist" button. Status changes to SHORTLISTED. | Shortlisting works |
| 9.4.4 | Bid award | ✅ Done | `frontend/src/views/ContractDetail.vue` + backend | "Award Contract" button with confirmation modal. Status changes to AWARDED. Contract status updates. | Award works |
| 9.4.5 | My bid status | ✅ Done | `frontend/src/views/ContractDetail.vue` | Contractor sees their bid status badge. | Status visible |
| 9.4.6 | **Bid comparison matrix** | ❌ Missing | `frontend/src/views/ContractDetail.vue` | Side-by-side table: contractor, cost, timeline, rating, message excerpt. Sortable. | Bids comparable |
| 9.4.7 | **Automated bid scoring** | ❌ Missing | `backend/bids/views.py` + frontend | Score bids on: cost (40%), timeline (30%), contractor rating (20%), message quality (10%). | Scoring objective |
| 9.4.8 | **Bid rejection with reason** | ❌ Missing | `frontend/src/views/ContractDetail.vue` + backend | "Reject" button with reason: cost too high / timeline unrealistic / incomplete proposal. Notify contractor. | Feedback given |
| 9.4.9 | **Bid withdrawal** | ❌ Missing | `frontend/src/views/ContractDetail.vue` + backend | Contractor can withdraw bid before award. Status: WITHDRAWN. | Withdrawal possible |
| 9.4.10 | **Pre-qualification requirements** | ❌ Missing | `frontend/src/views/ContractDetail.vue` + backend | Owner sets required contractor class, insurance, certifications. System validates before bid submission. | Quality enforced |
| 9.4.11 | **Invitation-only tenders** | ❌ Missing | `backend/contracts/models.py` + frontend | `is_invitation_only` flag. Owner invites specific contractors. Only invited see tender. | Privacy controlled |

---

## 9.5 Milestones & Execution

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 9.5.1 | Milestone CRUD | ✅ Done | `frontend/src/views/ContractDetail.vue` + backend | Owner adds milestones: title, description, amount, due date. `POST /contracts/{id}/milestones/`. | Milestones manageable |
| 9.5.2 | Milestone display | ✅ Done | `frontend/src/views/ContractDetail.vue` | List with status badge (PENDING/COMPLETED/APPROVED/PAID). | Status visible |
| 9.5.3 | Milestone completion (contractor) | ✅ Done | `frontend/src/views/ContractDetail.vue` + backend | "Mark Complete" button. Status → COMPLETED. | Completion tracked |
| 9.5.4 | Milestone approval (owner) | ✅ Done | `frontend/src/views/ContractDetail.vue` + backend | "Release Funds" button. Status → APPROVED. | Approval works |
| 9.5.5 | **Milestone evidence upload** | ❌ Missing | `frontend/src/views/ContractDetail.vue` + backend | Contractor uploads photos/documents as completion evidence. Owner reviews before approval. | Evidence reviewable |
| 9.5.6 | **Escrow integration for payments** | ❌ Missing | `backend/milestones/views.py` + frontend | `MilestonePayment` model exists but not wired. On approval, auto-create escrow transaction. Release on owner confirmation. | Payments secured |
| 9.5.7 | **Milestone payment tracking** | ❌ Missing | `frontend/src/views/ContractDetail.vue` | Show payment status: Pending → Approved → Released → Received. Reference number. | Payments tracked |
| 9.5.8 | **Penalty clause tracking** | ❌ Missing | `backend/contracts/models.py` + frontend | `PenaltyClause` model: delay penalty %, max penalty, conditions. Auto-calculate if milestone overdue. | Penalties enforced |
| 9.5.9 | **Overdue milestone alerts** | ❌ Missing | `frontend/src/views/ContractDetail.vue` + backend | Alert banner when milestone past due date. Escalation to owner after 7 days. | Delays flagged |
| 9.5.10 | **Contract extension** | ❌ Missing | `frontend/src/views/ContractDetail.vue` + backend | "Request Extension" button. Contractor proposes new end date + reason. Owner approves/rejects. | Extensions manageable |

---

## 9.6 Attachments & Documents

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 9.6.1 | Attachment viewing | ✅ Done | `frontend/src/views/ContractDetail.vue` | Links to open attachments in new tab. Image preview. | Attachments viewable |
| 9.6.2 | **Attachment upload from detail** | ❌ Missing | `frontend/src/views/ContractDetail.vue` + backend | Upload drawings, BOQ, specs, photos. `POST /contracts/{id}/attachments/` multipart. | Upload in-context |
| 9.6.3 | **Attachment type validation** | ❌ Missing | `frontend/src/views/ContractDetail.vue` | Warn if required attachments missing before publish: drawings, BOQ, specs. | Completeness checked |

---

## 9.7 Contractor Tender Discovery

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 9.7.1 | Tender discovery page | ✅ Done | `frontend/src/views/ViewTenders.vue` | Simple grid with status, location, budget, "EXECUTE BID" button. | Tenders discoverable |
| 9.7.2 | Tender filters | ✅ Done | `frontend/src/views/ViewTenders.vue` | Status, deployment zone. | Filters basic |
| 9.7.3 | **Advanced tender discovery** | ❌ Missing | `frontend/src/views/ViewTenders.vue` | Budget range, category, deadline proximity, eligibility match (auto-filter by contractor certs). | Discovery refined |
| 9.7.4 | **Tender recommendation** | ❌ Missing | `frontend/src/views/ContractorDashboard.vue` + backend | "Recommended for you" based on contractor category, location, past performance. | Recommendations relevant |

---

## 9.8 Backend API Gaps

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 9.8.1 | Contract template endpoints | ❌ Missing | `backend/contracts/views.py` | `GET /contracts/templates/`. Returns template list with pre-filled fields. | Templates available |
| 9.8.2 | Attachment upload endpoint | ❌ Missing | `backend/contracts/views.py` | `POST /contracts/{id}/attachments/` multipart. Creates `ContractAttachment`. | Uploads work |
| 9.8.3 | Bid rejection endpoint | ❌ Missing | `backend/bids/views.py` | `POST /bids/{id}/reject/` with reason. Notifies contractor. | Rejection formalized |
| 9.8.4 | Bid withdrawal endpoint | ❌ Missing | `backend/bids/views.py` | `POST /bids/{id}/withdraw/`. Contractor can withdraw before award. | Withdrawal possible |
| 9.8.5 | Milestone evidence endpoint | ❌ Missing | `backend/milestones/views.py` | `POST /milestones/{id}/evidence/` multipart upload. | Evidence attachable |
| 9.8.6 | Milestone payment release endpoint | ❌ Missing | `backend/milestones/views.py` | `POST /milestones/{id}/release-payment/`. Triggers escrow release. | Payments released |
| 9.8.7 | Contract activity log endpoint | ❌ Missing | `backend/contracts/views.py` | `GET /contracts/{id}/activity/`. Event-sourced with actor, action, timestamp. | Activity persistent |
| 9.8.8 | Contract version endpoints | ❌ Missing | `backend/contracts/views.py` | `GET/POST /contracts/{id}/versions/`. Track amendments. | Versions tracked |
| 9.8.9 | Penalty clause endpoints | ❌ Missing | `backend/contracts/views.py` | CRUD for `PenaltyClause`. Auto-calculate on overdue. | Penalties automated |

---

## 9.9 Mobile & Accessibility

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 9.9.1 | Responsive contract list | ✅ Done | `frontend/src/views/ContractList.vue` | Grid/list toggle, filters collapse on mobile. | Mobile layout works |
| 9.9.2 | Responsive contract detail | ✅ Done | `frontend/src/views/ContractDetail.vue` | Tabs accessible on mobile. Bid form stacks. | Mobile layout works |
| 9.9.3 | **Contractor mobile bid submission** | ❌ Missing | `frontend/src/views/ContractDetail.vue` | Simplified bid form for mobile. Photo attachment for portfolio. | Mobile bidding easy |

---

# 10. ADMIN MODULE

**Blueprint:** `ADMIN_MODULE_WORKFLOW_UX_TRANSFORM.md`  
**Frontend Root:** `frontend/src/views/AdminDashboard.vue`, `frontend/src/components/admin/OverviewSection.vue`, `frontend/src/components/admin/VerificationsSection.vue`, `frontend/src/components/admin/ModerationSection.vue`, `frontend/src/components/admin/UserManagementSection.vue`, `frontend/src/components/admin/SecurityMonitorSection.vue`, `frontend/src/components/admin/PropertiesSection.vue`, `frontend/src/components/admin/ReportsSection.vue`, `frontend/src/components/admin/SystemConfigSection.vue`  
**Backend Root:** `backend/disputes/`, `backend/reporting/`, `backend/risk/`, `backend/scoring/`, `backend/rbac/`, `backend/compliance/`

---

## 10.1 Admin Dashboard Shell

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 10.1.1 | Admin dashboard shell | ✅ Done | `frontend/src/views/AdminDashboard.vue` | `DashboardShell` with 8 tabs: Overview, Verifications, Real Estate, Moderation, Reports, Operators, Security, Settings. | Shell renders |
| 10.1.2 | Workflow card | ✅ Done | `frontend/src/views/AdminDashboard.vue` | Stage-aware guidance: START_HERE → QUEUE → OVERSIGHT. | Banner contextual |
| 10.1.3 | Tab switching with transition | ✅ Done | `frontend/src/views/AdminDashboard.vue` | Fade transition between tabs. Lazy-loaded components. | Transitions smooth |
| 10.1.4 | Add user modal | 🔄 Partial | `frontend/src/views/AdminDashboard.vue` | Modal opens but shows placeholder text: "User management is currently active. Please use the central portal." | Modal placeholder |

---

## 10.2 Overview & Platform Health

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 10.2.1 | Command node stats | ✅ Done | `frontend/src/components/admin/OverviewSection.vue` | ACTIVE_OPERATORS, AUDIT_EVENTS, PENDING_NODES, OPEN_DISPUTES. | Stats visible |
| 10.2.2 | Audit log terminal | ✅ Done | `frontend/src/components/admin/OverviewSection.vue` | Terminal-style display of `/rbac/audit-logs/`. Timestamp, actor, action, resource. | Logs visible |
| 10.2.3 | Multi-source data fetch | ✅ Done | `frontend/src/components/admin/OverviewSection.vue` | Fetches: audit logs, contractors, vendors, kyc, pending contracts, disputes, operators. | Data aggregated |
| 10.2.4 | **Platform health metrics** | ❌ Missing | `frontend/src/components/admin/OverviewSection.vue` + backend | Active users (24h), new registrations (7d), transaction volume, revenue, listing approval rate. | Health measured |
| 10.2.5 | **Real-time alert center** | ❌ Missing | `frontend/src/views/AdminDashboard.vue` + backend | Notification bell with unread count. Alerts: fraud detected, dispute opened, verification pending >48h. | Alerts real-time |
| 10.2.6 | **Health trend charts** | ❌ Missing | `frontend/src/components/admin/OverviewSection.vue` + backend | Line charts: users over time, disputes over time, revenue over time. | Trends visible |

---

## 10.3 Verification Queue

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 10.3.1 | Verification queue shell | ✅ Done | `frontend/src/components/admin/VerificationsSection.vue` | 3 queues: Pending Contractors, Pending Vendors, Pending KYC. | Queues visible |
| 10.3.2 | Pending counts | ✅ Done | `frontend/src/components/admin/VerificationsSection.vue` | Command nodes show queue lengths. | Counts visible |
| 10.3.3 | Approval/Reject actions | ✅ Done | `frontend/src/components/admin/VerificationsSection.vue` | Approve/Reject buttons per row. Loading state. Refresh after action. | Actions functional |
| 10.3.4 | Empty states | ✅ Done | `frontend/src/components/admin/VerificationsSection.vue` | Each queue has empty state with glyph and message. | Empty states helpful |
| 10.3.5 | **KYC document viewer** | ❌ Missing | `frontend/src/components/admin/VerificationsSection.vue` + backend | Click to view uploaded KYC documents (ID, business cert, tax docs). Inline preview or modal. | Documents reviewable |
| 10.3.6 | **Batch approval** | ❌ Missing | `frontend/src/components/admin/VerificationsSection.vue` + backend | Checkbox per row. "Approve Selected" / "Reject Selected" bulk actions. | Batch efficient |
| 10.3.7 | **Verification notes** | ❌ Missing | `frontend/src/components/admin/VerificationsSection.vue` + backend | Textarea for rejection reason. Stored per decision. Audit trail. | Reasons recorded |
| 10.3.8 | **Risk score in queue** | ❌ Missing | `frontend/src/components/admin/VerificationsSection.vue` + backend | Display `RiskScore.fraud_score` and `ReliabilityScore.risk_tier` per applicant. | Risk visible |
| 10.3.9 | **Auto-approval rules** | ❌ Missing | `backend/scoring/views.py` + frontend | Auto-approve if risk score <20, all docs uploaded, no compliance alerts. | Low-risk fast-tracked |

---

## 10.4 Moderation & Disputes

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 10.4.1 | Dispute arbitration queue | ✅ Done | `frontend/src/components/admin/ModerationSection.vue` | Table: ID, channel, reason, status, evidence count. | Disputes visible |
| 10.4.2 | Dispute resolution actions | ✅ Done | `frontend/src/components/admin/ModerationSection.vue` + backend | RELEASE or REFUND buttons for resolvable disputes. | Resolution functional |
| 10.4.3 | Dispute status badges | ✅ Done | `frontend/src/components/admin/ModerationSection.vue` | Color-coded: warning (OPENED), info (UNDER_REVIEW), success (RELEASE), danger (REFUND). | Status clear |
| 10.4.4 | **Dispute detail view** | ❌ Missing | `frontend/src/components/admin/ModerationSection.vue` + backend | Expand row to see: full description, evidence files, involved parties, timeline, related orders/contracts. | Context complete |
| 10.4.5 | **Evidence review** | ❌ Missing | `frontend/src/components/admin/ModerationSection.vue` + backend | View uploaded evidence files. Image preview, document download. | Evidence reviewable |
| 10.4.6 | **Content moderation (listings)** | ❌ Missing | `frontend/src/components/admin/ModerationSection.vue` + backend | Queue for flagged products, properties, contracts. Approve/Hide/Remove actions. | Content moderated |
| 10.4.7 | **Fraud pattern detection** | ❌ Missing | `frontend/src/components/admin/ModerationSection.vue` + backend | Detect: duplicate accounts, suspicious bidding patterns, refund abuse. Alert banner. | Fraud detected |
| 10.4.8 | **Escalation rules** | ❌ Missing | `backend/disputes/views.py` + frontend | Auto-escalate dispute to senior admin if unresolved >7 days. Notify on Slack/email. | Escalation automated |

---

## 10.5 User Management

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 10.5.1 | Operator registry | ✅ Done | `frontend/src/components/admin/UserManagementSection.vue` | Table: name, email, role, RBAC groups, status. | Operators visible |
| 10.5.2 | Toggle active/locked | ✅ Done | `frontend/src/components/admin/UserManagementSection.vue` + backend | DEACTIVATE/ACTIVATE button per user. | Status toggleable |
| 10.5.3 | **User detail view** | ❌ Missing | `frontend/src/components/admin/UserManagementSection.vue` + backend | Click row to see: profile, activity history, risk score, disputes, linked entities. | Detail accessible |
| 10.5.4 | **Role assignment** | ❌ Missing | `frontend/src/components/admin/UserManagementSection.vue` + backend | Dropdown to assign RBAC roles/groups. Save via API. | Roles manageable |
| 10.5.5 | **User creation** | ❌ Missing | `frontend/src/components/admin/UserManagementSection.vue` + backend | "Add Operator" modal with actual form: name, email, role, password. POST to create. | Creation functional |

---

## 10.6 Security Monitoring

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 10.6.1 | Security stats | ✅ Done | `frontend/src/components/admin/SecurityMonitorSection.vue` | ACTIVE_THROTTLES_24H, UNIQUE_IPS_BLOCKED, CRITICAL_SCOPES_HIT. | Stats visible |
| 10.6.2 | Throttle violation log | ✅ Done | `frontend/src/components/admin/SecurityMonitorSection.vue` + backend | Table: timestamp, IP, operator, resource path, scope. | Violations logged |
| 10.6.3 | **IP blocking management** | ❌ Missing | `frontend/src/components/admin/SecurityMonitorSection.vue` + backend | Block/unblock IP addresses. View blocked list. Duration setting. | IPs manageable |
| 10.6.4 | **Login anomaly detection** | ❌ Missing | `frontend/src/components/admin/SecurityMonitorSection.vue` + backend | Alert on: multiple failed logins, impossible travel, new device. | Anomalies detected |
| 10.6.5 | **Session management** | ❌ Missing | `frontend/src/components/admin/SecurityMonitorSection.vue` + backend | View active sessions. Force logout per session or per user. | Sessions controllable |

---

## 10.7 Reports & Analytics

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 10.7.1 | Reports section shell | ✅ Done | `frontend/src/components/admin/ReportsSection.vue` | Reports UI exists (~28KB). | Section renders |
| 10.7.2 | **Report export** | ❌ Missing | `frontend/src/components/admin/ReportsSection.vue` + backend | Export: CSV, PDF, XLSX. Date range selector. | Exports functional |
| 10.7.3 | **Scheduled reports** | ❌ Missing | `backend/reporting/views.py` + frontend | Schedule daily/weekly/monthly reports. Email delivery. | Reports automated |
| 10.7.4 | **Custom report builder** | ❌ Missing | `frontend/src/components/admin/ReportsSection.vue` + backend | Drag fields, filters, group by. Save report templates. | Builder flexible |

---

## 10.8 System Configuration

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 10.8.1 | System config section | ✅ Done | `frontend/src/components/admin/SystemConfigSection.vue` | Large config UI (~65KB). | Config editable |
| 10.8.2 | **Config versioning** | ❌ Missing | `backend/platform_settings/views.py` + frontend | Track config changes. Rollback to previous version. | Changes safe |
| 10.8.3 | **Feature flags** | ❌ Missing | `backend/platform_settings/views.py` + frontend | Toggle features on/off per environment. A/B test groups. | Features controllable |

---

## 10.9 Backend API Gaps

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 10.9.1 | Risk score exposure | ❌ Missing | `backend/risk/views.py` | `GET /risk/scores/` and `GET /risk/scores/{user_id}/`. | Scores accessible |
| 10.9.2 | Compliance alert endpoints | ❌ Missing | `backend/risk/views.py` | `GET/POST /risk/compliance-alerts/`. CRUD for alerts. | Alerts manageable |
| 10.9.3 | Reliability score exposure | ❌ Missing | `backend/scoring/views.py` | `GET /scoring/reliability/{user_id}/`. | Scores accessible |
| 10.9.4 | Platform analytics endpoint | ❌ Missing | `backend/reporting/views.py` | `GET /reporting/platform-health/`. Returns users, transactions, revenue, disputes. | Analytics available |
| 10.9.5 | Batch verification endpoint | ❌ Missing | `backend/compliance/views.py` | `POST /compliance/batch-verify/` with list of IDs and action. | Batch efficient |
| 10.9.6 | Content moderation endpoints | ❌ Missing | `backend/catalog/views.py` + `backend/property/views.py` | `POST /{resource}/{id}/moderate/` with action: approve, hide, remove. | Content moderated |
| 10.9.7 | IP block endpoints | ❌ Missing | `backend/security/views.py` | `POST/GET/DELETE /security/ip-blocks/`. | IPs manageable |

---

## 10.10 Mobile & Accessibility

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 10.10.1 | Responsive admin dashboard | ✅ Done | `frontend/src/views/AdminDashboard.vue` | `DashboardShell` adapts to mobile. Tabs accessible. | Mobile layout works |
| 10.10.2 | **Admin mobile alert notifications** | ❌ Missing | `frontend/src/views/AdminDashboard.vue` + backend | Push notifications for critical alerts: dispute opened, fraud detected, verification pending >48h. | Alerts real-time |

---

# 11. GOVERNMENT MODULE

**Blueprint:** `GOVERNMENT_MODULE_WORKFLOW_UX_TRANSFORM.md`  
**Frontend Root:** `frontend/src/views/GovernmentDashboard.vue`  
**Backend Root:** `backend/government/`

---

## 11.1 Government Dashboard

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 11.1.1 | Government dashboard shell | 🔄 Partial | `frontend/src/views/GovernmentDashboard.vue` | `DashboardShell` with single "Tender Overview" tab. Workflow card with DISCOVERY stage. | Shell renders |
| 11.1.2 | Public tender link | ✅ Done | `frontend/src/views/GovernmentDashboard.vue` | "View Public Tenders" button routes to `/tenders`. | Navigation works |
| 11.1.3 | Buyer workspace link | ✅ Done | `frontend/src/views/GovernmentDashboard.vue` | "Return to Project Owner Workspace" button routes to `/buyer/dashboard`. | Navigation works |
| 11.1.4 | **Government tender publishing UI** | ❌ Missing | `frontend/src/views/GovernmentTenderPublish.vue` (new) | Form: title, description, issuing authority, location, bid deadline, category, budget, eligibility criteria, required documents. | Tenders publishable |
| 11.1.5 | **Government tender list/management** | ❌ Missing | `frontend/src/views/GovernmentTenderList.vue` (new) | Table: all government tenders with status, bids count, deadline. Filter by status. | Tenders manageable |
| 11.1.6 | **Government tender detail workspace** | ❌ Missing | `frontend/src/views/GovernmentTenderDetail.vue` (new) | Tabs: Overview, Bids, Evaluation, Award, Oversight. Workflow banner. | Workspace complete |
| 11.1.7 | **Compliance review panel** | ❌ Missing | `frontend/src/views/GovernmentTenderDetail.vue` | Check bidder qualifications: tax compliance, certifications, past performance. Pass/fail per criterion. | Compliance enforced |
| 11.1.8 | **Award transparency page** | ❌ Missing | `frontend/src/views/GovernmentAwardTransparency.vue` (new) | Public page: tender title, bidders (anonymized), evaluation scores, winning bidder, award amount, award date. | Transparency ensured |
| 11.1.9 | **Supplier certification enforcement** | ❌ Missing | `frontend/src/views/GovernmentTenderDetail.vue` + backend | Block bid submission if contractor lacks required certifications. Display missing certs. | Certs enforced |
| 11.1.10 | **Anti-corruption audit log viewer** | ❌ Missing | `frontend/src/views/GovernmentTenderDetail.vue` + backend | Immutable timeline: published, bid opened, evaluated, awarded, amended. Actor, timestamp, IP. | Audit immutable |

---

## 11.2 Backend API

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 11.2.1 | PublicTender CRUD | ✅ Done | `backend/government/views.py` | `PublicTenderViewSet` with create, list, retrieve, update, delete. Proximity search. | API functional |
| 11.2.2 | AuditLog model | ✅ Done | `backend/government/models.py` | `AuditLog` linked to `PublicTender`. | Logs storable |
| 11.2.3 | **Bid submission for public tenders** | ❌ Missing | `backend/government/views.py` | `POST /government/tenders/{id}/bids/`. Separate from private contract bids. | Bids accepted |
| 11.2.4 | **Evaluation scoring endpoint** | ❌ Missing | `backend/government/views.py` | `POST /government/tenders/{id}/evaluate/` with criteria scores. Weighted total. | Evaluation objective |
| 11.2.5 | **Award endpoint** | ❌ Missing | `backend/government/views.py` | `POST /government/tenders/{id}/award/` with bid_id, award amount, award date. Auto-notify all bidders. | Award formalized |
| 11.2.6 | **Compliance check endpoint** | ❌ Missing | `backend/government/views.py` | `GET /government/tenders/{id}/compliance/{bid_id}/`. Returns qualification pass/fail per criterion. | Compliance checkable |
| 11.2.7 | **Audit log exposure** | ❌ Missing | `backend/government/views.py` | `GET /government/tenders/{id}/audit-log/`. Immutable, append-only. | Audit viewable |
| 11.2.8 | **Government reporting endpoint** | ❌ Missing | `backend/government/views.py` | `GET /government/reports/`. Tender participation, award fairness, execution progress. | Reports available |

---

## 11.3 Cross-Cutting Gaps

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 11.3.1 | **Government role & RBAC** | 🔄 Partial | `backend/rbac/permissions.py` | `GOVERNMENT` role exists but no dedicated government namespace permissions beyond `government:view` and `government:publish_tender`. | Permissions granular |
| 11.3.2 | **Government onboarding** | ❌ Missing | `frontend/src/views/GovernmentOnboarding.vue` (new) | Verify government email domain, agency registration, authorized signatory. | Onboarding verified |
| 11.3.3 | **Tender document management** | ❌ Missing | `backend/government/models.py` + frontend | `TenderDocument` model: RFP, terms of reference, BOQ, drawings. Upload/download. | Documents manageable |
| 11.3.4 | **Bid bond tracking** | ❌ Missing | `backend/government/models.py` + frontend | `BidBond` model: amount, expiry, status. Required for bids above threshold. | Bonds tracked |
| 11.3.5 | **Performance bond tracking** | ❌ Missing | `backend/government/models.py` + frontend | `PerformanceBond` model: amount, expiry, status. Required after award. | Bonds tracked |

---

## 11.4 Mobile & Accessibility

| # | Task | Status | File(s) | Exact Change Required | Acceptance Criteria |
|---|------|--------|---------|----------------------|---------------------|
| 11.4.1 | Responsive government dashboard | ✅ Done | `frontend/src/views/GovernmentDashboard.vue` | `DashboardShell` adapts to mobile. | Mobile layout works |
| 11.4.2 | **Public tender mobile browsing** | ❌ Missing | `frontend/src/views/ViewTenders.vue` | Mobile-optimized tender cards. Filter drawer. | Mobile browsing easy |

---

# APPENDIX A: Component Naming Convention

When creating new components, use this pattern so LLMs can locate them predictably:

```
{Module}{Feature}{Type}.vue

Examples:
- VendorPublishPage.vue          (full-page wizard)
- VendorCsvImportWizard.vue      (3-step import)
- VendorPerformanceChart.vue     (analytics)
- VendorWorkspaceHeader.vue      (already exists)
- PropertyListingWizard.vue      (property equivalent)
- PropertyManagerWorkspace.vue   (dashboard shell)
- PropertyDetailPage.vue         (public detail)
- PropertyMarketView.vue         (discovery/browse)
- BuyerShortlistSidebar.vue      (buyer equivalent)
- BuyerQuoteCart.vue             (multi-item cart)
- BuyerOrderTimeline.vue         (fulfillment timeline)
- BuyerComparisonMatrix.vue      (decision support)
- OwnerProjectWizard.vue         (project creation)
- OwnerEscrowPanel.vue           (financial status)
- OwnerBidComparison.vue         (bid evaluation)
- OwnerMilestoneTimeline.vue     (milestone gantt)
- InvestorOnboardingWizard.vue   (KYC & accreditation)
- InvestorPortfolioChart.vue     (returns analytics)
- InvestorDealRoom.vue           (data room)
- InvestorCapitalCall.vue        (funding notice)
- ContractorOnboardingWizard.vue (verification flow)
- ContractorJobWorkspace.vue     (execution workspace)
- ContractorBidWorkspace.vue     (bid preparation)
- ContractorCrewScheduler.vue    (workforce calendar)
- ContractorPaymentTracker.vue   (drawdown status)
- CourierOnboardingWizard.vue    (fleet & docs)
- CourierDriverView.vue          (mobile driver UI)
- CourierPodCapture.vue          (proof of delivery)
- CourierRouteOptimizer.vue      (multi-stop route)
- ProjectCreateWizard.vue        (multi-step project setup)
- ProjectWorkspace.vue           (project detail shell)
- ProjectGanttChart.vue          (phase/milestone timeline)
- ProjectBudgetTracker.vue       (budget vs actual)
- ProjectBomBuilder.vue          (hierarchical requirements)
- ProjectTeamManager.vue         (member roles & permissions)
- ContractTemplateSelector.vue   (standard clause templates)
- ContractBidComparison.vue      (side-by-side bid matrix)
- ContractMilestoneEvidence.vue  (completion proof review)
- ContractDocumentGenerator.vue  (PDF export)
- ContractPenaltyTracker.vue     (delay penalty calculation)
- AdminVerificationQueue.vue     (KYC/approval table)
- AdminRiskScoreCard.vue         (fraud/reliability display)
- AdminDisputeArbitration.vue    (evidence & resolution)
- AdminPlatformHealth.vue        (metrics & trend charts)
- AdminContentModeration.vue     (flagged listings queue)
- AdminSecurityMonitor.vue       (violations & anomalies)
- GovernmentTenderPublish.vue    (public tender creation)
- GovernmentBidEvaluation.vue    (scoring & compliance)
- GovernmentAwardTransparency.vue (public award page)
- GovernmentAuditTrail.vue       (immutable action log)
- GovernmentCompliancePanel.vue  (bidder qualification)
```

---

# APPENDIX B: Priority Order for Implementation

**Phase 1 — Vendor Quick Wins (1–2 sprints)**
1. Step-level wizard gating (1.2.9)
2. Performance metrics strip (1.3.9)
3. Quote response coaching (1.5.5)
4. Stock-out prediction banner (1.4.4)
5. CSV validation endpoint + preview (1.6.4, 1.11.2)

**Phase 2 — Property Quick Wins (1–2 sprints)**
6. Step-level validation gating (2.1.7)
7. Buyer trust signals on detail page (2.3.13)
8. Inquiry response coaching + overdue escalation (2.5.6, 2.5.7)
9. Property grouping by operational state (2.4.15)
10. Backend property analytics endpoint (2.9.1)

**Phase 3 — Buyer Quick Wins (1–2 sprints)**
11. Shortlist backend + frontend heart icons (3.6.2, 3.8.1)
12. Vendor scorecard on product detail (3.3.8)
13. Multi-item quote cart (3.4.5)
14. Order detail page with fulfillment timeline (3.5.7, 3.5.8)
15. Quote comparison matrix for multiple responses (3.6.5)

**Phase 4 — Owner Quick Wins (1–2 sprints)**
16. Milestone approval UI (4.5.7)
17. Escrow deposit UI + balance display (4.5.8, 4.5.9)
18. Real escrow data in dashboard (4.1.8)
19. Bid comparison matrix (4.4.10)
20. Project creation wizard with templates (4.2.4, 4.2.5)

**Phase 5 — Investor Quick Wins (1–2 sprints)**
21. Investor onboarding wizard with KYC upload (5.2.4, 5.2.5)
22. Portfolio analytics charts + transaction API (5.1.8, 5.5.2, 5.5.4)
23. Pledge → Agreement conversion workflow (5.4.6)
24. Investor opportunity watchlist (5.1.12, 5.3.6)
25. Risk scoring display on projects (5.3.5)

**Phase 6 — Contractor Quick Wins (1–2 sprints)**
26. Contractor onboarding wizard with cert upload (6.1.4, 6.1.5)
27. Real dashboard analytics (6.2.7)
28. Payment drawdown tracking (6.5.3)
29. Milestone progress evidence upload (6.4.4)
30. Auto-escrow release on milestone approval (6.5.4)

**Phase 7 — Courier Quick Wins (1–2 sprints)**
31. Document upload backend wiring (7.1.5)
32. Shipment assignment accept/reject (7.3.6)
33. Proof of Delivery capture (7.3.7)
34. Courier driver mobile view (7.3.10)
35. Real carrier tracking integrations (7.3.11)

**Phase 8 — Project Quick Wins (1–2 sprints)**
36. Project status transition controls (8.3.14)
37. Budget vs actual tracking endpoint (8.8.5)
38. Bulk quote request from requirements (8.4.5)
39. Project document upload (8.3.11)
40. Event-sourced activity feed (8.3.10)

**Phase 9 — Contract Quick Wins (1–2 sprints)**
41. Bid comparison matrix (9.4.7)
42. Milestone evidence upload + review (9.5.5)
43. Contract document generation (9.3.10)
44. Attachment upload from detail (9.6.2)
45. Bid rejection with reason (9.4.8)

**Phase 10 — Admin Quick Wins (1–2 sprints)**
46. KYC document viewer (10.3.5)
47. Risk score in verification queue (10.3.8)
48. Dispute detail view with evidence (10.4.4)
49. Batch approval actions (10.3.6)
50. Platform health metrics (10.2.4)

**Phase 11 — Government Quick Wins (1–2 sprints)**
51. Government tender publishing UI (11.1.4)
52. Government tender list/management (11.1.5)
53. Bid submission for public tenders (11.2.3)
54. Anti-corruption audit log viewer (11.1.10)
55. Award transparency page (11.1.8)

**Phase 12 — Cross-Module Continuity (2–3 sprints)**
56. Project BOM → Quote Request flow (3.7.5)
57. Persistent event-sourced timelines (all modules)
58. Order ↔ Delivery ↔ Escrow workflow linking
59. Buyer trust signals (vendor health, response time)
60. Unified notification center across all modules

**Phase 13 — Mobile & Accessibility (ongoing)**
61. Mobile bottom nav + field operations mode
62. Offline queue for critical actions
63. Full WCAG 2.1 AA audit

---

*End of Spec*
