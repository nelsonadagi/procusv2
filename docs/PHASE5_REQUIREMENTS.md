# PHASE5_REQUIREMENTS.md

## Construction Marketplace — Phase 5 Requirements

Phase 5 introduces the **Regulated Investment + Enterprise + Government Procurement Layer**.

Phase 5 transforms the platform into infrastructure-grade construction commerce.

---

## 1. Phase 5 Objective

Enable:

* Regulated investment flows (binding funding)
* Institutional and enterprise procurement workflows
* Government tendering and compliance
* Global tax, localization, and audit readiness

---

---

## 2. Actors & Permissions

### Verified Investor (KYC approved)
*   **Permissions**: `investments:view`, `investments:sign_agreement`, `investments:transfer_stake`, `compliance:view`
*   **Enforcement**: Restricted to investors who have passed `compliance:verify_kyc`. Required for binding capital deployment.

### Compliance Admin
*   **Permissions**: `compliance:verify_kyc`, `compliance:report_aml`, `risk:view`
*   **Actions**: Verify investor identities and perform anti-money laundering checks.

### Enterprise Requester / Approver / Admin
*   **Requester Permissions**: `orders:create`, `enterprise:request_approval`
*   **Approver Permissions**: `enterprise:approve_request`, `enterprise:view`
*   **Admin Permissions**: `enterprise:manage_org`, `enterprise:view`
*   **Actions**: Hierarchical procurement workflows within large organizations.

### Government Owner / Auditor
*   **Owner Permissions**: `government:publish_tender`, `government:view`
*   **Auditor Permissions**: `government:view`, `government:audit_tender`, `compliance:view`
*   **Actions**: Transparent tendering and legislative oversight without modification access for auditors.

---

## 3. Core Functional Requirements

### 2.1 Regulated Investment Marketplace

* Investor onboarding + KYC/AML
* Binding project funding commitments
* Escrow-backed deployment of capital
* Investor reporting + protections

---

### 2.2 Enterprise Construction Suite

* Multi-organization accounts
* Procurement approval workflows
* ERP integrations (future)
* SLA-backed supplier performance

### 2.2.1 Enterprise Organization Customization (Administrative Control)

* **Independent Branding**: Enterprise organizations can override platform defaults with their own logos, colors, and identity.
* **Granular Module Enablement**: Admins can toggle specific modules (e.g., Financing vs. Materials Only) for individual organizations.
* **Custom Procurement Rules**: Definitions for internal approval thresholds and compliance checklists.

---

### 2.3 Government Procurement Layer

* Public tender publishing
* Transparent bid evaluation
* Anti-corruption audit trails
* Compliance document handling

---

### 2.4 Compliance & Localization Engine

* Multi-currency settlement
* VAT/tax automation
* Data residency controls
* Jurisdiction-specific rules modules

---

### 2.5 AI Risk + Fraud Engine

* Fraud detection
* Contractor/vendor risk scoring
* Automated compliance checks
  n

---

## 3. Phase 5 Success Metrics

* Institutional funding participation
* Government/enterprise contracts onboarded
* Full escrow audit compliance
* Reduced fraud/dispute rates

---

**Phase 5 requirements are now defined.**
