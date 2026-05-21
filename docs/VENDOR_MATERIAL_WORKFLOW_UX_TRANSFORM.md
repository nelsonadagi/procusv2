# Vendor Material Publishing & Catalog Discovery — Workflow-First UX Transformation

**Module:** Vendor Inventory / Material Catalog  
**Date:** 2026-05-17  
**Status:** Design Blueprint — Ready for Implementation

---

# 1. MODULE EXPERIENCE VISION

## What the User Is Trying to Accomplish

A vendor is not "creating database records." A vendor is **launching a product into a marketplace** so that buyers can find it, trust it, and request quotes for it. The operational goal is: *get materials discovered, quoted, and sold with minimal friction.*

A buyer is not "browsing a catalog." A buyer is **solving a procurement problem** — finding the right material, from a trustworthy supplier, at the right price and lead time, that can be delivered to their project site.

## Emotional / Operational State

| Actor | Emotional State | Operational State |
|-------|----------------|-------------------|
| **New Vendor** | Anxious, uncertain, wants legitimacy | Has materials to sell but doesn't know if they're "doing it right" |
| **Approved Vendor** | Busy, wants efficiency, hates repetition | Managing inventory, prices, stock levels across many SKUs |
| **Buyer** | Time-pressured, risk-averse, comparison-shopping | Needs to compare options, validate specs, and get quotes fast |
| **Admin** | Oversight-focused, quality-conscious, bottleneck-aware | Needs to approve vendors, spot bad listings, enforce compliance |

## What Makes the Current UX Difficult

1. **The vendor sees a form, not a launch workflow.** Five tabs (Commercial, Technical, Compliance, Documents, Media) feel like a tax form, not a product launch.
2. **No sense of "done."** A vendor can save a product that has no images, no description, no certifications — and think it's ready. The system doesn't tell them what's missing.
3. **Approval is invisible.** A pending vendor can create products, invest time, and not realize those products are invisible to buyers.
4. **Buyers face decision fatigue.** The product list is dense with filters but offers no guidance on *what to prioritize* — cheapest? closest? best certified?
5. **No continuity between discovery and action.** A buyer finds a product, then has to figure out how to request a quote, how much to ask for, and what happens next.
6. **Inventory management is reactive.** Vendors only know stock is low when they manually check. The system doesn't guide them to restock.
7. **CSV import is a black box.** Upload → hope it works → maybe get errors. No preview, no validation, no recovery.

## What the Ideal Workflow Should Feel Like

> "The system understands I want to sell cement. It tells me exactly what buyers need to see to trust my listing. It warns me before I publish something incomplete. It reminds me when stock is low. It makes my materials easy to find and easy to buy."

The module should behave like a **product launch assistant**, not a CMS:
- It guides the vendor through launch readiness (like a pre-flight checklist).
- It surfaces what's blocking visibility to buyers.
- It tells the vendor what buyers care about most (price, stock, certifications, delivery).
- It tells the buyer which product best matches their needs.
- It predicts what will go wrong before it happens.

---

# 2. USER GOALS

## Vendor (Supplier)

### Primary Goals
1. **Get approved** so I can start selling
2. **Publish materials** that buyers can find and trust
3. **Keep inventory accurate** so I don't get orders I can't fulfill
4. **Respond to quotes** quickly to win business

### Secondary Goals
5. Import my catalog via CSV instead of manual entry
6. Highlight my best products (featured, new arrival, on sale)
7. Track which materials are getting views and quotes
8. Maintain compliance documentation for audits

### Urgent Goals
9. Fix low-stock items before I lose orders
10. Update prices when costs change
11. Respond to quote requests before buyers go elsewhere

### Recurring Operational Goals
12. Weekly stock reconciliation
13. Monthly price review
14. Quarterly certification renewal check

---

## Buyer (Project Owner / Contractor)

### Primary Goals
1. **Find the right material** for my project
2. **Compare options** across price, quality, delivery, and trust
3. **Request a quote** with the right quantity
4. **Track my quote** through to order

### Secondary Goals
5. Filter by location to minimize delivery cost/time
6. Verify certifications for compliance requirements
7. Save favorite products or vendors for later
8. Reorder previously purchased materials

### Urgent Goals
9. Find in-stock alternatives when preferred item is unavailable
10. Get quotes fast for time-sensitive projects
11. Validate that a vendor is approved and trustworthy

---

## Admin

### Primary Goals
1. Approve legitimate vendors quickly
2. Reject or suspend problematic vendors
3. Ensure catalog quality (no spam, no incomplete listings)
4. Monitor marketplace health (vendor fulfillment, buyer satisfaction)

### Urgent Goals
5. Review vendors with repeated buyer complaints
6. Identify and remove fraudulent listings
7. Escalate disputes before they escalate to refunds

---

# 3. WORKFLOW-FIRST UX REDESIGN

## Core Workflow: Material Launch

```
[Vendor Onboarding Complete]
    → [Approval Granted]
        → [Start Material Launch]
            → [Commercial Setup]
                → [Technical Specs]
                    → [Compliance Upload]
                        → [Media Upload]
                            → [Readiness Review]
                                → [Publish]
                                    → [Buyer Discovery]
                                        → [Quote Request]
                                            → [Vendor Response]
                                                → [Order Commit]
                                                    → [Delivery]
                                                        → [Completion]
```

---

## Workflow Stage Definitions

### Stage: Vendor Approval Pending

| Field | Value |
|-------|-------|
| **What User Sees** | "Your vendor profile is under review. You'll be notified once approved." |
| **Main CTA** | "View My Profile" (read-only preview) |
| **Secondary Actions** | Edit profile, Upload additional documents |
| **Blockers** | Cannot publish materials, cannot receive quotes, invisible to buyers |
| **Guidance** | "While you wait, prepare your product catalog using the CSV template so you can publish immediately after approval." |

