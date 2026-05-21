# Property Module Workflow UX Blueprint

This document redesigns the property module as a guided operational workflow, not a passive listing catalog.

The module must help users complete property tasks without training or human intervention by always showing:

- what is happening
- what to do next
- what is blocked
- what is urgent
- what can wait
- who is responsible
- what unlocks after the next action

The property module covers:

- property discovery
- property listing management
- inquiries
- appointment booking
- financing
- project linkage
- operator review and moderation

---

## 1. Module Experience Vision

The user is trying to move a property opportunity forward without having to interpret the platform first.

Examples of that goal:

- a property owner wants to publish a listing and receive inquiries
- a property manager wants to manage listings, availability, and bookings
- a buyer wants to compare properties, ask questions, and book a visit
- an investor wants to understand whether the property is finance-ready or project-linked
- an admin wants to verify or moderate the asset safely

### What makes the current UX difficult

- properties contain rich information, but the next step is not always obvious
- a listing can be discoverable even when key data is missing
- inquiries, appointments, financing, and project linkage are related but not always presented as one workflow
- empty states often explain a feature instead of directing action
- users can get lost between property detail, property manager tools, and project execution

### Ideal experience

The property module should feel like an operational assistant that says:

1. this property is ready to publish
2. these fields are missing
3. this inquiry needs a reply
4. this appointment can be booked now
5. this property can be linked to a project
6. this financing path is available

The user should never wonder what to do next.

---

## 2. User Goals

### Public Visitor

#### Primary User Goals

- find a property that matches location, type, and budget
- understand whether the property is suitable for buying, leasing, development, or completion
- send an inquiry without friction
- book a visit if slots are available

#### Secondary User Goals

- compare properties
- check whether a property is finance-ready
- view project linkage if it exists

#### Urgent User Goals

- get a response to an inquiry
- secure an appointment slot

#### Recurring Operational Goals

- return to the listing
- monitor inquiry responses
- follow the property timeline

### Project Owner

#### Primary User Goals

- create a property listing
- use the property as the starting point for a project
- receive and manage inquiries
- publish availability

#### Secondary User Goals

- attach financing options
- maintain structured property data
- track property-to-project continuity

#### Urgent User Goals

- publish a listing quickly
- respond to inbound interest

#### Recurring Operational Goals

- edit listing data
- publish new availability
- review project linkage

### Property Manager

#### Primary User Goals

- manage assigned listings
- keep inquiries and appointments moving
- publish availability
- maintain accurate listing data

#### Secondary User Goals

- support finance-ready listings
- coordinate with owners and buyers

#### Urgent User Goals

- respond to an inquiry
- publish visit slots
- fix incomplete listing data

#### Recurring Operational Goals

- update listings
- maintain calendars
- review incoming leads

### Investor

#### Primary User Goals

- inspect a property as an acquisition or development opportunity
- assess readiness, risk, and financing posture
- move into investment or project-linked finance

#### Secondary User Goals

- compare properties
- review ownership and development notes

#### Urgent User Goals

- identify whether the opportunity is finance-ready
- confirm whether a property is linked to a project

#### Recurring Operational Goals

- track property-related opportunities
- return to promising assets

### Buyer

#### Primary User Goals

- understand the asset quickly
- contact the owner or manager
- book a visit
- decide whether to proceed

#### Secondary User Goals

- track follow-up communication
- evaluate commercial terms

#### Urgent User Goals

- get a response
- reserve a viewing slot

#### Recurring Operational Goals

- revisit saved properties
- compare options

### Admin / Staff

#### Primary User Goals

- review listings
- verify or moderate property records
- resolve issues

#### Secondary User Goals

- audit activity
- manage platform quality

#### Urgent User Goals

- resolve problematic listings
- unblock a pending review

#### Recurring Operational Goals

- monitor approvals
- inspect activity timelines

---

## 3. Workflow-First UX Redesign

