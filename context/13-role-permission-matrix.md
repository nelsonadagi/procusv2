# Role Permission Matrix

## Purpose

This file combines the documented role model with the current RBAC implementation pattern so access control work has a concrete starting point.

## Primary user roles in the platform

From docs and code:

- `ADMIN`
- `PROJECT_OWNER`
- `VENDOR`
- `CONTRACTOR`
- `INVESTOR`
- `PROPERTY_MANAGER`
- `GOVERNMENT`
- `COURIER`

Additional group-oriented roles seeded in RBAC:

- `GUEST`
- `BUYER`
- `VERIFIED_INVESTOR`
- `GOVERNMENT_OWNER`
- `GOVERNMENT_AUDITOR`

## How authorization works

### Layer 1: user role

The custom user model has:

- one primary `role`
- optional JSON list of additional `roles`

Recommended policy direction:

- `PROJECT_OWNER` is the default base role for normal users
- other non-admin roles are approved specializations
- normal users may hold multiple approved non-admin roles
- `ADMIN` should remain separate and should not be mixed into normal `roles[]`
- onboarding approval should be the usual trigger for granting specialized roles

### Layer 2: Django groups

Users are synchronized into Django groups based on role and additional roles.

### Layer 3: logical permissions

Permissions are seeded under the `rbac` app label using codenames like:

- `catalog_view`
- `contracts_post_contract`
- `projects_create_project`

Views then check logical permissions such as:

- `catalog:view`
- `contracts:post_contract`
- `projects:create_project`

## Namespace-level permission families

Seeded permission namespaces include:

- `catalog`
- `orders`
- `contracts`
- `bids`
- `contractors`
- `escrow`
- `finance`
- `disputes`
- `projects`
- `property`
- `investments`
- `enterprise`
- `government`
- `logistics`
- `milestones`
- `compliance`
- `risk`
- `banking`
- `integrations`
- `users`
- `vendors`
- `taxonomy`
- `security`
- `reviews`
- `reports`

## Permission registry policy

The platform now treats permissions as a predefined catalog rather than free-form admin-created records.

Admin implications:

- the seed layer creates the known permission registry under the `rbac` app label
- each seeded role starts with a default permission bundle
- the admin roles screen should assign or remove predefined permissions from roles
- admins should not create, rename, or delete permissions from the UI

## Practical role summary

### ADMIN

Effective access:

- full access by role shortcut in permission checks
- broad management of platform, roles, users, moderation, security, and reporting
- should be manually assigned rather than granted through self-service onboarding

### PROJECT_OWNER

Typical access:

- default base identity for new users
- buyer-style procurement actions
- create and update projects
- post and award contracts
- manage milestones
- release escrow-related funds where allowed
- remain available even when the user also becomes a vendor, contractor, investor, courier, or government actor

### VENDOR

Typical access:

- create and update catalog entries
- manage stock
- process orders
- manage own vendor-owned resources

### CONTRACTOR

Typical access:

- view contracts
- submit bids
- participate in milestone and dispute-related workflows relevant to execution

### INVESTOR

Typical access:

- view projects and investment opportunities
- pledge commitments
- sign agreements

### PROPERTY_MANAGER

Typical access:

- create and update property listings on behalf of self or an owner
- manage property calendars and appointment availability
- respond to property inquiries
- manage linked property-to-project operational context
- expose financing and follow-up workflows for standalone assets

Seeded permission bundle:

- `projects:view`
- `property:view`
- `property:list_property`
- `property:update_property`
- `reports:view`

### COURIER

Typical access in practice:

- manage own courier profile
- interact with shipments and pricing resources tied to own profile

Seeded permission bundle:

- `orders:view`
- `integrations:view`
- `logistics:view`
- `logistics:onboard`
- `logistics:manage_profile`
- `logistics:manage_pricing`
- `logistics:manage_shipments`
- `reports:view`
- `banking:view`
- `banking:manage_accounts`

## Group mapping note

Normal user roles should map to their matching RBAC groups:

- `PROJECT_OWNER` -> `PROJECT_OWNER`
- `VENDOR` -> `VENDOR`
- `CONTRACTOR` -> `CONTRACTOR`
- `INVESTOR` -> `INVESTOR`
- `PROPERTY_MANAGER` -> `PROPERTY_MANAGER`
- `GOVERNMENT` -> `GOVERNMENT`
- `COURIER` -> `COURIER`

`GOVERNMENT_OWNER` and `GOVERNMENT_AUDITOR` remain elevated RBAC groups, but they should not be used as the default sync target for a normal user whose account role is simply `GOVERNMENT`.

### BUYER / buyer-capable roles

Current code suggests buyer actions can be performed by:

- `PROJECT_OWNER`
- `CONTRACTOR`
- `ADMIN`

This should be treated as implementation truth for now, but the product direction is to treat buyer behavior as part of the base `PROJECT_OWNER` identity rather than as a separate end-user registration role.

## Approval-driven role activation

Preferred model:

1. user registers with base `PROJECT_OWNER`
2. user starts a specialized onboarding flow
3. admin approves that workflow
4. the corresponding specialized role is granted

Approval state should be reflected in prompts and access decisions:

- no profile yet: invite activation
- submitted and pending: show review state
- approved: enable specialized workspace
- rejected or incomplete: explain next corrective action

This should apply to:

- `VENDOR`
- `CONTRACTOR`
- `INVESTOR`
- `PROPERTY_MANAGER`
- `COURIER`
- `GOVERNMENT`

## Implementation guidance

Before changing permissions:

1. inspect the view permission classes
2. inspect `permission_map` and `required_permission`
3. confirm whether ownership checks also apply
4. confirm whether admin bypass is intentional
5. verify frontend role assumptions still match backend values

## Known caution

The documented user classes and the RBAC seed model are close, but not perfectly identical. Always validate both the user `role` value and the seeded group permission model before making access changes.
