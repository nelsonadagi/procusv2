# Workflows

## Marketplace workflow

Primary flow:

1. base user registers as `PROJECT_OWNER`
2. user discovers products and requests quotes as part of the base procurement flow
3. if the user wants to sell, they activate vendor onboarding
4. vendor profile is reviewed and approved by admin
5. approved vendor creates or imports products in vendor-scoped inventory
6. vendors enrich products with certifications, technical attributes, documents, reorder thresholds, and stock state
7. vendors adjust on-hand stock through the inventory workspace and can review product movement history
8. buyer filters by category, region, certification, and availability before requesting quotes or placing orders
9. buyer selects one of the active payment methods configured by admin and checkout validates stock and records an inventory commit
10. payment is simulated or processed through the selected gateway and the payment record updates
11. vendor confirms with an estimated delivery date
12. cancellation of eligible orders restores stock, then fulfillment, delivery, review, or dispute follows

## Contracting workflow

1. base user or owner posts contract or tender
2. if a user wants to bid, they activate contractor onboarding
3. contractor profile is reviewed and approved by admin
4. approved contractors discover and submit bids
5. owner reviews, shortlists, and awards
6. execution begins
7. milestones are defined and approved
8. payment or escrow release is triggered

## Escrow and dispute workflow

1. funds are associated with a contract or payment event
2. milestones trigger release candidates
3. disputes can freeze or hold funds
4. operator or policy logic determines release or refund path
5. payment operations use the same configurable gateway catalog exposed in platform settings

## Project and capital workflow

1. owner creates project
2. project requirements are added
3. contracts can be linked to projects
4. updates are posted
5. investors pledge commitments
6. financing applications can target either the project or a related property
7. owners, investors, and approved operators can submit and review finance applications in the finance workspace
8. approved financing can support project execution, property acquisition, completion, or renovation
9. property and investment modules extend capital visibility

## Property workflow

### Actor entry points

| Actor | Entry Point | Capabilities |
|-------|-------------|--------------|
| **Guest / Public** | `/properties`, `/properties/:id` | browse, search, filter, submit anonymous inquiries, book appointments |
| **Buyer** | `/properties`, `/properties/:id` | same as public, plus authenticated inquiry tracking |
| **Project Owner** | `/properties`, `/properties/:id`, `/owner/dashboard` | create listings, edit own listings, link to projects, manage inquiries/appointments |
| **Property Manager** | `/property-manager/dashboard` | create listings, manage assigned listings, publish availability, handle inquiries/appointments |
| **Investor** | `/properties`, `/properties/:id` | browse and evaluate; finance applications can target properties |
| **Admin** | `/admin`, `/properties/:id` | full CRUD on all properties, manage all inquiries/appointments, view reports |

### Workflow steps

1. **Property Owner** or approved **Property Manager** creates a standalone property listing
2. Listing operators enrich the asset with:
   - structured specifications, features, pricing, ownership context
   - media, floor plans, virtual tours
   - showing schedules and availability windows
3. Development metadata captures zoning, readiness, utilities, and operating context
4. **Public** and **authenticated** users discover the property through search and filters
5. Users submit inquiries (anonymous allowed if phone/email provided)
6. Inquiry creation triggers:
   - notifications to owner/manager
   - a chat thread for follow-up communication
7. Owner or manager defines calendar availability for visits
8. Users book appointment slots from the property calendar
9. The property may remain **standalone** or be **linked to a project**
10. Financing may target either:
    - the property itself (acquisition, renovation, completion)
    - a linked project (structured budget, milestones, execution cash flow)
11. When linked to a project, formal materials and service demand flows through `ProjectRequirement`
12. **Admin** can moderate, verify ownership, or manage any listing across the platform

## Compliance workflow

1. user or entity onboarding begins for a specialized workflow
2. admin or compliance review determines whether the role is activated
3. KYC / AML checks are applied where required
4. jurisdiction rules influence access or processing
5. risk signals and audit trails are recorded
6. reporting and regulatory outputs are generated

## Role activation workflow

1. user registers once into the base `PROJECT_OWNER` account
2. user enters a specialized workspace intentionally
3. workspace prompts for the required profile or onboarding submission
4. admin reviews and approves or rejects the request
5. approved specialization is added to the user's accessible roles
6. user keeps base access and may accumulate multiple non-admin roles
7. `ADMIN` remains a separate manually assigned operator identity

Examples of approved specialization include:

- vendor operations
- contractor operations
- investor operations
- property management operations

## Logistics workflow

1. user activates courier onboarding if they want logistics-partner workflows
2. courier profile is created and approved where required
3. order or shipment is created
4. carrier or courier assignment is made
5. pricing zone and pricing rule logic determines cost
6. tracking events update shipment state

## Context sources

- `docs/BUYER_WORKFLOW_PHASE1.md`
- `docs/MILESTONE_PAYMENT_WORKFLOW.md`
- `docs/DISPUTE_RESOLUTION_WORKFLOW.md`
- `docs/INVESTMENT_WORKFLOW.md`
- `docs/KYC_AML_WORKFLOW.md`
- `docs/GOVERNMENT_PROCUREMENT_WORKFLOW.md`
- `docs/CREDIT_SCORING_WORKFLOW.md`
- `docs/BANKING_ESCROW_INTEGRATIONS.md`
- `docs/ROLE_AND_ONBOARDING_POLICY.md`