**System Behavior:**
- Show a countdown/queue position if possible
- Provide the CSV template download
- Show a checklist of what will be needed post-approval
- Do NOT show the "Add Material" button (it creates false hope)

---

### Stage: Ready to Launch

| Field | Value |
|-------|-------|
| **What User Sees** | "You're approved! Let's publish your first material." |
| **Main CTA** | "Publish New Material" |
| **Secondary Actions** | Import catalog via CSV, View marketplace guide |
| **Blockers** | None |
| **Guidance** | "Complete products get 3x more quotes. Follow the checklist to maximize visibility." |

---

### Stage: Material Setup — Commercial

| Field | Value |
|-------|-------|
| **What User Sees** | "Step 1 of 5: Commercial Setup — What are you selling and for how much?" |
| **Main CTA** | "Continue to Technical Specs" |
| **Secondary Actions** | Save as draft, Preview listing |
| **Blockers** | Name, category, unit, base_price, description are required |
| **Guidance** | Inline tips: "Buyers filter by category first. Choose the most specific category." / "Set a bulk price to attract large project orders." |

**Smart Behaviors:**
- Auto-suggest category based on product name
- Currency defaults to vendor's country currency
- Slug auto-generates from name in real-time
- Show "Listing Strength" meter that updates as fields are filled

---

### Stage: Material Setup — Technical

| Field | Value |
|-------|-------|
| **What User Sees** | "Step 2 of 5: Technical Details — Help buyers specify the right material." |
| **Main CTA** | "Continue to Compliance" |
| **Secondary Actions** | Save as draft, Go back |
| **Blockers** | None (all optional) |
| **Guidance** | "Projects often require specific dimensions, weight, or grade. The more detail, the fewer 'is this compatible?' questions you'll get." |

---

### Stage: Material Setup — Compliance

| Field | Value |
|-------|-------|
| **What User Sees** | "Step 3 of 5: Compliance — Build trust with certifications." |
| **Main CTA** | "Continue to Documents" |
| **Secondary Actions** | Skip for now, Go back |
| **Blockers** | None |
| **Guidance** | "Government and enterprise buyers filter by certification. KEBS, ISO 9001, and CE Mark are the most searched." |

---

### Stage: Material Setup — Documents

| Field | Value |
|-------|-------|
| **What User Sees** | "Step 4 of 5: Documents — Upload datasheets, warranties, and safety sheets." |
| **Main CTA** | "Continue to Photos" |
| **Secondary Actions** | Skip for now, Go back |
| **Blockers** | None |
| **Guidance** | "Buyers download datasheets before requesting quotes. Products with documents get 40% more engagement." (metric can be real or illustrative) |

---

### Stage: Material Setup — Media

| Field | Value |
|-------|-------|
| **What User Sees** | "Step 5 of 5: Photos — Show buyers what they're getting." |
| **Main CTA** | "Review & Publish" |
| **Secondary Actions** | Save as draft, Go back |
| **Blockers** | None (but system warns if no images) |
| **Guidance** | "Products with 3+ high-quality images receive 5x more views." |

---

### Stage: Readiness Review

| Field | Value |
|-------|-------|
| **What User Sees** | A preview of the listing AS THE BUYER WOULD SEE IT, with a readiness checklist |
| **Main CTA** | "Publish to Marketplace" |
| **Secondary Actions** | Edit any section, Save as draft |
| **Blockers** | Critical: Missing name, price, category. Warning: No images, no description, no certifications |
| **Guidance** | Readiness meter: "Your listing is 70% complete. Adding photos and certifications will boost visibility." |

**Readiness Checklist:**
- ✅ Commercial info complete
- ✅ Price set
- ⚠️ No images (reduces visibility)
- ⚠️ No certifications (buyers may skip)
- ✅ Ready to publish

---

### Stage: Published & Live

| Field | Value |
|-------|-------|
| **What User Sees** | "Your material is live! Here's what happens next." |
| **Main CTA** | "Add Another Material" |
| **Secondary Actions** | View public listing, Share link, Edit, Duplicate |
| **Blockers** | None |
| **Guidance** | "Buyers will now see your material in search results. You'll receive quote requests via email and dashboard notifications." |

---

### Stage: Buyer Discovery

| Field | Value |
|-------|-------|
| **What User Sees** | Search results, comparison cards, filter guidance |
| **Main CTA** | "Request Quote" |
| **Secondary Actions** | Compare, Save, View details, Contact vendor |
| **Blockers** | OUT_OF_STOCK products cannot be quoted |
| **Guidance** | "3 suppliers near your project location. Filter by delivery time to narrow down." |

---

### Stage: Quote Requested

| Field | Value |
|-------|-------|
| **What Vendor Sees** | "New quote request for [Material Name] — Respond within 24h for best conversion." |
| **Main CTA** | "Review & Respond" |
| **Secondary Actions** | View buyer profile, Decline with reason |
| **Blockers** | Product must be ACTIVE and in stock |
| **Guidance** | "Your average response time is 4 hours. Responding within 2 hours increases win rate by 35%." |

---

## Stage Transitions (System Rules)

| From | To | Trigger | Auto-Actions |
|------|-----|---------|--------------|
| DRAFT | ACTIVE | Vendor clicks "Publish" | Index for search, notify followers |
| ACTIVE | OUT_OF_STOCK | Stock hits 0 OR vendor sets status | Remove from search, show "Notify when back" to buyers |
| OUT_OF_STOCK | ACTIVE | Stock added OR vendor sets status | Re-index, notify waiting buyers |
| ACTIVE | DISABLED | Vendor disables | Hide from search, cancel open quotes |
| PENDING | APPROVED | Admin approves | Email vendor, unlock publishing |
| APPROVED | SUSPENDED | Admin suspends | Freeze all products, notify vendor |

