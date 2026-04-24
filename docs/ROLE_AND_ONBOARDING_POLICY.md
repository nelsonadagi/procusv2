# Role And Onboarding Policy

## Purpose

This document defines the intended user-role model for the platform and how onboarding, approval, and workspace activation should work.

It should be treated as the current policy target when product copy, admin workflows, and access-control behavior are updated.

## Core policy

### Default identity

All new non-admin users register into a shared base account:

- primary role: `PROJECT_OWNER`

This base identity is the platform's default operating mode and should be enough to:

- browse public marketplace content
- create projects
- request quotes
- place orders
- manage project-owner workflows

### Specialized roles

Other business roles are not intended to be granted at registration.

They are activated only after:

1. the user explicitly chooses that workflow
2. the user completes the relevant onboarding/profile submission
3. an admin approves that submission where required

Specialized roles:

- `VENDOR`
- `CONTRACTOR`
- `INVESTOR`
- `PROPERTY_MANAGER`
- `COURIER`
- `GOVERNMENT`

### Admin identity

`ADMIN` is separate from the normal multi-role user model.

Rules:

- `ADMIN` is manually assigned
- `ADMIN` should not be mixed into normal user `roles[]`
- admin assignment should happen through admin/operator controls, not self-service flows

## Multi-role model

Normal users may hold multiple approved non-admin roles.

Recommended structure:

- `role`: current primary or active workspace role
- `roles[]`: approved additional non-admin roles

Example:

```json
{
  "role": "PROJECT_OWNER",
  "roles": ["VENDOR", "CONTRACTOR", "PROPERTY_MANAGER"]
}
```

Important constraints:

- `PROJECT_OWNER` is the default base role
- `ADMIN` should not appear in `roles[]`
- specialized roles are added as the result of workflow approval, not simple profile edits

## Approval-driven activation

### Vendor

Flow:

1. user registers as base `PROJECT_OWNER`
2. user opens vendor workspace
3. user submits vendor profile
4. admin approves vendor profile
5. platform grants or confirms `VENDOR` role access

### Contractor

Flow:

1. user registers as base `PROJECT_OWNER`
2. user opens contractor workspace
3. user submits contractor profile
4. admin reviews credentials
5. platform grants or confirms `CONTRACTOR` role access

### Investor

Flow:

1. user registers as base `PROJECT_OWNER`
2. user opens investor workspace
3. user submits investor/KYC onboarding
4. admin or compliance workflow verifies the profile
5. platform grants or confirms `INVESTOR` role access

### Property manager

Flow:

1. user registers as base `PROJECT_OWNER`
2. user opens property management workspace
3. user submits property-manager onboarding or ownership/management credentials
4. admin reviews and approves the submission where required
5. platform grants or confirms `PROPERTY_MANAGER` role access

### Courier

Flow:

1. user registers as base `PROJECT_OWNER`
2. user opens courier workspace
3. user submits courier company profile
4. admin or operations workflow approves it if required
5. platform grants or confirms `COURIER` role access

### Government

Flow:

1. user registers as base `PROJECT_OWNER`
2. user opens government workspace
3. user completes institution-specific onboarding
4. admin or governance workflow approves the institution
5. platform grants or confirms `GOVERNMENT` role access

## Access-control guidance

Specialized actions should not rely on role text alone.

They should normally require both:

- an approved role assignment
- a corresponding approved profile or onboarding record

Examples:

- vendor catalog management should require vendor profile existence and usable approval state
- contractor bidding should require contractor profile existence and approval
- investor agreement activity should require investor onboarding and KYC state
- property listing management should require property ownership or approved property-manager access
- courier logistics management should require courier profile existence
- government publishing should require government onboarding and approval

Public interaction rule:

- anonymous property inquiries may be allowed without a platform role if callback phone or email is provided
- public appointment booking may be allowed against manager-defined availability slots
- lead capture should still create auditable inquiry records, notifications, and communication threads

## Product copy and prompt guidance

User-facing prompts should reinforce workflow activation instead of self-declared identity.

Prefer messages like:

- "Activate vendor workspace"
- "Complete contractor onboarding"
- "Submit for investor approval"
- "Activate property manager workspace"
- "Set viewing availability"
- "Your courier profile is pending review"

Avoid messages like:

- "Choose your permanent role now"
- "You are now a vendor" before approval
- "Change your role to unlock access" when a missing profile is the real blocker

### Prompt fit assessment

Current prompt direction that fits this policy well:

- registration copy that describes one shared account first
- onboarding cards that say "activate" or "continue onboarding"
- dashboard states that distinguish:
  - no profile yet
  - pending review
  - approved and ready

Current prompt direction that should be phased out:

- registration copy that implies users should pick a role first
- profile copy that implies any user can freely assign themselves specialized roles
- dashboard copy that says a role change alone unlocks access without approval

Recommended prompt sequence for specialized workflows:

1. invite the user to activate the workspace
2. explain the onboarding required
3. show review or approval status clearly
4. unlock the specialized workspace only after approval is confirmed

## Admin UX implications

Admin controls should behave as workflow approval tools, not arbitrary identity editors.

Preferred admin behavior:

- review onboarding submissions
- approve or reject them
- grant the corresponding specialized role on approval
- keep admin assignment separate from normal role activation

## Documentation implications

When updating docs or UI copy:

- describe `PROJECT_OWNER` as the base/default role
- describe other non-admin roles as approved specializations
- describe `PROPERTY_MANAGER` as the specialized role for standalone property operations
- describe `ADMIN` as separate and manually assigned
- describe multiple non-admin roles as valid for one user
