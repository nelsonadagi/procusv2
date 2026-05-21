# Buyer Discovery, Shortlist, Quote Request, and Order Workflow -- Workflow-First UX Transformation

**Module:** Buyer / Public Discovery Workspace  
**Date:** 2026-05-17  
**Status:** Design Blueprint -- Ready for Review

---

# 1. MODULE EXPERIENCE VISION

## What the User Is Trying to Accomplish

A buyer is not browsing for entertainment. They are trying to **find the right opportunity, compare it quickly, and move it forward** through inquiry, quote, order, or booking.

The module should make it obvious what is happening, what is blocked, and what the next action is.

## Emotional / Operational State

| Actor | Emotional State | Operational State |
|---|---|---|
| **Guest Buyer** | Curious, cautious, not yet committed | Exploring opportunities without a saved profile |
| **Logged-In Buyer** | Goal-driven, comparing options | Wants shortlist, quote requests, and order progress |
| **High-Intent Buyer** | Time-constrained, urgent | Needs fast contact, fast quote, and fast confirmation |

## What Makes the Current UX Difficult

1. Search can return results without saying what to do next.
2. Listings can be hard to compare quickly.
3. The shortlist, inquiry, and quote path can feel disconnected.
4. Users may not know whether they should book, contact, or order.
5. Empty states often explain instead of directing.

## What the Ideal Workflow Should Feel Like

> "The system shows me the best next step and carries me from discovery to action without making me think through the workflow myself."

The buyer workspace should behave like a **decision assistant**:
- it recommends what to compare
- it saves what matters
- it shows the blocked step
- it pushes the user toward the next valid action

---

# 2. USER GOALS

## Buyer

### Primary Goals
1. Find relevant items fast
2. Compare options
3. Request quotes or contact sellers
4. Place an order or move into the next workflow

### Secondary Goals
5. Save favorites
6. Track quote status
7. Revisit previous searches

### Urgent Goals
8. Recover from no-results searches
9. Respond to a pending quote decision
10. Finish checkout or order confirmation

### Recurring Operational Goals
11. Reopen saved searches
12. Review quote responses
13. Monitor delivery or fulfillment status

---

# 3. WORKFLOW-FIRST UX REDESIGN

## Core Workflow

```text
[Search]
  -> [Browse]
    -> [Compare]
      -> [Shortlist]
        -> [Request Quote]
          -> [Review Response]
            -> [Place Order]
              -> [Track Fulfillment]
```

## Lifecycle Table

| Stage | What User Sees | Main CTA | Secondary Actions | Blockers | Guidance |
|---|---|---|---|---|---|
| Search | Query bar and filters | Search Again | Clear filters | no match | suggest broader search |
| Browse | Results cards | Open Item | Compare, shortlist | missing data | show trust signals |
| Compare | Side-by-side summary | Shortlist Choice | Remove item | incomplete specs | explain the difference |
| Quote | Quote request form | Request Quote | Save draft | missing quantity or contact | explain what happens next |
| Response | Seller reply and timeline | Accept Quote | Ask follow-up | pending seller response | show expected wait time |
| Order | Order summary | Confirm Order | Edit details | payment pending | explain fulfillment trigger |
| Track | Status timeline | View Status | Contact support | delayed fulfillment | show recovery path |

---

# 4. NEXT-BEST-ACTION ENGINE

## Examples

| Trigger | Message | Severity | CTA | Destination Page | Escalation Rules |
|---|---|---|---|---|---|
| No shortlist items | "Save items you want to compare later." | Low | Save shortlist | Search results | remind on return |
| Quote pending | "Your quote is waiting on a response." | Medium | View quote | Quote detail | escalate after SLA |
| Order payment incomplete | "Order cannot move until payment is complete." | High | Complete payment | Checkout | notify after delay |
| Delivery delayed | "Your order is delayed and needs review." | High | Track delivery | Order detail | escalate to support |

---

# 5. DASHBOARD / WORKSPACE REDESIGN

## Workspace Layout

- top: search and compare state
- first body zone: urgent actions
- second body zone: shortlist and recent quotes
- third body zone: activity timeline

## Empty States

- no shortlist
- no recent searches
- no quote responses

---

# 6. NOTIFICATION & ESCALATION SYSTEM

- in-app: quote response, order update, delivery update
- email: quote sent, order confirmed, delayed delivery
- SMS / push: urgent quote response, fulfillment delay

---

# 7. FINAL UX TRANSFORMATION SUMMARY

The buyer module should reduce decision friction, not add more browsing noise. The UI should always point to the next valid action: compare, shortlist, request, confirm, or track.
