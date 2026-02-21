# SECURITY_CHECKLIST.md

## Construction Marketplace MVP — Security Checklist (Phase 1)

This document defines the minimum security controls required for a production-ready Phase 1 marketplace.

---

## 1. Authentication & Access Control

* Use JWT authentication
* Enforce strong password policies
* Support phone/email verification

### Admin-Only Configuration Permissions

* **Platform Manage Settings**: Restricted to `platform_admin`
* **Gateway Secrets**: Encrypted at rest; visible only via secure fields
* **Audit Trail**: mandatory for all gateway and configuration overrides
* **Module Switches**: feature flags only manageable via backoffice.

Permissions must be enforced at API level.

---

## 2. Vendor Trust & Verification

Phase 1 requires manual verification:

* Business registration check
* Location confirmation
* Verified badge status

Prevent unverified vendors from accepting payments.

---

## 3. Data Protection

* Use HTTPS everywhere
* Encrypt secrets in environment variables
* Never store raw payment details

---

## 4. Payment Security

* Payments handled via provider (Stripe/Mpesa)
* Store only transaction references
* Prevent duplicate payment execution

---

## 5. Marketplace Fraud Prevention

* Rate-limit quote requests
* Detect abnormal pricing changes
* Admin moderation of suspicious vendors

---

## 6. Order Integrity

* Orders immutable after payment
* Snapshot product pricing at purchase
* Maintain audit logs for disputes

---

## 7. Infrastructure Security

* Docker images pinned to stable versions
* Database backups enabled
* Restrict admin access via IP or MFA

---

## 8. Compliance Readiness (Future)

Phase 2+:

* KYC for financing
* Escrow compliance
* Regional tax/VAT support

---

**Phase 1 security baseline is now defined.**