---

# 4. NEXT-BEST-ACTION ENGINE

## Recommendation System Design

The system continuously evaluates the vendor's catalog and generates contextual recommendations.

### Recommendation: Incomplete Listing

| Field | Value |
|-------|-------|
| **Trigger** | Product is ACTIVE but readiness score < 60% |
| **User Context** | Vendor viewing dashboard |
| **Recommended Action** | "Add photos to [Product Name] to increase visibility" |
| **Priority** | Medium |
| **CTA** | "Complete Listing" |
| **Why It Matters** | Incomplete listings get fewer views and quotes |
| **Operational Impact** | Revenue loss from invisible products |
| **Unlocked After** | Higher search ranking, more quote requests |

### Recommendation: Low Stock

| Field | Value |
|-------|-------|
| **Trigger** | `inventory_signal` changes to `LOW_STOCK` |
| **User Context** | Vendor dashboard |
| **Recommended Action** | "Restock [Product Name] — only 5 units left before going out of stock" |
| **Priority** | High |
| **CTA** | "Adjust Inventory" |
| **Why It Matters** | Out-of-stock products are hidden from buyers |
| **Operational Impact** | Lost quote opportunities |
| **Unlocked After** | Product returns to search results |

### Recommendation: Pending Approval

| Field | Value |
|-------|-------|
| **Trigger** | Vendor registered, status = PENDING for > 48h |
| **User Context** | Vendor dashboard |
| **Recommended Action** | "Complete your business verification to speed up approval" |
| **Priority** | High |
| **CTA** | "Complete Verification" |
| **Why It Matters** | Cannot publish or receive quotes until approved |
| **Operational Impact** | Zero revenue potential |

### Recommendation: Unresponded Quote

| Field | Value |
|-------|-------|
| **Trigger** | Quote request received, no response for > 12h |
| **User Context** | Vendor dashboard + email + push |
| **Recommended Action** | "Respond to quote from [Buyer Name] for [Product Name]" |
| **Priority** | Urgent |
| **CTA** | "Respond Now" |
| **Why It Matters** | Buyers typically request 3 quotes and pick the fastest responder |
| **Operational Impact** | Direct revenue loss |

### Recommendation: Price Competitiveness

| Field | Value |
|-------|-------|
| **Trigger** | Product price is > 20% above category median |
| **User Context** | Vendor viewing product detail |
| **Recommended Action** | "Your price is 25% above the category average. Consider a bulk discount to stay competitive." |
| **Priority** | Low |
| **CTA** | "Adjust Pricing" |
| **Why It Matters** | Price is the #1 filter buyers use |
| **Operational Impact** | Fewer quote requests |

### Recommendation: Certification Expiring

| Field | Value |
|-------|-------|
| **Trigger** | ProductCertification `expires_on` is within 30 days |
| **User Context** | Vendor dashboard |
| **Recommended Action** | "Your KEBS certification for [Product Name] expires in 14 days. Renew to maintain compliance." |
| **Priority** | High |
| **CTA** | "Upload Renewal" |
| **Why It Matters** | Expired certifications may disqualify products from government procurement |

### Recommendation: No Featured Products

| Field | Value |
|-------|-------|
| **Trigger** | Vendor has > 5 products, none marked `is_featured` |
| **User Context** | Vendor dashboard |
| **Recommended Action** | "Feature your top-selling product to appear in homepage highlights" |
| **Priority** | Medium |
| **CTA** | "Feature a Product" |

---

# 5. DASHBOARD / WORKSPACE REDESIGN

## From "Admin Card" to "Command Center"

The current `VendorInventorySection` is a card inside an admin dashboard. The new workspace is a ** mission control** for the vendor's catalog operations.

---

## Workspace Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│  WORKSPACE HEADER                                                   │
│  "Good morning, [Vendor]. You have 3 urgent actions today."         │
├─────────────────────────────────────────────────────────────────────┤
│  PRIORITY STRIP (horiz scroll on mobile)                            │
│  [🚨 2 Low Stock] [⏰ 1 Unresponded Quote] [📋 3 Pending Tasks]      │
├──────────────────┬──────────────────────────────────────────────────┤
│  HEALTH SCORE    │  CATALOG PERFORMANCE                              │
│  ┌──────────┐    │  ┌──────────────┐ ┌──────────────┐ ┌──────────┐  │
│  │    78%   │    │  │ 14 Products  │ │ 127 Views    │ │ 8 Quotes │  │
│  │  Good    │    │  │ 12 Active    │ │ This Week    │ │ This Mo  │  │
│  └──────────┘    │  └──────────────┘ └──────────────┘ └──────────┘  │
│  + 3 warnings    │                                                   │
├──────────────────┴──────────────────────────────────────────────────┤
│  WAITING ON YOU                        │  WAITING ON OTHERS           │
│  [Restock Cement] [Respond to Quote]   │  [Admin Approval] [Buyer     │
│  [Upload Cert]                         │   Decision]                  │
├─────────────────────────────────────────────────────────────────────┤
│  CATALOG LIST (not a raw table)                                     │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │ 🔴 Dangote Cement    LOW STOCK    5 left    [Restock] [Edit]   ││
│  │ 🟢 Steel Rebar       HEALTHY      120 left  [Promote] [Edit]   ││
│  │ 🟡 Timber Planks     NO IMAGES    45 left   [Add Photos]      ││
│  └─────────────────────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────────────────────┤
│  QUICK ACTIONS                                                      │
│  [+ Publish Material] [📥 Import CSV] [📊 View Reports]             │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Priority Zones