The property module should behave as a guided workflow with the following stages.

### Property Listing Workflow

| Stage | What User Sees | Main CTA | Secondary Actions | Blockers | Guidance |
|---|---|---|---|---|---|
| Draft | Basic property form with missing fields highlighted | Complete Listing | Save draft, preview | missing title, location, price, listing type | show a completion checklist |
| Ready to Publish | Listing has enough information to be useful | Publish Listing | Add media, add features, add finance info | no media, no specs, no availability | recommend the next missing section |
| Published | Property appears in search and detail pages | Share Listing | Edit details, publish availability | incomplete commercial data | show visibility status |
| Active Lead Flow | Inquiries and visits are coming in | Respond to Leads | Manage appointments, update listing | unanswered inquiry, no available slots | prioritize response tasks |
| Linked to Project | Property is tied to execution | Open Project | Review requirements, manage progress | project not created yet | recommend project creation |
| Archived | Property is no longer active | Restore Listing | Duplicate listing | none | explain reactivation path |

### Discovery Workflow

| Stage | What User Sees | Main CTA | Secondary Actions | Blockers | Guidance |
|---|---|---|---|---|---|
| Browsing | Search and filters with results cards | Open Property | Refine filters | no results | suggest widening filters |
| Comparing | Cards, pricing, availability, and key specs | View Details | Save search, compare | missing data | explain what is missing |
| Deciding | Property detail with inquiry, appointment, finance, and project options | Contact Owner | Book Visit, Apply For Financing | no slot, inquiries closed | show why the action is unavailable |

### Inquiry Workflow

| Stage | What User Sees | Main CTA | Secondary Actions | Blockers | Guidance |
|---|---|---|---|---|---|
| Inquiry Ready | Contact form on the property page | Send Inquiry | Book visit, call, message | inquiry disabled | recommend booking or project link |
| Inquiry Submitted | Confirmation and follow-up context | View Timeline | Open chat | no contact details | show expected response path |
| Inquiry Active | Owner/manager has responded | Continue Conversation | Schedule visit | no reply yet | highlight waiting-on-others |
| Inquiry Closed | Lead resolved or archived | Reopen Conversation | View history | none | keep communication history visible |

### Appointment Workflow

| Stage | What User Sees | Main CTA | Secondary Actions | Blockers | Guidance |
|---|---|---|---|---|---|
| Slots Published | Visit windows visible on the property page | Book Slot | Ask question, view map | no slots | explain when to check back |
| Slot Selected | One slot highlighted with form | Confirm Booking | Change slot, add notes | missing contact info | validate fields inline |
| Booking Confirmed | Success message and timeline entry | View Appointment | Reschedule, cancel if allowed | approval required | tell user what happens next |
| Visit Completed | Appointment record with outcome | Add Follow-Up | Return to property | none | suggest inquiry or finance next |

### Finance Workflow

| Stage | What User Sees | Main CTA | Secondary Actions | Blockers | Guidance |
|---|---|---|---|---|---|
| Finance Available | Finance tab enabled with product choices | Apply For Financing | Compare products | no finance products | explain target types |
| Application Draft | Product and purpose fields | Submit Application | Save draft | missing product or amount | suggest defaults |
| Under Review | Status tracking and summary | View Status | Upload missing docs | compliance gap | explain review timing |
| Approved | Funding path visible | Continue To Funding | Read terms | none | show next operational step |

### Property-to-Project Workflow

| Stage | What User Sees | Main CTA | Secondary Actions | Blockers | Guidance |
|---|---|---|---|---|---|
| Standalone Asset | Property exists on its own | Link To Project | Keep as property only | no project intent | explain when linking helps |
| Project Candidate | Development opportunity is evident | Create Project | Review scope, add requirements | insufficient details | recommend project creation |
| Linked Asset | Property and project cross-link each other | Open Project Workspace | View property history | none | keep both records visible |

