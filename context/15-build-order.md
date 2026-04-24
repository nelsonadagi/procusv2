# Build Order

## Purpose

This is the recommended execution order for stabilizing and completing the system without increasing drift.

## Guiding principle

Do not expand the platform breadth before stabilizing the platform spine.

## Recommended order

### 1. Environment and execution truth

Goals:

- make backend run consistently
- make tests executable in a real environment
- confirm Docker, PostGIS, Redis, Celery, and Channels assumptions

Why first:

- every later implementation step depends on reproducible runtime behavior

### 2. API alignment and route cleanup

Goals:

- reconcile frontend API calls with backend routes
- remove stale namespaces
- document the intended versioning strategy

Why second:

- otherwise every new feature risks being wired against the wrong contract

### 3. Authentication, roles, and permission validation

Goals:

- confirm actual auth approach
- validate role names and group syncing
- validate admin, vendor, contractor, buyer, owner, and courier flows

Why third:

- authorization mistakes compound quickly across all workflows

### 4. Marketplace core stabilization

Modules:

- accounts
- vendors
- catalog
- orders
- reviews
- taxonomy
- platform_settings

Goals:

- stabilize browse, quote, checkout, order, fulfillment, and review workflows

### 5. Contract execution stabilization

Modules:

- contractors
- contracts
- bids
- milestones

Goals:

- stabilize tender posting, bid handling, award, and milestone flows

### 6. Financial control stabilization

Modules:

- escrow
- disputes
- finance
- scoring

Goals:

- ensure funds, holds, release conditions, and finance flows are safe and testable

### 7. Project and capital stabilization

Modules:

- projects
- property
- investments

Goals:

- ensure projects, commitments, and capital workflows align with contracts and finance

### 8. Operational support systems

Modules:

- logistics
- notifications
- chat
- security

Goals:

- stabilize support systems once the core business flows are dependable

### 9. Advanced regulated and intelligence modules

Modules:

- compliance
- government
- regulation
- enterprise
- banking
- reporting
- risk
- ai_engine
- liquidity
- integrations

Goals:

- complete and verify advanced features after the platform backbone is trustworthy

## Implementation mode recommendation

For each stage:

1. audit current routes and tests
2. fix mismatches
3. verify workflow end-to-end
4. then add new capability

## What not to do

- do not add new dashboards before API alignment
- do not add new finance behavior before permission and workflow validation
- do not trust phase docs as endpoint truth without code verification