### Zone 1: Urgent Actions (Top, Always Visible)
- Items requiring action within 24h
- Ordered by revenue impact
- Collapsible but never hidden

### Zone 2: Health Score (Left sidebar on desktop, top on mobile)
- Single score (0-100) for catalog health
- Derived from: stock levels, listing completeness, response times, certification status
- Expandable to show contributing factors

### Zone 3: Performance Metrics (Right of health)
- Key numbers: active products, views, quotes, conversion rate
- Trend indicators (↑ ↓ →)
- Click to drill down

### Zone 4: Catalog List (Main area)
- Not a raw data table
- Each row is an **operational card** showing status, next action, and quick buttons
- Grouped by: Needs Attention, Healthy, Drafts, Disabled
- Default sort: Urgent first, then recently active

### Zone 5: Quick Actions (Sticky bottom on mobile)
- Primary: Publish New Material
- Secondary: Import CSV, Run Report

---

## What Appears When

| Condition | What Appears |
|-----------|-------------|
| First login after approval | "Welcome! Publish your first material" wizard launcher |
| Low stock items exist | Urgent actions strip with "Restock" buttons |
| Unresponded quotes exist | Urgent actions strip with "Respond" buttons |
| All products healthy | "Your catalog is healthy. Consider featuring a product." |
| No products published | Empty state with wizard launcher + CSV import |
| Certifications expiring soon | Warning banner with "Renew Certifications" CTA |

---

# 6. NAVIGATION REDESIGN

## From Module Menu to Goal-Based Navigation

### BAD (Current)
```
Vendor Dashboard
├── My Profile
├── Inventory
│   ├── Add Material
│   ├── Import CSV
│   └── List
├── Orders
├── Quotes
├── Analytics
└── Settings
```

### GOOD (Proposed)
```
Vendor Command Center
├── 🚀 Launch
│   ├── Publish New Material
│   ├── Import Catalog
│   └── Duplicate Existing
├── 📦 Catalog
│   ├── Needs Attention (urgent items)
│   ├── Active Listings
│   ├── Drafts
│   └── Out of Stock
├── 💬 Quotes & Orders
│   ├── Respond to Quotes (unresponded first)
│   ├── Active Orders
│   └── Order History
├── 📊 Performance
│   ├── Views & Engagement
│   ├── Quote Conversion
│   └── Competitive Position
└── ⚙️ Account
    ├── Business Profile
    ├── Certifications
    └── Payout Settings
```

### Mobile Navigation
Bottom tab bar:
```
[📦 Catalog] [🚀 Launch] [💬 Quotes] [📊 Insights] [👤 Account]
```

---

# 7. MULTI-STEP WIZARD DESIGN

## Wizard: Publish New Material

### Step 1: What Are You Selling?
**Purpose:** Capture the core identity of the product.

| Element | Behavior |
|---------|----------|
| **Name** | Auto-complete from common materials in category |
| **Category** | Hierarchical dropdown: Category → Subcategory |
| **Short Description** | 1-sentence pitch. Inline hint: "This appears in search results." |
| **Full Description** | Rich text (lightweight). Inline hint: "Include use cases, benefits, and quality claims." |
| **Validation** | Name + Category + Description required to proceed |
| **Smart Default** | Category pre-selects based on name match |

**After Step 1:** Auto-save as DRAFT. Show "Draft saved" toast.

---

### Step 2: Pricing & Availability
**Purpose:** Set commercial terms.

| Element | Behavior |
|---------|----------|
| **Unit** | Dropdown: bag, ton, piece, meter, kg, litre, etc. |
| **Base Price** | Number input with currency symbol |
| **Bulk Price** | Optional. Only shown if "Offer bulk pricing" toggled on |
| **Bulk Threshold** | Appears when bulk price is entered |
| **Stock Quantity** | Current on-hand quantity |
| **Reorder Level** | Warning threshold. Default: 20% of stock |
| **Min Order** | Default: 1 |
| **Max Order** | Optional. Blank = no limit |
| **Validation** | Price > 0, Stock >= 0, Min <= Max |
| **Smart Default** | Currency from vendor country, Min Order = 1 |

**Inline Education:** "Bulk pricing attracts project buyers who order in large quantities."

---

### Step 3: Specifications
**Purpose:** Technical details for specification matching.

| Element | Behavior |
|---------|----------|
| **Brand** | Free text with auto-suggest from existing brands |
| **Model / SKU** | Free text |
| **Weight** | Number + unit (kg default) |
| **Dimensions** | L × W × H with unit selector |
| **Color** | Color picker OR text |
| **Material Composition** | Textarea |
| **Quality Grade** | Dropdown: Standard, Grade A, Premium, Industrial |
| **Lead Time** | Days to delivery |
| **Delivery Regions** | Multi-select chips: NAIROBI, MOMBASA, etc. |

**All fields optional.** Progress bar still advances.

---

### Step 4: Compliance
**Purpose:** Build trust through certifications.

| Element | Behavior |
|---------|----------|
| **Certification Registry** | Searchable dropdown: KEBS, ISO 9001, CE, ASTM, etc. |
| **Certification Number** | Free text |
| **Issuing Body** | Auto-filled from registry, editable |
| **Issue Date** | Date picker |
| **Expiry Date** | Date picker. System warns when < 30 days |
| **Add Another** | Button to add more certs |

**Smart Behavior:** If vendor selects "Cement" category, suggest "KEBS Certified" and "ISO 9001" as common certifications.

---

### Step 5: Documents & Media
**Purpose:** Upload proof and photos.