---

## 4. Next-Best-Action Engine

The module should always prioritize the next useful action.

### Trigger Conditions and Responses

| Trigger Condition | User Context | Recommended Action | Priority | Escalation | CTA Buttons | Notification Trigger |
|---|---|---|---|---|---|---|
| Incomplete listing setup | owner or manager creating a property | complete missing listing sections | high | remind after inactivity | Continue Listing, Save Draft | listing draft saved |
| Missing media | property is draft or poor-performing | upload photos or floor plans | medium | none | Upload Media | media incomplete |
| No availability published | property should support visits | add showing slots | high | alert after property is live for a while | Publish Availability | booking blocked |
| Inquiry waiting too long | lead has not been answered | reply to inquiry | high | escalate to owner/manager | Open Inquiry, Reply Now | lead waiting |
| Appointment request pending | booking submitted | confirm or reschedule | high | notify operator and visitor | Review Booking | visit pending |
| Finance path available | property can be financed | open financing application | medium | none | Apply For Financing | finance eligible |
| Project opportunity detected | property has development signals | create or link a project | medium | suggest after repeated views | Create Project | project suggestion |
| Search returns no results | user over-filtered | reset or widen filters | medium | none | Reset Filters | no-result guidance |
| Property under review | admin or staff reviewing | resolve review item | high | escalate by SLA | Review Listing | review pending |

### Why the recommendation matters

- it reduces user uncertainty
- it shortens the path to completion
- it prevents users from abandoning a workflow at a dead end
- it makes the module feel responsive rather than static

---

## 5. Workspace Redesign

The property module should behave as a workspace, not just a page.

### Property Manager Workspace

#### Priority Zones

- urgent actions: inquiries, bookings, publish availability
- waiting-on-you: listing completion, unanswered leads
- waiting-on-others: booking confirmations, admin review
- timeline: recent inquiries, appointments, updates
- recommendations: add media, link project, publish finance

#### What appears first

1. property completion status
2. urgent leads and bookings
3. publish availability button
4. listing health and missing fields

#### What should be hidden initially

- advanced property metadata
- internal verification notes
- secondary relationship sections

### Property Detail Workspace

The detail page should open with:

1. property headline
2. price or commercial terms
3. current status
4. next best action
5. tabs for overview, specs, financing, links, and communication

### Buyer / Visitor Workspace

The detail page should open with:

1. summary of what the asset is
2. whether it is available
3. whether inquiries or visits are open
4. the main CTA for the current stage
5. what to do if a slot or response is not available

---

## 6. Navigation Redesign

Navigation should reflect the workflow, not the database.

### Good Navigation Labels

- Browse Properties
- View Details
- Send Inquiry
- Book Visit
- Apply For Financing
- Link To Project
- Manage Availability
- Review Leads

### Avoid

- broad admin labels like "Property Records"
- unexplained technical labels like "Property Console"
- menu items that expose every sub-object at once

### Progressive Navigation

- beginner users see browse, contact, and book
- operators see manage listing, availability, and leads
- advanced users see project linkage, finance, and audit

### Mobile Navigation

- search
- filters
- contact
- book
- timeline
- finance

---

## 7. Multi-Step Wizard Design

### Create Property Wizard

#### Step 1: Core Identity

- Purpose: define the asset
- User guidance: title, type, listing type, location
- Validation: required fields must be completed
- Defaults: suggest country and listing type from context
- Smart suggestions: infer asset type from selected purpose
- Completion: save draft automatically

#### Step 2: Commercial Terms

- Purpose: define price and finance posture
- User guidance: ask for a real price or rent amount
- Validation: at least one commercial term should be present
- Defaults: currency from active country
- Smart suggestions: show pricing strategy choices
- Completion: allow publish only if terms are valid

#### Step 3: Property Facts

