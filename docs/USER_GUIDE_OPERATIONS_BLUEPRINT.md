# User Guide Operations Blueprint

This document converts the existing user guide into a workflow-intelligence blueprint for UI, UX, product operations, and workflow automation.

It preserves the documented roles and business flows while adding:

- workflow state models
- next-best-action guidance
- validation and blocker logic
- notification and escalation logic
- dashboard priorities
- timeline semantics
- progressive disclosure
- mobile considerations
- AI-assisted operational guidance

## 1. Platform Experience Philosophy

The platform should behave like a guided operating system for construction commerce and project execution.

### Core Principles

| Principle | Operational Meaning |
|---|---|
| Workflow-first UX | Every screen should answer "what can I do next?" before showing secondary detail. |
| Goal-driven navigation | Navigation should be organized around outcomes such as buying materials, posting tenders, approving milestones, or resolving disputes. |
| Contextual guidance | The system should explain why a step matters, what blocks the step, and what happens after completion. |
| Progressive disclosure | Show the minimum necessary controls first; reveal advanced actions only when the user is ready or the workflow requires them. |
| Operational visibility | Every major object should expose current state, next action, risk, owner, and deadline. |
| State-aware interfaces | Buttons, tabs, cards, and empty states should change based on object lifecycle and permissions. |
| Role-aware experiences | The dashboard should reflect the user’s approved roles and operational responsibilities. |
| Intelligent dashboards | Dashboards should prioritize active work, blocked items, expiring deadlines, and items awaiting approval. |
| AI-assisted operations | AI should recommend the next operational action, not generate vague strategy. |
| Trust and transparency | The system should show what changed, who changed it, when, and why. |

### Experience Behavior

The platform should continuously guide users through the next action that moves a workflow forward.

- If a workflow is incomplete, the UI should show the missing requirement, not only the error.
- If an approval is pending, the UI should show the approver, the deadline, and the impact of delay.
- If a payment is completed, the UI should immediately surface delivery or fulfillment progress.
- If a workflow stalls, the system should recommend the recovery path, not just display a status.
- If the user has multiple roles, the interface should keep the base workspace available while exposing the specialized workspaces only when relevant.

## 2. Role Analysis

### Project Owner

#### Role Objectives

- create and manage projects
- post contracts and tenders
- procure materials and services
- review bids and award work
- fund milestones and release escrow
- monitor execution, delivery, and disputes

#### Primary Workflows

1. Register into the base project-owner workspace.
2. Create a project or start from a property-linked opportunity.
3. Define requirements and procurement needs.
4. Post tenders or request materials.
5. Review bids or quote responses.
6. Award contracts or accept quotes.
7. Approve milestones and release payments.
8. Monitor progress, delivery, disputes, and project completion.

#### Critical Actions

- create project
- post tender
- review bids
- award contract
- fund escrow
- approve milestone
- resolve disputes

#### Common Failure Points

- project created without requirements
- tender posted without clear evaluation criteria
- award delayed because bids are not comparable
- escrow not funded before work starts
- milestone approval delayed due to missing evidence
- user cannot find the next operational step

#### UX Guidance Opportunities

- show a project readiness score
- show missing requirements before tender posting
- highlight bids that match budget and timeline
- recommend the next milestone review action
- warn when funding is insufficient for the next release

#### Dashboard Priorities

- active projects
- pending approvals
- open procurements
- escrow status
- milestone timeline
- overdue tasks
- disputes

#### Notifications

- new bid received
- contract awarded
- milestone ready for approval
- escrow release pending
- payment confirmed
- dispute opened
- project overdue

#### Timeline Events

- project created
- tender posted
- bid submitted
- contract awarded
- milestone approved
- funds released
- dispute opened or resolved

#### AI Assistance Opportunities

- recommend bid shortlist based on cost, timeline, and vendor history
- predict project delay risk
- detect underfunded milestones
- suggest missing procurement items
- surface likely dispute causes

### Vendor

#### Role Objectives

- complete vendor onboarding
- get verified by admin
- manage product inventory
- respond to quote requests
- fulfill orders
- maintain stock accuracy
- track shipment and delivery status

#### Primary Workflows

1. Register as a base user.
2. Activate vendor onboarding.
3. Submit business and operational details.
4. Wait for admin approval.
5. Create or import products.
6. Maintain inventory levels and product metadata.
7. Receive quote requests and new orders.
8. Confirm orders and set delivery estimates.
9. Pack, ship, and track delivery progress.
10. Resolve order issues and follow up on disputes.

#### Critical Actions

- complete onboarding
- get approved
- create products
- keep stock accurate
- respond to quotes
- confirm orders
- ship orders

#### Common Failure Points

- pending verification blocks full vendor operations
- missing product details reduce quote conversion
- stock quantity becomes stale
- order status updated without delivery estimate
- shipment tracking missing after payment
- vendor misses approval or inquiry notifications

#### UX Guidance Opportunities

- onboarding checklist with verification state
- inventory health warnings
- quote response deadlines
- order readiness alerts
- shipment initiation prompt after payment confirmation