| Element | Behavior |
|---------|----------|
| **Photos** | Drag-drop zone. Show thumbnails. Require 1, recommend 3+. Auto-validate file size < 5MB |
| **Primary Photo** | Star toggle on first uploaded image |
| **Documents** | Drag-drop for PDFs. Label each: Datasheet, Safety Sheet, Warranty, etc. |
| **Document Visibility** | Public (buyers see) vs Internal (vendor only) |

**Validation Warning:** "You can publish without photos, but listings with images get 5× more views."

---

### Step 6: Review & Publish
**Purpose:** Final check before going live.

| Element | Behavior |
|---------|----------|
| **Buyer Preview** | Render the product card EXACTLY as buyers will see it |
| **Readiness Score** | 0-100% based on completeness |
| **Checklist** | ✅ Required fields, ⚠️ Warnings (no images, no certs), ✅ Ready |
| **Marketing Flags** | Toggle: Featured, New Arrival, On Sale |
| **Main CTA** | "Publish to Marketplace" (enabled if readiness > 50%) |
| **Secondary** | "Save as Draft" (always available) |

**After Publish:** Confetti animation + "Your material is live!" + "What happens next" explainer.

---

## Wizard: Import Catalog via CSV

### Step 1: Download Template
- Show template with example rows
- Explain each column
- CTA: "Download CSV Template"

### Step 2: Upload & Validate
- Drag-drop CSV
- **Instant preview:** Show first 5 rows parsed
- **Validation report:** Row-by-row errors BEFORE importing
- CTA: "Fix Errors in Spreadsheet" OR "Proceed with Import"

### Step 3: Import & Review
- Progress bar during import
- Summary: "Created 45 products, 3 errors"
- List of errors with row numbers
- CTA: "View Imported Products" OR "Download Error Report"

---

# 8. TIMELINE & ACTIVITY UX

## Operational Timeline for Each Product

Every product gets a visible timeline showing its operational journey.

```
Product: Dangote Cement 50kg

Timeline:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 May 10   📝 Draft Created
📅 May 10   ✅ Published to Marketplace
📅 May 12   📸 Photos Uploaded (3 images)
📅 May 14   📥 Quote Request from ABC Construction (10 bags)
📅 May 14   💬 Quote Responded (price confirmed)
📅 May 15   📦 Order Placed by ABC Construction
📅 May 16   🚚 Dispatched
📅 May 17   ⭐ Delivered
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Upcoming:
⚠️ May 25   KEBS Certification Expires
```

## Timeline Event Types

| Icon | Event Type | Actor | Visibility |
|------|-----------|-------|------------|
| 📝 | Created | Vendor | Vendor only |
| ✅ | Published | Vendor | Public |
| 📸 | Media Added | Vendor | Public |
| 📥 | Quote Requested | Buyer | Vendor |
| 💬 | Quote Responded | Vendor | Buyer |
| 📦 | Order Placed | Buyer | Both |
| 🚚 | Dispatched | Vendor | Buyer |
| ⭐ | Delivered | Buyer / Vendor | Both |
| ⚠️ | Stock Low | System | Vendor |
| 🛑 | Out of Stock | System | Vendor (public: hidden) |
| 📋 | Cert Expiring | System | Vendor |
| 🔄 | Price Changed | Vendor | Public (if active) |

---

# 9. EMPTY STATES & GUIDED STATES

## Empty State: No Products Published

**Current:** Blank table or "No products found"

**Proposed:**
```
┌─────────────────────────────────────────┐
│                                         │
│         🏗️  Your Catalog is Empty       │
│                                         │
│   Start selling construction materials  │
│   to project owners across the region.  │
│                                         │
│   [🚀 Publish First Material]           │
│   [📥 Import from CSV]                  │
│                                         │
│   ⏱️ Setup time: ~5 minutes per product │
│                                         │
│   💡 Tip: Products with photos and      │
│      certifications get 5× more quotes. │
│                                         │
└─────────────────────────────────────────┘
```

## Empty State: No Quotes Received

```
┌─────────────────────────────────────────┐
│                                         │
│         📭 No Quotes Yet                │
│                                         │
│   Buyers are browsing. Here's how to    │
│   increase your chances:                │
│                                         │
│   1. Add photos to your materials       │
│   2. Set competitive bulk pricing       │
│   3. Enable delivery to more regions    │
│                                         │
│   [Improve My Listings]                 │
│                                         │
└─────────────────────────────────────────┘
```

## Empty State: No Certifications

```
┌─────────────────────────────────────────┐
│                                         │
│         📋 No Certifications Added      │
│                                         │
│   Government and enterprise buyers      │
│   filter by certification.              │
│                                         │
│   Common for your category:             │
│   • KEBS Certified                      │
│   • ISO 9001:2015                       │
│   • CE Mark                             │
│                                         │
│   [Add Certifications]                  │
│                                         │
└─────────────────────────────────────────┘
```

---

# 10. BLOCKING & VALIDATION UX

## Blocker: Vendor Not Approved

**Current:** Generic 403 or hidden button

**Proposed:**
```
┌─────────────────────────────────────────┐
│  ⏳ Waiting for Approval                │
│                                         │
│  Your vendor profile is under review.   │
│  Typical approval time: 1-2 business    │
│  days.                                  │
│                                         │
│  While you wait:                        │
│  [📥 Prepare Catalog CSV]               │
│  [📋 Review Requirements]               │
│                                         │
│  You'll be notified via email and       │
│  dashboard when approved.               │
│                                         │
└─────────────────────────────────────────┘
```

## Blocker: Product Missing Required Fields

**Current:** Generic "Failed to save material record"

**Proposed:** Inline field-level errors with recovery path:
```
⚠️ Cannot publish yet. Please fix:
• Name: Required — What buyers will search for
• Base Price: Required — Set to 0 if price is on request
• Category: Required — Helps buyers find your product

[Go to Commercial Setup]
```