- Purpose: help buyers compare the property
- User guidance: bedrooms, bathrooms, area, condition, occupancy
- Validation: optional but strongly recommended
- Smart suggestions: hide irrelevant fields when asset type is land or development

#### Step 4: Media And Proof

- Purpose: make the listing trustworthy
- User guidance: add photos, floor plans, or documents
- Smart suggestions: mark a primary image automatically

#### Step 5: Availability And Leads

- Purpose: enable visits and inquiries
- User guidance: turn on inquiry and appointment workflows
- Validation: if appointments are on, at least one slot should be publishable

#### Step 6: Publish

- Purpose: move from draft to live listing
- Completion behavior: show a publish summary and what becomes visible

### Book Visit Wizard

#### Step 1: Choose Slot
#### Step 2: Add Contact Details
#### Step 3: Add Notes
#### Step 4: Confirm Booking

The form should auto-save selected slot and explain what happens after confirmation.

### Finance Application Wizard

#### Step 1: Pick Target
#### Step 2: Choose Purpose
#### Step 3: Enter Amount
#### Step 4: Review Terms
#### Step 5: Submit

---

## 8. Timeline and Activity UX

The timeline should show the property journey.

### Timeline Structure

- property created
- media added
- listing published
- inquiry received
- inquiry answered
- visit booked
- visit completed
- finance application submitted
- finance approval or rejection
- project linked
- listing archived

### Ownership Visibility

- show who acted
- show what changed
- show whether the system or a user made the update

### Escalation Visibility

- show if a lead has been waiting too long
- show if a booking has not been confirmed
- show if a review is blocking publication

### Recovery Actions

- reply now
- publish slots
- complete missing listing fields
- link the property to a project
- resubmit finance details

---

## 9. Empty States and Guided States

### No Properties

- message: "You have not created a property yet."
- why it matters: the workspace is empty because there is no asset to operate on
- CTA: Create Listing
- setup time: 5 to 10 minutes
- template: use the property creation wizard
- automation: prefill country, location, and listing type

### No Results

- message: "No properties match your filters."
- why it matters: the search is too narrow
- CTA: Reset Filters
- setup time: immediate
- template: suggested filter reset
- automation: suggest nearby or finance-ready assets

### No Inquiries

- message: "No one has contacted you yet."
- why it matters: the listing may be incomplete or not visible enough
- CTA: Improve Listing
- setup time: 10 to 20 minutes
- automation: suggest missing media or price clarity

### No Appointments

- message: "You have not published any visit slots."
- why it matters: users cannot book visits
- CTA: Publish Availability
- setup time: 5 to 10 minutes
- automation: suggest recurring weekly slots

### No Financing Products

- message: "No financing options are available right now."
- why it matters: the user may need a different route
- CTA: Link Project or Check Again Later
- setup time: immediate
- automation: suggest project-linked finance if the property is a development asset

### No Linked Projects

- message: "This property is still standalone."
- why it matters: project context is optional but useful for development assets
- CTA: Create Project
- setup time: 10 to 15 minutes
- automation: prefill project scope from property data

---

## 10. Blocking and Validation UX

| Blocker | Cause | User Message | Recovery Path | Escalation Logic | Auto-Recovery |
|---|---|---|---|---|---|
| Inquiries disabled | owner turned off inbound contact | inquiries are closed for this property | enable inquiries in listing settings | none | yes, when owner toggles on |
| Appointment slots missing | no availability published | no visit slots are available yet | publish availability | remind operator after activation | yes, by copying previous slot pattern |
| Missing title or location | draft listing incomplete | this listing needs a title and location | complete core details | none | no |
| Missing price or commercial terms | user cannot compare or finance | add pricing to continue | fill commercial section | none | yes, with suggested currency |
| Permission missing | user is not owner/manager/admin | you do not have permission to change this property | switch to the correct workspace or request access | admin review if needed | no |
| Review pending | admin or compliance action required | this listing is waiting for review | wait or respond to requested changes | escalate on SLA breach | no |
| Finance not allowed | property cannot be financed directly | this property uses project-linked finance instead | link the property to a project | suggest project workflow | yes, by redirecting to project finance |

