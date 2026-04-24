# Page Priorities

## Purpose

This file defines the recommended order for visual refinement work.

## Tier 1: Highest visual leverage

These pages shape the user’s impression of the whole product and should be refined first.

- `frontend/src/App.vue`
- `frontend/src/views/ProductList.vue`
- `frontend/src/views/ProductDetail.vue`
- `frontend/src/views/Login.vue`
- `frontend/src/views/Register.vue`

Why:

- they define first impression
- they expose the brand most often
- improvements here cascade across the whole app

## Tier 2: Core operational dashboards

- `frontend/src/views/BuyerDashboard.vue`
- `frontend/src/views/VendorDashboard.vue`
- `frontend/src/views/ContractorDashboard.vue`
- `frontend/src/views/AdminDashboard.vue`
- `frontend/src/views/OwnerDashboard.vue`

Why:

- these are where long-term usage quality matters most
- they should feel like one coherent platform, not five unrelated apps

## Tier 3: Marketplace and transaction workflows

- `frontend/src/views/ContractList.vue`
- `frontend/src/views/ContractDetail.vue`
- `frontend/src/views/ViewTenders.vue`
- `frontend/src/views/ProjectList.vue`
- `frontend/src/views/ProjectDetail.vue`
- `frontend/src/views/PropertyListing.vue`
- `frontend/src/views/SecondaryMarket.vue`

Why:

- these are high-value decision pages
- they combine discovery, trust, and action

## Tier 4: Specialist operational surfaces

- courier screens
- vendor inventory and orders
- logistics tracking and calculator
- security and verification sections
- system config sections

Why:

- these matter, but benefit most after the higher-level shells are stable

## Recommended redesign order

1. global shell
2. public marketplace
3. auth experience
4. dashboard system
5. workflow-heavy detail pages
6. specialist tools

## What success looks like

After refinement:

- the app feels like one platform
- public and private areas share the same brand DNA
- dashboards feel precise and premium
- forms and tables no longer feel visually secondary to hero sections
- the brand is visible without becoming theatrical