#### Dashboard Priorities

- pending verifications
- quote requests awaiting response
- new orders
- low-stock warnings
- active shipments
- fulfillment backlog

#### Notifications

- vendor approved
- quote request received
- quote accepted
- order placed
- payment confirmed
- shipment ready
- delivery delayed

#### Timeline Events

- vendor onboarding submitted
- vendor approved
- product created or imported
- quote response submitted
- order confirmed
- shipment created
- delivery completed

#### AI Assistance Opportunities

- stock reorder suggestions
- quote pricing suggestions
- late-shipment risk detection
- product completeness checks
- fulfillment workload forecasting

### Contractor

#### Role Objectives

- complete contractor onboarding
- upload credentials
- pass verification
- discover tenders
- submit bids
- execute awarded work
- track milestones and payments

#### Primary Workflows

1. Register as a base user.
2. Activate contractor onboarding.
3. Submit certifications and profile data.
4. Wait for admin approval.
5. Browse tenders and post bids.
6. Track shortlists, awards, and milestones.
7. Execute work and report progress.
8. Receive milestone approvals and payments.

#### Critical Actions

- complete verification
- submit bid
- respond to clarification requests
- report milestone progress
- close out work

#### Common Failure Points

- verification pending blocks bidding
- missing bid details reduce competitiveness
- unclear tender scope creates incorrect bids
- milestone evidence not uploaded
- payments delayed because approval is pending

#### UX Guidance Opportunities

- verification checklist
- bid completeness scoring
- deadline countdowns
- milestone evidence prompts
- award and start-work guidance

#### Dashboard Priorities

- open tenders
- submitted bids
- awarded jobs
- pending milestones
- payment status

#### Notifications

- verification approved
- tender matched
- bid received
- bid shortlisted or awarded
- milestone approval due
- payment released

#### Timeline Events

- contractor onboarding submitted
- verification approved
- bid posted
- contract awarded
- milestone completed
- payment released

#### AI Assistance Opportunities

- bid competitiveness feedback
- win probability signals
- schedule risk detection
- milestone delay warnings
- document completeness checks

### Investor

#### Role Objectives

- complete onboarding and KYC
- discover projects and assets
- pledge capital
- confirm commitments
- sign agreements
- monitor returns and distributions

#### Primary Workflows

1. Request investor role activation.
2. Complete KYC and compliance review.
3. Browse fundable projects or opportunities.
4. Review risk, funding gap, and timeline.
5. Pledge capital.
6. Confirm commitments.
7. Sign agreements.
8. Track portfolio and distributions.

#### Critical Actions

- complete KYC
- review project risk
- pledge capital
- confirm commitment
- sign agreement

#### Common Failure Points

- KYC incomplete
- project risk not understood
- funding commitment not confirmed
- agreement unsigned
- distribution status unclear

#### UX Guidance Opportunities

- KYC completion checklist
- funding gap explanation
- expected return visibility
- risk warnings tied to project state
- agreement status prompts

#### Dashboard Priorities

- KYC status
- active pledges
- pending confirmations
- portfolio performance
- distribution timeline

#### Notifications

- KYC approved
- commitment requested
- agreement ready for signature
- milestone approved
- distribution available
- compliance review requested

#### Timeline Events

- KYC submitted
- KYC approved
- pledge created
- commitment confirmed
- agreement signed
- distribution paid

#### AI Assistance Opportunities

- project risk scoring
- capital allocation suggestions
- completion probability
- late milestone impact detection
- concentration risk warnings

### Property Manager

#### Role Objectives

- manage property listings
- coordinate inquiries and appointments
- publish availability
- link properties to projects
- support finance and redevelopment workflows

#### Primary Workflows

1. Activate property-manager onboarding.
2. Create and publish property listings.
3. Add availability and viewing slots.
4. Respond to inquiries and appointment requests.
5. Link assets to projects when needed.
6. Support financing or redevelopment workflows.

#### Critical Actions

- publish listing
- respond to inquiry
- approve viewing
- update availability
- maintain property accuracy

#### Common Failure Points

- listing published without availability
- inquiry not answered quickly
- property detail missing key operational data
- linked project context absent

#### UX Guidance Opportunities

- inquiry urgency badge
- appointment readiness indicator
- property completeness scoring
- linked-project suggestion

#### Dashboard Priorities

- active listings
- new inquiries
- appointment requests
- availability calendar
- linked projects

#### Notifications

- inquiry received
- appointment booked
- listing updated
- finance request received
- project link requested

#### Timeline Events

- listing created
- inquiry received
- appointment scheduled
- listing updated
- property linked to project

#### AI Assistance Opportunities

- listing quality suggestions
- inquiry response prioritization
- appointment conversion risk
- pricing comparison guidance

### Government

#### Role Objectives

- publish tenders
- manage institutional procurement
- review submissions
- enforce compliance
- monitor reporting and traceability

#### Primary Workflows