The UI should explain:

- why the action is blocked
- who needs to act
- what the user can do now
- what unlocks after resolution

---

## 11. Action Hierarchy Design

### Primary Actions

- create listing
- publish listing
- send inquiry
- book visit
- apply for financing
- link project

### Secondary Actions

- edit details
- add media
- add features
- manage availability
- view timeline
- compare assets

### Rare Actions

- archive listing
- delete property
- moderate listing
- verify ownership

### Dangerous Actions

- delete property
- deactivate listing
- reject financing application
- cancel confirmed appointment

Rules:

- primary actions should be visible immediately
- secondary actions should be in a compact action rail
- rare actions should live in menus
- dangerous actions should require confirmation and show impact

---

## 12. Human Language Rewrite

### Status Messages

- "Draft complete. You can publish after adding media or availability."
- "Inquiry received. The owner or manager should reply soon."
- "Visit booked. The property team will confirm the appointment."
- "Finance application submitted. Review is underway."
- "Project linked. Property and execution records now move together."

### Empty State Messages

- "Create your first property listing to start receiving leads."
- "Publish availability so visitors can book a visit."
- "Add pricing and media so buyers can compare this property."

### Approval Messages

- "Your property listing is waiting for review."
- "Your listing is approved and now visible in search."
- "This property can now accept inquiries and visits."

### Error Messages

- "This property cannot be published yet because the title is missing."
- "This visit cannot be booked because no slots are open."
- "This finance application needs a selected product and amount."

### Success Messages

- "Listing published successfully."
- "Inquiry sent to the owner or manager."
- "Visit booked successfully."

### Escalation Messages

- "This inquiry has been waiting too long. Please respond now."
- "The listing is live, but no visit slots have been published."
- "The property is ready for a project link. Create one to continue."

---

## 13. Intelligent Notifications

| Trigger | Recipient | Priority | Delivery Channel | Deep Link Destination | Recommended Action |
|---|---|---|---|---|---|
| New inquiry | owner / manager | high | in-app, email | property detail inquiry tab | reply now |
| New appointment request | owner / manager | high | in-app, push | booking panel | confirm or reschedule |
| Appointment confirmed | visitor | medium | in-app, SMS | appointment timeline | prepare for visit |
| No response to inquiry | owner / manager | high | in-app | property inbox | respond now |
| Listing review required | owner / admin | high | in-app, email | property moderation panel | resolve missing data |
| Finance application submitted | owner / investor-facing reviewer | medium | in-app, email | finance tab | review application |
| Project link created | owner / manager | medium | in-app | project workspace | continue into execution |
| Visit slot published | visitor followers / interested users | medium | in-app | property detail | book visit |

Notifications should always say:

- what changed
- why it matters
- what the user should do next

---

## 14. Operational Health System

### Property Health

Scoring factors:

- listing completeness
- media completeness
- availability published
- inquiry response speed
- appointment conversion
- financing readiness
- project linkage readiness

### Warning Thresholds

- 80 to 100: healthy
- 60 to 79: watch
- 40 to 59: at risk
- below 40: stalled

### Recovery Recommendations

- add missing details
- publish media
- publish availability
- respond to leads
- link to project

### Visual Indicators

- green: ready
- amber: needs attention
- red: blocked

---

## 15. AI-Assisted UX Opportunities

The AI layer should give practical operational assistance.

### Useful AI behaviors

- detect missing listing steps
- recommend best property-to-project transition points
- suggest if a property is finance-ready
- predict inquiry conversion risk
- warn when appointment slots are too sparse
- flag stale listings
- recommend which property fields are still missing

### Not useful

- generic marketing copy
- vague "optimize your strategy" messages
- actions without explanation

### Example AI prompts