## Blocker: Out of Stock

**Current:** Product hidden from buyers silently

**Proposed:** Vendor sees:
```
🔴 Dangote Cement is OUT OF STOCK

Buyers cannot see or quote this product.

[Restock Now] — Add inventory to reactivate
[Keep Hidden] — Leave as out of stock
```

Buyer sees (if they had it saved/bookmarked):
```
⚠️ This material is temporarily out of stock.

[🔔 Notify Me When Available]
[🔍 Find Similar Materials]
```

## Blocker: Certification Expired

```
⚠️ KEBS Certification for Dangote Cement expired on May 15, 2026.

This product may be filtered out of government procurement searches.

[Upload Renewal] [Mark as Pending Renewal]
```

---

# 11. ACTION HIERARCHY DESIGN

## Visual Dominance Rules

| Action Type | Visual Treatment | Location | Confirmation |
|-------------|-----------------|----------|--------------|
| **Primary** | Solid earth-orange button, full width on mobile | Top right of workspace, bottom sticky on mobile | None for save, modal for publish |
| **Secondary** | Outline button | Next to primary | None |
| **Tertiary** | Ghost/text link | Inside cards, dropdowns | None |
| **Destructive** | Red text, requires explicit confirmation | Inside "More actions" menu | "Type DELETE to confirm" |
| **Rare** | Hidden in "More actions" (⋯) menu | Dropdown only | Context-dependent |

## Action Map: Vendor Catalog Workspace

```
Product Card:
┌─────────────────────────────────────────┐
│ Dangote Cement 50kg              [⋯]   │
│ ⚠️ LOW STOCK — 5 units left             │
│                                         │
│ [Restock] ← Primary (urgent)            │
│ [Edit] ← Secondary                      │
│ [Preview] ← Tertiary                    │
│                                         │
│ ⋯ More Actions:                         │
│   Duplicate                             │
│   Disable                               │
│   Delete (requires confirmation)        │
└─────────────────────────────────────────┘
```

## Hidden by Default
- Export single product
- View raw API data
- Advanced SEO settings
- Inventory movement history (expandable)

---

# 12. HUMAN LANGUAGE REWRITE

## Status Messages

| System Language | Human Language |
|-----------------|----------------|
| `status: ACTIVE` | ✅ Live on marketplace |
| `status: DRAFT` | 📝 Saved, not visible to buyers |
| `status: OUT_OF_STOCK` | 🔴 Hidden — restock to reactivate |
| `status: DISABLED` | 🚫 Paused by vendor |
| `inventory_signal: LOW_STOCK` | ⚠️ Running low — 5 left |
| `inventory_signal: IN_STOCK` | ✅ Available |
| `verified_status: PENDING` | ⏳ Under review |
| `verified_status: APPROVED` | ✅ Verified supplier |

## Empty State Messages

| System Language | Human Language |
|-----------------|----------------|
| "No data" | "Your catalog is empty. Let's publish your first material." |
| "404 Not Found" | "This material is no longer available. Here are similar options." |
| "ValidationError" | "We need a bit more info before this can go live." |

## Error Messages

| System Language | Human Language |
|-----------------|----------------|
| "User has no vendor profile" | "Complete your vendor registration to start selling." |
| "Vendor is not approved" | "Your account is pending approval. You'll be notified within 1-2 business days." |
| "Failed to save material record" | "We couldn't save your product. Check the highlighted fields above." |
| "Only vendors can import products" | "Complete vendor verification to use bulk import." |

## Success Messages

| System Language | Human Language |
|-----------------|----------------|
| "Product created" | "Your material is live! Buyers can now find and request quotes." |
| "Inventory updated" | "Stock updated. Your listing is back in search results." |
| "Quote request sent" | "Quote sent! You'll receive a response from the vendor within 24 hours." |

---

# 13. INTELLIGENT NOTIFICATIONS

## Notification Design System

Every notification must answer: **What happened? Why does it matter? What should I do?**

### Notification: Stock Low

| Field | Value |
|-------|-------|
| **Trigger** | `inventory_signal` changes to `LOW_STOCK` |
| **Recipient** | Vendor |
| **Priority** | High |
| **Channel** | Dashboard banner + email |
| **Title** | "Dangote Cement is running low" |
| **Body** | "You have 5 bags left. At current quote volume, you'll be out of stock in ~2 days." |
| **CTA** | "Restock Now" |
| **Deep Link** | `/vendor/dashboard?action=restock&product={uuid}` |

### Notification: New Quote Request

| Field | Value |
|-------|-------|
| **Trigger** | Buyer submits quote request |
| **Recipient** | Vendor |
| **Priority** | Urgent |
| **Channel** | Dashboard + email + push (if enabled) |
| **Title** | "New quote request: 50 bags of Dangote Cement" |
| **Body** | "ABC Construction needs a quote by May 20. You respond in 4 hours on average." |
| **CTA** | "Review & Respond" |
| **Deep Link** | `/vendor/quotes/{quote_id}` |

### Notification: Approval Granted

| Field | Value |
|-------|-------|
| **Trigger** | Admin approves vendor |
| **Recipient** | Vendor |
| **Priority** | High |
| **Channel** | Dashboard + email |
| **Title** | "You're approved! Start selling today." |
| **Body** | "Your vendor account is verified. You can now publish materials and receive quotes." |
| **CTA** | "Publish First Material" |
| **Deep Link** | `/vendor/dashboard?action=first_publish` |

### Notification: Certification Expiring Soon