1. Activate government workspace.
2. Publish or manage tenders.
3. Review contractor or supplier responses.
4. Track compliance and audit trail.
5. Manage award and reporting obligations.

#### Critical Actions

- publish tender
- review submissions
- award procurement
- monitor compliance
- produce reports

#### Common Failure Points

- incomplete tender data
- unclear eligibility rules
- delayed evaluation
- insufficient audit evidence

#### UX Guidance Opportunities

- publication checklist
- compliance summary
- deadline tracking
- award recommendation summary

#### Dashboard Priorities

- active tenders
- pending reviews
- compliance alerts
- award deadlines
- reporting queue

#### Notifications

- tender published
- submission received
- review due
- compliance issue flagged
- report ready

#### Timeline Events

- tender drafted
- tender published
- submission received
- evaluation completed
- award published

#### AI Assistance Opportunities

- eligibility completeness checks
- tender inconsistency detection
- deadline risk detection
- compliance gap highlighting

### Admin

#### Role Objectives

- approve specialized roles
- manage compliance and moderation
- oversee disputes
- configure system settings
- monitor security and audit trails

#### Primary Workflows

1. Review onboarding and verification requests.
2. Approve or reject specialized roles.
3. Monitor security, moderation, and audit events.
4. Resolve disputes or escalate them.
5. Maintain configuration, countries, currencies, taxonomies, and permissions.

#### Critical Actions

- approve users
- verify entities
- resolve disputes
- manage settings
- review audit events

#### Common Failure Points

- approvals delayed
- missing review queue visibility
- disputes not surfaced in one place
- configuration drift across modules

#### UX Guidance Opportunities

- consolidated review queue
- approval SLA tracking
- risk-based prioritization
- system health indicators

#### Dashboard Priorities

- pending approvals
- verification queue
- disputes
- security events
- audit logs
- configuration health

#### Notifications

- approval requested
- verification issue
- dispute escalated
- security incident
- configuration change

#### Timeline Events

- role approved
- entity verified
- dispute escalated
- system setting changed
- security event recorded

#### AI Assistance Opportunities

- approval prioritization
- duplicate entity detection
- risk-based escalation
- abnormal activity detection

### Courier

#### Role Objectives

- complete courier onboarding
- manage logistics settings
- receive shipment work
- track delivery progress
- update shipment statuses

#### Primary Workflows

1. Register courier profile.
2. Get approved if required.
3. Configure pricing zones and rules.
4. Receive shipment assignments.
5. Update tracking events and delivery status.
6. Resolve failed delivery or reroute cases.

#### Critical Actions

- complete onboarding
- configure service area
- update shipment status
- capture tracking events

#### Common Failure Points

- shipment created without carrier assignment
- pricing rules missing
- delivery updates delayed
- tracking number not available to buyer

#### UX Guidance Opportunities

- shipment queue
- service-area readiness
- route status
- failed-delivery recovery prompt

#### Dashboard Priorities

- assigned shipments
- pending pickups
- in-transit deliveries
- failed deliveries
- pricing setup status

#### Notifications

- shipment assigned
- pickup pending
- route updated
- delivery failed
- delivery completed

#### Timeline Events

- courier approved
- pricing rule created
- shipment assigned
- tracking event created
- delivery completed

#### AI Assistance Opportunities

- route delay prediction
- shipment workload balancing
- delivery failure detection
- pricing zone suggestions

### Buyer / Public Visitor

#### Role Objectives

- browse products and properties
- request quotes
- place orders
- follow delivery
- open disputes when necessary
- explore the platform without friction

#### Primary Workflows

1. Browse catalog or properties.
2. Request a quote or make an inquiry.
3. Review vendor responses.
4. Accept a quote and check out.
5. Monitor order status and delivery.
6. Open a dispute if needed.

#### Critical Actions

- request quote
- compare responses
- checkout
- confirm delivery
- open dispute

#### Common Failure Points

- no quote responses
- address missing at checkout
- payment recorded but delivery not visible
- tracking number absent

#### UX Guidance Opportunities

- quote status explanations
- delivery progress visibility
- payment-to-delivery continuity
- dispute helper guidance

#### Dashboard Priorities

- quote requests
- open orders
- delivery tracking
- messages
- disputes

#### Notifications

- quote response received
- order placed
- payment confirmed
- shipment initiated
- delivery status changed
- dispute resolution update

#### Timeline Events

- quote requested
- quote received
- order placed
- payment confirmed
- delivery started
- delivery completed

#### AI Assistance Opportunities

- response comparison
- delivery ETA warning
- reorder reminders
- dispute risk detection

## 3. Workflow State Model

### Projects