- "This listing is ready to publish, but it needs at least one image."
- "This property looks like a development opportunity. Create a project to continue."
- "Inquiry volume is low because availability has not been published."
- "This asset is finance-ready, but ownership notes are incomplete."

---

## 16. Mobile Experience Redesign

### Mobile Priority Actions

- create listing draft
- reply to inquiry
- publish availability
- book visit
- confirm finance application
- open property timeline

### Mobile Navigation

- overview
- leads
- appointments
- financing
- project link

### Quick Actions

- new inquiry reply
- publish slot
- add media
- create project

### Swipe Actions

- dismiss
- save draft
- mark reviewed

### Offline Handling

- save draft property edits locally
- queue inquiry replies if connection is weak
- show sync status clearly

### Camera / File Capture UX

- capture listing photos directly
- upload floor plans or documents
- label media immediately after capture

---

## 17. Accessibility and Inclusivity

### WCAG Considerations

- keyboard accessible controls
- visible focus states
- high-contrast status colors
- semantic headings and landmarks

### Color Independence

- status should never rely on color alone
- pair badges with text labels

### Screen Reader Support

- buttons should have descriptive names
- timeline entries should read in order
- booking slots should announce time clearly

### Low Literacy UX

- short sentences
- clear next-step labels
- icon plus text on key actions

### Multilingual UX

- use simple wording that translates cleanly
- avoid idioms and jargon

### Low Bandwidth UX

- defer heavy media until needed
- show text summaries even when images are slow
- keep core actions available without waiting for galleries

---

## 18. Progressive Disclosure Model

### Beginner Experience

- browse properties
- open property detail
- send inquiry
- book visit
- see one clear next step

### Intermediate Experience

- manage availability
- edit listings
- compare assets
- view timeline
- apply for financing

### Advanced Experience

- link property to project
- moderate or verify listings
- inspect operational health
- manage multiple workflows at once

### Usage Maturity Rules

- keep advanced controls hidden until the user has a role that needs them
- keep operator-only sections collapsed by default
- surface guided checklists first

---

## 19. Cross-Module Intelligence

| Trigger | Suggested Action | Automation Opportunity | Workflow Continuity |
|---|---|---|---|
| Property is development-ready | create project | prefill project data from property fields | property to project |
| Project requirements appear | suggest procurement | generate material and service needs | project to procurement |
| Finance-ready property is opened | suggest financing | open property-targeted finance flow | property to finance |
| Inquiries increase on a listing | suggest response prioritization | rank unanswered leads | property to communication |
| Property linked to a project | show project workspace | sync status and timelines | property to execution |
| Visit completed | suggest follow-up | prompt inquiry or project conversion | property to lead nurturing |
| Delivery or supply needs appear | suggest materials | connect to procurement module | property to materials |

---

## 20. Final UX Transformation Summary

### Current UX Problems

- listings are information-rich but action-light
- workflow steps are separated instead of coordinated
- many pages explain the data rather than guide the user
- users can reach dead ends in search or empty states
- cross-module transitions are present but not obvious enough

### Proposed UX Transformation

- turn property pages into guided workspaces
- show the next step at every stage
- make inquiry, booking, financing, and project linkage feel continuous
- replace dead-end empties with recovery actions
- show health, status, and responsibility clearly

### Operational Benefits

- faster publishing
- better lead conversion
- fewer support questions
- clearer property-to-project flow
- better appointment completion

### User Psychology Improvements

- less uncertainty
- more confidence
- more trust in the platform
- less need to ask for help

### Cognitive Load Reductions

- fewer choices at once
- more progressive disclosure
- clearer labels
- obvious next actions

### Workflow Efficiency Gains

- faster listing setup
- faster inquiry response
- easier booking
- clearer finance and project transitions

### Adoption Improvements

- users can complete property workflows independently
- operators can work without training calls
- the module feels like a system that knows the job