| Field | Value |
|-------|-------|
| **Trigger** | Certification expires in ≤ 30 days |
| **Recipient** | Vendor |
| **Priority** | Medium |
| **Channel** | Dashboard + weekly digest email |
| **Title** | "KEBS Certification expires in 14 days" |
| **Body** | "Renew to keep your cement products visible in government procurement searches." |
| **CTA** | "Upload Renewal" |

---

# 14. OPERATIONAL HEALTH SYSTEM

## Catalog Health Score

**Score: 0-100** displayed prominently on vendor dashboard.

### Scoring Factors

| Factor | Weight | How Calculated |
|--------|--------|----------------|
| Listing Completeness | 25% | % of products with images + description + specs |
| Stock Health | 25% | % of active products with healthy stock levels |
| Response Performance | 20% | Average quote response time (target: < 4h) |
| Certification Status | 15% | % of products with valid certifications |
| Catalog Freshness | 15% | Last update date across products |

### Thresholds

| Score | Label | Action |
|-------|-------|--------|
| 90-100 | Excellent | Feature on homepage, badge on profile |
| 70-89 | Good | Minor improvements suggested |
| 50-69 | Needs Attention | Specific blockers highlighted |
| 0-49 | At Risk | Products may be hidden, urgent action required |

### Visual Indicator

```
Health Score: 78 — Good
[████████████░░░░░░░░] 78%

Contributing Factors:
✅ Listing Completeness  92%
⚠️ Stock Health          65%  ← 2 products low stock
✅ Response Performance   95%
⚠️ Certification Status   70%  ← 1 cert expiring soon
✅ Catalog Freshness      88%
```

---

# 15. AI-ASSISTED UX OPPORTUNITIES

## Practical Workflow Intelligence (No Hype)

### 1. Smart Category Suggestion
**What:** When vendor types "Portland cement 50kg", auto-suggest "Cement > Portland Cement"
**Implementation:** Simple text matching against category names + synonyms.

### 2. Price Anomaly Detection
**What:** Flag if vendor's price is > 2× category median OR < 50% of median.
**Message:** "Your price is significantly above the category average. Buyers may filter you out. Consider reviewing."
**Implementation:** Pre-aggregated category price stats, updated nightly.

### 3. Stock-Out Prediction
**What:** "Based on your quote volume, you'll run out of Dangote Cement in ~3 days."
**Implementation:** Simple linear projection from quote request rate vs. current stock.

### 4. Certification Gap Detection
**What:** For "Cement" category, suggest "KEBS Certified" if not present.
**Implementation:** Category → common certification mapping table.

### 5. Duplicate Detection
**What:** "You already have 'Dangote Cement 50kg'. Are you sure you want to publish another?"
**Implementation:** Fuzzy string match on product name + brand within vendor's catalog.

### 6. Delivery Region Suggestion
**What:** Suggest regions based on vendor's location + historical order data.
**Implementation:** "You're in Nairobi. Most of your orders come from Nairobi and Kiambu."

### 7. Photo Quality Check
**What:** Warn if uploaded image is < 500px, blurry, or not product-related.
**Implementation:** Basic image dimension check (frontend). ML-based quality check (future).

---

# 16. MOBILE EXPERIENCE REDESIGN

## Mobile-First Priorities

### Quick Actions (Bottom Sheet)
Swipe up from bottom:
```
[📷 Scan Product] [➕ Quick Add] [📊 Stock Check]
```

### Product Card (Swipe Actions)
Swipe left on product: [Edit] [Restock]
Swipe right: [Disable] [Delete]

### Photo Capture
- Camera opens directly from "Add Photo"
- Auto-crop to square
- Auto-compress for upload
- Immediate thumbnail preview

### Field Operations Mode
For vendors managing warehouse inventory:
- Large buttons (thumb-sized)
- High contrast for outdoor/sunlight viewing
- Offline queue: stock adjustments saved locally, synced when online
- Barcode/QR scanner integration for SKU entry

### Quote Response (One-Tap)
```
New Quote Request!
50 bags × Dangote Cement

[✅ Accept at Listed Price]  [💬 Counter Offer]  [❌ Decline]
```

---

# 17. ACCESSIBILITY & INCLUSIVITY

## WCAG 2.1 AA Compliance

| Requirement | Implementation |
|-------------|----------------|
| **Color Independence** | Status icons (🟢🟡🔴) always paired with text labels. Never rely on color alone. |
| **Keyboard Navigation** | All wizards navigable via Tab/Enter/Arrow keys. Escape closes modals. |
| **Screen Reader** | All form fields have associated labels. Live regions for dynamic updates ("Stock updated"). |
| **Focus Management** | Focus trapped in modals. Returns to trigger on close. |
| **Contrast** | All text meets 4.5:1 ratio. Interactive elements 3:1. |

## Low Literacy UX
- Use icons + text for all actions (never text-only buttons for critical actions)
- Sentence case, not title case
- Avoid jargon: "Publish" not "Commit to catalog index"
- Progressive disclosure: simple mode by default, advanced mode toggle

## Multilingual UX
- All user-facing strings in translation files
- Number formatting (currency, dates) localized
- Right-to-left layout support for Arabic

## Low Bandwidth UX
- Images lazy-loaded, WebP format
- CSV import works offline (queue for sync)
- Dashboard loads core metrics first, charts deferred
- Skeleton screens instead of spinners

---

# 18. PROGRESSIVE DISCLOSURE MODEL

## Beginner Experience (First 3 sessions)

**What's Visible:**
- Step-by-step wizard for first product
- Inline tooltips on every field
- "Why this matters" explanations
- Simplified dashboard: only Catalog + Quotes
- Checklist: "Complete your setup" (5 tasks)

**What's Hidden:**
- Advanced filters
- Bulk operations
- Analytics/Reports
- CSV import (until 3rd product)
- Marketing flags (until approved)