| State | Meaning | Allowed Actions | Blockers | Next Recommended Action |
|---|---|---|---|---|
| Draft | Project is being assembled | edit, add requirements, link property | missing scope or budget | complete project details |
| Ready for Procurement | Requirements are sufficient | post tenders, invite bids | missing BoQ or timeline | publish procurement need |
| In Procurement | Bids or offers are being collected | review, shortlist, revise | insufficient responses | wait or expand scope |
| Awarded | Work has been assigned | fund escrow, start execution | unsigned agreement | activate contract |
| In Execution | Work is underway | update milestones, monitor progress | delayed milestone, funding shortfall | review status and approvals |
| At Risk | Execution is blocked | escalate, renegotiate, dispute | unresolved issue | open resolution workflow |
| Completed | Project is finished | archive, report, payout | none | close and report |

### Tenders / Contracts

| State | Meaning | Allowed Actions | Blockers | Next Recommended Action |
|---|---|---|---|---|
| Draft | Not yet public | edit, validate, preview | missing scope | finalize tender |
| Published | Visible to eligible bidders | receive bids, update timeline | unclear eligibility | monitor responses |
| Bidding | Active responses arriving | bid, shortlist, compare | deadline passed | review submissions |
| Awarded | Winning bidder chosen | sign, start execution | award not accepted | confirm contract terms |
| Active | Work in progress | submit milestones, raise issues | milestone overdue | continue execution |
| Closed | Work finished or cancelled | archive, report | none | close record |

### Orders

| State | Meaning | Allowed Actions | Blockers | Next Recommended Action |
|---|---|---|---|---|
| PLACED | Order created, awaiting payment or processing | pay, cancel if allowed, message vendor | missing payment method | complete payment |
| CONFIRMED | Vendor and system acknowledged the order | pack, estimate delivery, create shipment | missing fulfillment update | prepare shipment |
| PACKING | Order is being prepared | update packing status, add note | stock shortage | complete packing |
| SHIPPED | Shipment created and in transit | track, update carrier events | missing tracking | monitor delivery |
| DELIVERED | Delivered to recipient | confirm receipt, open dispute if needed | buyer not available | confirm or resolve |
| COMPLETED | Delivery accepted and closed | rate, archive | none | leave feedback |
| CANCELLED | Order voided | restock, notify parties | non-cancellable state | restore stock or close |

### Escrow

| State | Meaning | Allowed Actions | Blockers | Next Recommended Action |
|---|---|---|---|---|
| Unfunded | No money locked | fund, reconcile | missing source payment | deposit funds |
| Held | Funds reserved | monitor, approve milestone | dispute or missing approval | wait for milestone review |
| Release Pending | Approval received | release, reconcile | insufficient approval evidence | verify release conditions |
| Released | Funds transferred | audit, report | none | close payment event |
| Frozen | Dispute or hold exists | resolve, review, refund | unresolved dispute | start resolution |

### Milestones

| State | Meaning | Allowed Actions | Blockers | Next Recommended Action |
|---|---|---|---|---|
| Draft | Milestone defined but not active | edit, schedule | incomplete scope | finalize milestone |
| Active | Work is in progress | update progress, attach evidence | no evidence | continue execution |
| Submitted | Contractor says milestone is ready | review, approve, reject | missing attachments | inspect work |
| Approved | Owner accepted work | release funds | escrow unavailable | trigger payout |
| Rejected | Work failed review | revise, resubmit | unresolved defects | fix issues |

### Property Listings

| State | Meaning | Allowed Actions | Blockers | Next Recommended Action |
|---|---|---|---|---|
| Draft | Not published | edit, preview, enrich | missing media or metadata | complete listing |
| Published | Visible in marketplace | inquire, book, link project | incomplete availability | maintain listing |
| Active Inquiry | User interest exists | respond, schedule, negotiate | no contact response | reply promptly |
| Under Review | Ownership or compliance review | verify, moderate | legal or documentation issue | resolve review item |
| Linked to Project | Property is attached to project flow | manage project handoff | missing project detail | align workflows |
| Archived | No longer active | restore, duplicate | none | republish or close |

### Investments

| State | Meaning | Allowed Actions | Blockers | Next Recommended Action |
|---|---|---|---|---|
| Discoverable | Visible to investors | review, compare, pledge | incomplete disclosure | review project |
| Pledged | Intent expressed | confirm, revise | KYC incomplete | complete commitment |
| Confirmed | Capital committed | sign agreement | unsigned agreement | execute agreement |
| Funded | Funds locked and active | track, report | none | monitor progress |
| Returning | Distributions available | view payout, audit | milestone delay | wait for release |
| Closed | Investment completed | archive | none | review return summary |

### KYC

| State | Meaning | Allowed Actions | Blockers | Next Recommended Action |
|---|---|---|---|---|
| Not Started | User has not begun | start, upload documents | no data | begin verification |
| Submitted | Documents uploaded | review, edit if allowed | incomplete documents | finish submission |
| Under Review | Admin/compliance review active | wait, respond | pending verification | monitor status |
| Verified | Approved | operate, transact | none | proceed |
| Rejected | Failed review | correct, resubmit | failing document or policy | resolve rejection reason |

### Vendor Verification

