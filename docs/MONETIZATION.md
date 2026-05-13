# MONETIZATION.md

## Monetization Strategy

This document defines how the platform is expected to generate revenue as it matures.

The monetization model should be read as a phased stack:

1. marketplace transaction revenue
2. execution and service revenue
3. financial infrastructure revenue
4. project and property visibility revenue
5. enterprise and government revenue
6. institutional infrastructure revenue

The model is intentionally layered. Later revenue streams depend on earlier operational trust, liquidity, and data depth.

---

## 1. Revenue Principles

- Charge for value created, not for idle access.
- Keep marketplace fees separate from regulated finance revenue.
- Distinguish platform revenue from pass-through costs.
- Treat regulated investment flows as compliance-sensitive and separate from general SaaS or marketplace fees.
- Make the fee trigger visible to the user at the point of action.

---

## 2. Phase-to-Revenue Map

| Phase | Revenue Source | Trigger |
|---|---|---|
| Phase 1 | Materials transaction commissions | Successful material order or quote-to-order conversion |
| Phase 2 | Contractor bidding and service marketplace fees | Tender posting, bid visibility, award, or service execution |
| Phase 3 | Escrow fees and financing spreads | Escrow setup, milestone release, finance approval, or disbursement |
| Phase 4 | Project listing fees, premium visibility, property lead generation | Project promotion, boosted placement, premium listing exposure, lead capture |
| Phase 5 | Enterprise subscriptions and government procurement contracts | Account subscription, enterprise seats, procurement access, compliance tooling |
| Phase 6 | Institutional settlement and compliance infrastructure fees | High-volume settlement, reporting, integration, or regulated infrastructure usage |

---

## 3. Pricing Surfaces

### 3.1 Marketplace Fees

- Material transaction commission
- Contractor service fee
- Listing boost fee
- Featured placement fee
- Lead routing or lead capture fee where applicable

### 3.2 Financial Fees

- Financing origination fee
- Financing spread
- Escrow administration fee
- Milestone release or settlement fee
- Credit line management fee

### 3.3 Platform and Enterprise Fees

- Subscription fee
- Seat-based enterprise fee
- Compliance module fee
- Government procurement contract fee
- Integration or API access fee for large accounts

---

## 4. Revenue Ownership

The docs should keep these buckets separate:

- Platform revenue: fees retained by the marketplace operator
- Partner revenue: finance, payments, or compliance partner fees where the platform is acting as a channel
- Pass-through costs: taxes, gateway charges, statutory fees, and disbursement costs
- Regulated flows: investment contributions and settlement activity that must remain compliance-aware

This separation matters because the same user action can produce different accounting treatment depending on whether it is a marketplace order, a financing event, or a regulated investment event.

---

## 5. Unit Economics To Track

The docs should define these metrics even before exact numbers are final:

- gross merchandise value
- take rate
- average order value
- average contract value
- average project value
- financing conversion rate
- financing margin
- escrow throughput
- lead-to-project conversion rate
- project-to-contract conversion rate
- contract award rate
- enterprise renewal rate

These metrics should appear in analytics and investor reporting once the platform matures.

---

## 6. User-Facing Monetization Story

The customer-facing rationale should stay simple:

- buyers pay for access to better procurement outcomes
- contractors pay for pipeline, credibility, and execution tooling
- project owners pay for visibility, trust, and operational control
- property owners pay for exposure, inquiries, and qualified leads
- investors pay through capital deployment workflows and compliance-enabled access
- enterprises pay for scale, governance, and integrations

If a fee cannot be explained in one sentence from the user’s perspective, it should not be promoted prominently in the UI.

---

## 7. Phase Gating

Do not imply later-stage monetization before the supporting product exists.

- Phase 1 should not imply enterprise subscriptions.
- Phase 2 should not imply regulated investment revenue.
- Phase 3 should not imply full investment-marketplace monetization.
- Phase 4 should not imply regulated securities activity.
- Phase 5 should not imply institutional settlement rails are already live.

The docs should always make it clear which revenue streams are live, which are planned, and which are only strategic targets.

---

## 8. Compliance Note

Any revenue derived from financing, escrow, or investment-linked activity must be documented with care.

The docs should distinguish:

- fees charged by the platform
- spreads or margins charged by a finance product
- capital contributions from investors
- regulated securities or settlement activity

This prevents the product and compliance docs from blurring operational platform revenue with regulated financial activity.