## Intermediate Experience (After 5+ products published)

**What's Unlocked:**
- CSV import
- Bulk edit
- Featured/New Arrival flags
- Analytics dashboard
- Competitive pricing insights

## Advanced Experience (After 20+ products + 10+ orders)

**What's Unlocked:**
- API access
- Advanced inventory rules (auto-reorder thresholds)
- Custom delivery zones
- Team member access
- Webhook notifications

---

# 19. CROSS-MODULE INTELLIGENCE

## Integration Map

### Catalog ↔ Projects
| Trigger | Suggested Action | Automation |
|---------|-----------------|------------|
| Project owner creates BOM (Bill of Materials) | "Find suppliers for these 8 materials" | Auto-search catalog for matching specs |
| Product price changes | Notify project owners who have quoted | Optional: auto-update open quotes |

### Catalog ↔ Contracts
| Trigger | Suggested Action | Automation |
|---------|-----------------|------------|
| Quote accepted | "Generate supply agreement from template" | Pre-fill contract with product + price + qty |
| Contract signed | Auto-create order + reserve stock | Stock reservation system |

### Catalog ↔ Escrow
| Trigger | Suggested Action | Automation |
|---------|-----------------|------------|
| Order placed | "Buyer has funded escrow. Prepare shipment." | Notify vendor when escrow is funded |
| Delivery confirmed | "Release payment from escrow" | Auto-release after buyer confirmation |

### Catalog ↔ Delivery/Logistics
| Trigger | Suggested Action | Automation |
|---------|-----------------|------------|
| Order confirmed | "Schedule delivery to [project site]" | Route optimization suggestion |
| Delivery delayed | "Notify buyer of delay, offer alternative" | Auto-escalation if delay > 24h |

### Catalog ↔ Disputes
| Trigger | Suggested Action | Automation |
|---------|-----------------|------------|
| Buyer reports wrong material | "Review delivery photos vs. product specs" | Flag for admin review if pattern emerges |
| Quality complaint | "Check certification validity + batch records" | Auto-suspend product if 3+ complaints |

### Catalog ↔ Finance
| Trigger | Suggested Action | Automation |
|---------|-----------------|------------|
| Monthly close | "Your top 5 products generated 80% of revenue" | Auto-generate vendor payout report |
| Tax season | "Export transaction history for [period]" | Generate tax-ready CSV |

### Catalog ↔ Property
| Trigger | Suggested Action | Automation |
|---------|-----------------|------------|
| Property listing created | "Materials needed for this renovation: [auto-generated BOM]" | Cross-sell relevant materials |

---

# 20. FINAL UX TRANSFORMATION SUMMARY

## Current UX Problems

1. **Form-first, not goal-first.** Voters see tabs and fields, not a launch workflow.
2. **No operational awareness.** The system doesn't tell vendors what's wrong, what's urgent, or what to do next.
3. **Silent failures.** Products can be incomplete, out of stock, or invisible — and the vendor doesn't know.
4. **No buyer guidance.** Buyers see a dense catalog with no sense of what to prioritize or trust.
5. **Disconnected workflows.** Publishing, quoting, ordering, and delivery feel like separate systems.
6. **CRUD mentality.** Everything behaves like a database admin panel, not an operational tool.

## Proposed UX Transformation

| From | To |
|------|-----|
| Form tabs | Step-by-step wizard with progress |
| "Save" button | "Publish with Readiness Check" |
| Raw product table | Operational cards with next-best-action |
| Silent stock changes | Proactive low-stock alerts with restock CTA |
| Generic errors | Contextual recovery guidance |
| Passive catalog | Active marketplace assistant |
| Feature hunting | Goal-based navigation |
| Empty tables | Guided empty states with CTAs |
| Static product page | Buyer decision-support with comparison |
| Isolated module | Cross-module workflow continuity |

## Operational Benefits

- **Faster time-to-first-sale:** Guided wizard reduces vendor onboarding from hours to minutes
- **Higher catalog quality:** Readiness score drives completeness, reducing buyer friction
- **Fewer stock-outs:** Proactive alerts prevent lost revenue
- **Faster quote responses:** Prioritized quote notifications increase win rate
- **Lower support burden:** Contextual guidance replaces documentation and training

## User Psychology Improvements

- **Confidence:** Vendors know exactly what's needed to succeed
- **Control:** Clear status + next steps reduce anxiety
- **Progress:** Step-by-step flow creates momentum and completion satisfaction
- **Recognition:** Health score + performance metrics provide positive feedback loops

## Cognitive Load Reductions

- **Decision fatigue eliminated:** Next-best-action engine tells users what to do
- **Information overload reduced:** Progressive disclosure hides advanced features
- **Error recovery simplified:** Every blocker includes "how to fix it" guidance
- **Context switching minimized:** Workspace surfaces everything needed for daily operations

## Workflow Efficiency Gains

- **Vendor:** Publish → Monitor → Restock → Respond in a single workspace
- **Buyer:** Search → Compare → Quote → Track in a guided flow
- **Admin:** Review → Approve → Monitor → Escalate with full visibility

## Adoption Improvements

- **Zero training required:** The system teaches through inline guidance
- **Zero documentation required:** Every empty state, error, and blocker includes explanation + CTA
- **Immediate value:** First-time vendors publish a product in < 5 minutes
- **Continuous engagement:** Health score + notifications keep vendors active

---

## Closing Principle

> The vendor should never ask: "What do I do now?"  
> The buyer should never ask: "Can I trust this supplier?"  
> The admin should never ask: "What's going wrong?"  
>
> The system should answer before they ask.

---

*End of UX Transformation Blueprint*