| State | Meaning | Allowed Actions | Blockers | Next Recommended Action |
|---|---|---|---|---|
| Not Applied | No vendor profile | start onboarding | no submission | create profile |
| Pending | Submitted for review | wait, update if allowed | missing fields | complete application |
| Approved | Vendor can operate | publish products, receive orders | none | manage inventory |
| Rejected | Application declined | revise, resubmit | unresolved compliance issue | fix and reapply |
| Suspended | Temporarily inactive | appeal, resolve issue | policy violation | contact admin |

### Contractor Verification

| State | Meaning | Allowed Actions | Blockers | Next Recommended Action |
|---|---|---|---|---|
| Not Applied | No contractor profile | start onboarding | no submission | create profile |
| Pending | Submitted for review | wait, edit if permitted | missing credentials | complete application |
| Approved | Can bid | browse tenders, bid | none | submit bid |
| Rejected | Not approved | resubmit | incomplete documents | correct and reapply |

### Deliveries

| State | Meaning | Allowed Actions | Blockers | Next Recommended Action |
|---|---|---|---|---|
| Not Started | Payment not yet confirmed or shipment not created | pay, confirm order | unpaid order | complete payment |
| Initiated | Shipment record created | track, pack, assign carrier | missing carrier detail | prepare fulfillment |
| Packed | Ready for dispatch | ship, update tracking | carrier unavailable | hand off to courier |
| In Transit | Moving toward destination | monitor, update ETA | route delay | watch tracking |
| Delivered | Reached recipient | confirm, dispute if needed | recipient unavailable | verify receipt |
| Failed | Delivery attempt failed | retry, reschedule | address or access issue | correct delivery data |

### Disputes

| State | Meaning | Allowed Actions | Blockers | Next Recommended Action |
|---|---|---|---|---|
| Opened | Issue reported | review, attach evidence | missing details | collect evidence |
| Under Review | Admin or operator is reviewing | respond, mediate | incomplete record | wait for review |
| Frozen | Funds or workflow paused | resolve, approve hold | unresolved conflict | decide outcome |
| Resolved | Outcome reached | close, release | none | finalize record |
| Escalated | Needs higher authority | escalate, audit | complex or repeated issue | assign escalation owner |

## 4. Next-Best-Action Engine

The platform should always determine:

- what the user should do next
- what is blocking them
- what is urgent
- what is optional

### Rule Structure

| Trigger Condition | Message | Severity | CTA | Destination Page | Escalation Rule |
|---|---|---|---|---|---|
| Incomplete onboarding | Complete your profile to unlock this workflow | High | Finish onboarding | role onboarding page | remind after 24h, escalate to admin queue after 72h |
| Unpaid escrow | Funds are not yet secured for the next milestone | High | Fund escrow | escrow page | notify owner and finance contacts |
| Pending milestone approval | Review submitted work to keep the project moving | High | Review milestone | milestone detail page | escalate after SLA expiry |
| Missing verification | This specialization is blocked until approval | High | Submit documents | verification page | notify admin review queue |
| Delayed shipment | Delivery is behind schedule | Medium | Track delivery | shipment page | alert vendor and buyer after threshold |
| Funding shortfall | The budget gap is still open | High | Review funding options | project financing page | notify investor leads and owner |
| Unsigned agreement | The workflow cannot become binding yet | High | Sign agreement | agreement page | remind user and notify counterpart |

### Example Guidance by Role

#### Project Owner

- show incomplete project scope
- recommend posting procurement only after requirements are ready
- surface milestone approval deadlines
- warn about funding gaps before execution stalls

#### Vendor

- show pending quote requests
- warn about low stock and expiring delivery promises
- recommend shipment initiation after payment confirmation

#### Contractor

- show tenders nearing deadline
- warn when verification is incomplete
- recommend uploading evidence before milestone submission

#### Investor

- show KYC completeness
- recommend reviewing risk before pledging
- highlight commitments waiting on signature

#### Property Manager

- show inquiries waiting for response
- recommend updating availability when appointments fill up
- warn when listing data is stale

#### Government

- show tenders needing review
- recommend compliance checks before award
- warn on deadline and transparency gaps

#### Admin

- show highest-risk approvals first
- prioritize disputes and compliance review
- surface stalled workflows by SLA

#### Courier

- show shipments awaiting action
- recommend updating tracking after pickup
- warn when a delivery is overdue or failed

#### Buyer / Public Visitor

- show quote responses waiting
- recommend checkout after quote comparison
- warn when payment is recorded but shipment has not started

## 5. Dashboard Intelligence Design

### Project Owner Dashboard

#### Sections

- active projects
- procurement queue
- milestone status
- escrow status
- dispute queue
- property-linked opportunities

#### Priority Hierarchy

1. blocked or overdue work
2. pending approvals
3. active procurement
4. recently completed items

#### Metrics

- active projects
- budget remaining
- milestones due
- escrow balance
- disputes open

#### Alerts

- milestone overdue
- escrow underfunded
- contract unsigned
- project risk elevated

#### Recommended Actions

- post tender
- review bids
- approve milestone
- fund escrow

#### Empty States

- explain how to start a project
- show one-click actions to create project or post tender

