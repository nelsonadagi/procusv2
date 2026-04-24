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
9. checkout validates stock and records an inventory commit
10. vendor confirms with an estimated delivery date
11. cancellation of eligible orders restores stock, then fulfillment, delivery, review, or dispute follows

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

## Project and capital workflow

1. owner creates project
2. project requirements are added
3. contracts can be linked to projects
4. updates are posted
5. investors pledge commitments
6. property and investment modules extend capital visibility

## Property workflow

1. property owner or approved `PROPERTY_MANAGER` creates a standalone property listing
2. listing operators can enrich the asset with structured specifications, features, pricing, ownership context, media, and showing schedules
3. development metadata captures zoning, readiness, and operating context
4. public or authenticated users discover the property through search and filters
5. users may submit inquiries anonymously if callback phone or email is provided
6. inquiry creation should trigger notifications and a communication thread
7. owner or manager defines calendar availability for visits
8. users book appointment slots from the property calendar
9. the property may remain standalone or be linked to a project
10. financing may target either the property itself or a linked project
11. when linked to a project, formal materials and service demand should flow through project requirements

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