#### Quick Actions

- create project
- post tender
- review bids
- open disputes

### Vendor Dashboard

#### Sections

- onboarding status
- inventory health
- quote requests
- open orders
- shipments
- low-stock products

#### Priority Hierarchy

1. verification status
2. orders requiring response
3. low-stock risks
4. active shipments

#### Metrics

- response time
- fulfillment rate
- low-stock items
- shipped orders

#### Alerts

- unverified vendor profile
- overdue quote response
- low stock
- shipment delay

#### Recommended Actions

- complete verification
- respond to quote
- confirm order
- ship order

#### Empty States

- explain how to finish vendor onboarding
- prompt inventory creation or CSV import

#### Quick Actions

- add product
- import CSV
- adjust stock
- view orders

### Contractor Dashboard

#### Sections

- verification status
- tenders
- bids submitted
- active jobs
- milestones
- payments

#### Priority Hierarchy

1. verification
2. pending bids
3. active milestones
4. payment status

#### Metrics

- bids submitted
- awards won
- milestone completion rate
- payment status

#### Alerts

- unverified profile
- bid deadline close
- milestone overdue
- payment pending

#### Recommended Actions

- complete verification
- submit bid
- upload evidence
- review award

#### Empty States

- explain how to start bidding
- link to onboarding and active tenders

#### Quick Actions

- browse tenders
- submit bid
- upload document
- open active job

### Investor Dashboard

#### Sections

- KYC status
- opportunities
- pledges
- agreements
- portfolio
- distributions

#### Priority Hierarchy

1. KYC
2. commitments waiting
3. distribution events
4. portfolio risk

#### Metrics

- pledged capital
- confirmed commitments
- active agreements
- expected distributions

#### Alerts

- KYC incomplete
- agreement unsigned
- funding target near deadline
- project delay risk

#### Recommended Actions

- complete KYC
- review opportunity
- confirm commitment
- sign agreement

#### Empty States

- explain investment process
- show verified opportunities and what each stage means

#### Quick Actions

- browse projects
- pledge capital
- sign agreement
- view portfolio

### Property Manager Dashboard

#### Sections

- listings
- inquiries
- appointments
- availability calendar
- linked projects
- financing requests

#### Priority Hierarchy

1. new inquiries
2. today’s appointments
3. stale listings
4. linked project updates

#### Metrics

- inquiry volume
- booking rate
- response time
- active listings

#### Alerts

- inquiry unanswered
- appointment conflict
- listing incomplete
- approval needed

#### Recommended Actions

- respond to inquiry
- update availability
- publish listing
- link property to project

#### Empty States

- explain how property listings create lead flow
- prompt first property creation

#### Quick Actions

- add property
- manage calendar
- reply to inquiry
- link project

### Government Dashboard

#### Sections

- active tenders
- submissions
- compliance flags
- awards
- reports

#### Priority Hierarchy

1. tenders nearing deadline
2. compliance issues
3. awards waiting
4. reporting obligations

#### Metrics

- open tenders
- review backlog
- compliance issues
- reporting completion

#### Alerts

- deadline risk
- missing evaluation data
- transparency issue

#### Recommended Actions

- review submission
- publish award
- resolve compliance issue

#### Empty States

- explain tender publishing path
- show next procurement action

#### Quick Actions

- publish tender
- review bids
- award contract
- export report

### Admin Dashboard

#### Sections

- approval queue
- verifications
- disputes
- security events
- configuration
- audit log

#### Priority Hierarchy

1. high-risk approvals
2. blocked workflows
3. disputes
4. security/compliance issues

#### Metrics

- approval SLA
- outstanding verifications
- unresolved disputes
- security alerts

#### Alerts

- approval overdue
- suspicious activity
- failed verification
- workflow stuck

#### Recommended Actions

- approve or reject
- request missing documents
- resolve dispute
- inspect audit trail

#### Empty States

- explain that this is an operations center
- show all queues as empty only when the platform is truly clear

#### Quick Actions

- approve user
- review dispute
- inspect audit
- manage settings

### Courier Dashboard

#### Sections

- onboarding status
- shipment queue
- tracking events
- failed deliveries
- pricing rules

#### Priority Hierarchy

1. pending pickups
2. in-transit shipments
3. failed deliveries
4. setup gaps

#### Metrics

- active shipments
- on-time delivery rate
- failed delivery rate
- service areas configured

#### Alerts

- shipment assignment
- route delay
- failed delivery
- missing pricing rule

#### Recommended Actions

- update shipment
- confirm pickup
- resolve failed delivery
- configure pricing

#### Empty States

- explain how to activate courier operations
- prompt service-area setup

#### Quick Actions

- view shipments
- update status
- add pricing zone
- edit profile

### Buyer / Public Visitor Dashboard

#### Sections

- quote requests
- orders
- tracking
- messages
- disputes

#### Priority Hierarchy

1. active orders
2. payment confirmation
3. shipment progress
4. responses waiting

#### Metrics

- open requests
- paid orders
- shipments in transit
- disputes open

#### Alerts

- quote response ready
- payment confirmed
- shipment started
- delivery delayed

#### Recommended Actions

- compare responses
- complete checkout
- track delivery
- open dispute

#### Empty States

- explain how quotes and orders work
- point to browse or request flow

#### Quick Actions

- browse marketplace
- request quote
- open order
- start chat

## 6. Timeline and Activity System

The timeline should function as the platform memory for every workflow object.

### Timeline Layers

- global activity feed for recent important events
- entity timeline for a project, order, or contract
- audit trail for admin and compliance actions
- communication history for messages, comments, and approvals
- milestone visibility for execution tracking

### Timeline Event Format

Each event should include:

- timestamp
- actor
- action
- entity
- state before
- state after
- reason or note
- linked notification

### Example Events

- project created
- tender published
- bid submitted
- vendor approved
- quote request sent
- quote response received
- order placed
- payment confirmed
- shipment initiated
- milestone approved
- dispute opened
- dispute resolved
- investor commitment confirmed
- KYC approved

### Visibility Rules

- users should see events relevant to their role and entities they own, manage, or participate in
- admins should see all workflow-critical events
- public users should only see their own inquiries, property interactions, and authenticated objects
- sensitive compliance details should be visible only to authorized reviewers

## 7. Notification and Escalation System

### Notification Channels

- email for durable records and approvals
- in-app for real-time workflow prompts
- SMS for urgent delivery, approval, or deadline events
- WhatsApp for high-engagement operational reminders where supported
- push for mobile workflow moments and short-turnaround approvals

### Notification Rules

| Trigger | Recipient | Priority | Retry Policy | Escalation Rules |
|---|---|---|---|---|
| Approval requested | reviewer or admin | High | retry until acknowledged | escalate when SLA expires |
| Dispute opened | counterparty, admin | High | retry on failure | escalate if unresolved |
| Payment confirmed | buyer, vendor, courier if needed | High | retry until delivered | escalate only if delivery does not start |
| Deadline expiring | responsible user | Medium to High | retry before deadline | escalate after threshold |
| Missing compliance | user and admin | High | retry once | lock action if required |
| Failed delivery | buyer, vendor, courier | High | immediate retry | escalate if no recovery update |
| Contract awarded | winner, owner | Medium | retry twice | escalate if acceptance missing |
| Investment confirmed | investor, owner | Medium | retry twice | escalate if signature pending |

### Escalation Principles

- operational deadlines should escalate before the workflow fully stalls
- urgent financial or compliance events should escalate faster than informational updates
- repeated failure to act should move the item into a higher-priority queue
- escalation should always include a recovery action

## 8. Empty States and Guided States

Each empty state should teach the user what the feature does, why it matters, and how to begin.

| Empty State | Guidance | Business Value | CTA | Estimated Effort | Onboarding Assistance |
|---|---|---|---|---|---|
| No projects | Explain that projects track procurement and execution | Gives the user a control center for work | Create project | Low | guided project setup |
| No bids | Explain how bids compare suppliers or contractors | Accelerates award decisions | Browse tenders or request bids | Low | eligibility explanation |
| No products | Explain that products must exist before quotes and orders | Enables commerce | Add product | Medium | CSV import and template |
| No investments | Explain that investments unlock capital tracking | Creates funding visibility | Browse opportunities | Low | risk summary |
| No orders | Explain how quotes become orders after checkout | Starts delivery workflow | Request quote | Low | workflow primer |
| Incomplete profile | Explain what data unlocks the workspace | Prevents blocked actions later | Complete profile | Low | checklist |
| Unverified account | Explain approval as a specialization gate | Protects trust and compliance | Submit verification | Medium | document checklist |
| No properties | Explain listings drive inquiries and capital flows | Creates lead generation | Add property | Medium | listing guide |
| No milestones | Explain milestones connect work to payment | Enables progress and release logic | Create milestone | Low | milestone template |

## 9. Validation and Blocking Logic

When an action is blocked, the UI should say why, what to fix, and what happens after the fix.

| Blocker | Reason | User Message | Recovery Guidance | Recommended Action |
|---|---|---|---|---|
| Missing role approval | specialization is not verified | This workspace is locked until approval is complete | complete onboarding and wait for review | open verification flow |
| Missing payment method | checkout cannot continue | Select an active payment method to proceed | use an enabled gateway | choose payment method |
| Insufficient permissions | user cannot modify this object | You do not have access to this action | switch workspace or request access | contact admin or owner |
| Invalid transition | workflow state does not allow the action | This item cannot move to that state yet | check required prior step | complete prerequisite |
| Missing compliance docs | regulated workflow needs documentation | Upload the missing document to continue | submit required files | upload document |
| Incomplete address or delivery location | order cannot be delivered reliably | Add a valid delivery location | create or select a hub | update delivery data |
| No available approver | approval queue is blocked | No approver is assigned yet | notify admin or supervisor | assign reviewer |
| Shipment not initiated | order paid but delivery not started | Delivery has not started yet | initiate fulfillment or shipment | view order timeline |

## 10. Progressive Disclosure Model

### Beginner Experience

Show only:

- primary actions
- current status
- one clear next step
- simplified terminology
- guided empty states

### Intermediate Experience

Show:

- dashboard widgets
- timelines
- filters
- comparison tools
- approval queues
- context cards

### Advanced Experience

Show:

- bulk operations
- audit views
- performance metrics
- automation controls
- export tools
- operational exceptions

### Visibility Rule

Do not expose advanced controls unless the user has:

- the required role
- the object in the correct state
- the required validation completed

## 11. Cross-Module Intelligence

### Property to Project

- Trigger: property listing becomes development-ready
- Recommendation: create or link a project
- Automation: carry listing metadata into project requirements

### Project to Procurement

- Trigger: project requirements are complete
- Recommendation: publish tender or request materials
- Automation: generate procurement checklist

### Procurement to Contractor Hiring

- Trigger: bids are received
- Recommendation: shortlist and award
- Automation: compare bid cost, timing, and risk

### Project to Financing

- Trigger: budget gap exists
- Recommendation: open funding workflow
- Automation: suggest financing options

### Milestone to Escrow Release

- Trigger: milestone approved
- Recommendation: release escrow
- Automation: create payment release task

### Payment to Delivery

- Trigger: order payment confirmed
- Recommendation: initiate shipment and fulfillment
- Automation: create shipment and tracking timeline entry

### Delayed Delivery to Dispute

- Trigger: shipment delay threshold exceeded
- Recommendation: open support or dispute path
- Automation: notify buyer, vendor, and courier

### Verification to Role Activation

- Trigger: documents approved
- Recommendation: unlock workspace
- Automation: add role access and dashboard sections

## 12. AI-Assisted UX Opportunities

AI should improve operations, not replace workflow ownership.

| Use Case | What AI Should Do | What It Should Not Do |
|---|---|---|
| Procurement recommendations | rank tenders, suppliers, or contractors by fit | auto-award without human review |
| Contractor risk scoring | surface delay, quality, or compliance risk | block users without explainable basis |
| Funding suggestions | highlight likely funding gaps and timing | promise financing approval |
| Project completion prediction | estimate risk of late completion | replace project management judgment |
| Anomaly detection | flag suspicious or unusual workflow patterns | generate false certainty |
| Delivery risk prediction | warn about route or shipment delays | override courier operations automatically |
| Financial warnings | identify cash flow or escrow concerns | make investment decisions for users |
| Compliance assistance | identify missing docs or invalid transitions | act as legal advice |

### Practical AI Outputs

- "Your project needs one more procurement step before tender publication."
- "This contractor has a higher delay risk because three prior milestones were late."
- "This payment is complete, but shipment has not been initiated."
- "Your investor commitment is waiting on one missing KYC document."
- "This property could be linked to a project because the listing is development-ready."

## 13. Mobile UX Considerations

The mobile experience should support fast operational decisions.

- quick approvals with one-tap confirm/reject
- notification-driven entry points
- compact timeline cards
- mobile-first shipment and milestone updates
- field-friendly upload flows for photos and documents
- courier-friendly status changes with minimal typing
- offline-tolerant draft capture for notes and evidence
- persistent action buttons for urgent workflows

### Mobile Priorities by Role

- Project Owner: approvals, project status, disputes
- Vendor: quote response, order update, shipment status
- Contractor: bid submission, milestone evidence
- Investor: pledge review, agreement signing
- Property Manager: inquiry response, appointment updates
- Courier: tracking updates, delivery completion
- Admin: review queue, approval decisions

## 14. Accessibility and Inclusivity

### Accessibility Requirements

- use semantic headings and landmarks
- maintain keyboard navigation for all critical actions
- provide visible focus states
- avoid color-only status communication
- pair icons with text where the meaning is not obvious
- support screen-reader labels for buttons and state chips
- preserve readable contrast across status colors

### Inclusivity Requirements

- support multilingual workflows
- keep terminology plain and role-appropriate
- allow low-bandwidth fallback where possible
- compress long workflows into small steps
- use explanation text for approvals and rejections
- avoid assuming users understand construction, finance, or compliance jargon

## 15. Final UX Principles Summary

The platform should operate as a guided workflow engine with a visible state machine behind every major user journey.

- workflow-first design: start with what the user is trying to complete
- intelligent guidance: show the next best action, not just the current page
- contextual actions: only show relevant controls for the current state and role
- role-driven experiences: each dashboard reflects the user’s operational responsibilities
- operational transparency: every state change should be visible in a timeline or audit trail
- progressive complexity: beginners see the essentials; advanced users can access full operational controls
- trust-oriented workflows: approvals, payments, verification, and delivery should always be explainable
- actionable dashboards: surfaces should highlight blockers, urgency, and next steps

This blueprint should be treated as the behavioral spec for UI design, workflow automation, dashboard layout, and notification logic across the platform.
