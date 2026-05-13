# 🏗️ Material Financing Guide — Procus v2

> Guide for buyers, vendors, and contractors seeking credit for construction material procurement.

---

## 📑 Table of Contents

1. [Overview](#1-overview)
2. [Who Can Apply](#2-who-can-apply)
3. [Finance Product Types](#3-finance-product-types)
4. [Application Workflow](#4-application-workflow)
5. [Repayment](#5-repayment)
6. [Supplier Credit Lines](#6-supplier-credit-lines)
7. [For Vendors: Offering Credit](#7-for-vendors-offering-credit)
8. [Risk & Eligibility](#8-risk--eligibility)
9. [FAQ](#9-faq)

---

## 1. Overview

Construction projects often require materials before payment is received. Procus provides embedded financing options to bridge this gap:

- **Buyer Material Credit**: Buyers can finance material orders and pay over time
- **Vendor Working Capital**: Suppliers can access credit to stock inventory
- **Contractor Procurement Loans**: Contractors can finance materials for active jobs

---

## 2. Who Can Apply

| Role | Financing Type | Minimum Requirements |
|------|---------------|---------------------|
| **Buyer** | Material Order Credit | Verified account, 2+ completed orders, no open disputes |
| **Vendor** | Working Capital / Inventory Credit | Approved vendor profile, 90+ days on platform, fulfillment rate >80% |
| **Contractor** | Procurement Loan | Verified contractor profile, active awarded contract, reliability score >60 |

> **Note**: First-time users typically cannot access financing. Build transaction history to qualify.

---

## 3. Finance Product Types

### 3.1 Material Order Credit (Buyers)

Finance a specific material order instead of paying upfront.

| Attribute | Details |
|-----------|---------|
| Target | `MATERIAL_ORDER` |
| Purpose | `MATERIALS_PROCUREMENT` |
| Max Amount | Up to 80% of order value (platform/product dependent) |
| Term | 30–90 days |
| Interest | Set per product (e.g., 1.5% monthly) |
| Repayment | Single bullet or 2–3 instalments |

**Use Case**: You need 500 bags of cement for a job starting next week. You don't have cash on hand. Apply for material credit at checkout.

### 3.2 Working Capital (Vendors)

Stock inventory in advance of confirmed orders.

| Attribute | Details |
|-----------|---------|
| Target | `GENERAL_WORKING_CAPITAL` |
| Purpose | `WORKING_CAPITAL` |
| Max Amount | Product-dependent (up to KES 500,000 for starter tier) |
| Term | 60–180 days |
| Interest | 5–15% annual rate |
| Collateral | Inventory + sales history |

### 3.3 Contractor Procurement Loan

Finance materials for an active construction contract.

| Attribute | Details |
|-----------|---------|
| Target | `CONTRACT` |
| Purpose | `MATERIALS_PROCUREMENT` |
| Max Amount | Up to contract value × 0.4 |
| Term | Aligned to contract milestones |
| Interest | 2–3% monthly |
| Collateral | Contract value + milestone payments |

### 3.4 Property-Linked Finance

Finance materials for property renovation or completion.

| Attribute | Details |
|-----------|---------|
| Target | `PROPERTY` |
| Purpose | `RENOVATION` or `COMPLETION` |
| Max Amount | Up to property value estimate × 0.3 |
| Term | 6–24 months |

---

## 4. Application Workflow

### 4.1 Step-by-Step Application

1. **Navigate to Finance Portal**
   - Buyers: At checkout, select **"Apply for Credit"**
   - Vendors/Contractors: From dashboard, click **"Apply for Financing"**

2. **Select Product**
   - Browse active `FinanceProduct` listings
   - Compare interest rates, max amounts, and terms

3. **Specify Target**
   - Link to an existing `Order`, `Contract`, or `PropertyListing`
   - Or apply for general working capital

4. **Enter Amount & Purpose**
   - Requested amount (cannot exceed product max)
   - Detailed purpose description
   - Purpose category (e.g., `MATERIALS_PROCUREMENT`)

5. **Submit Application**
   - Platform evaluates your credit score
   - Review takes 1–3 business days

### 4.2 Application Status Flow

```
SUBMITTED
    ↓
UNDER REVIEW (platform scoring + manual check)
    ↓
APPROVED → Loan account created → Funds disbursed
    ↓
REJECTED → Reason provided → Re-apply in 30 days
```

### 4.3 Credit Scoring Inputs

The platform evaluates:

| Factor | Weight | Description |
|--------|--------|-------------|
| Transaction History | 40% | Order volume, payment reliability |
| Dispute Rate | 30% | Frequency of conflicts |
| Platform Tenure | 20% | Time active, profile completeness |
| Ratings | 10% | Partner feedback scores |

> **Tip**: Maintain a clean record — pay orders on time, avoid disputes, and keep your profile updated.

---

## 5. Repayment

### 5.1 Loan Account

Once approved, a `FinanceLoan` is created:
- `principal_amount`: Approved loan value
- `disbursed_amount`: Amount actually sent (may be staged)
- `repayment_due_date`: Final payment deadline
- `status`: `ACTIVE` until fully repaid

### 5.2 Repayment Methods

| Method | How It Works |
|--------|--------------|
| **Auto-Debit** | Link M-Pesa or bank account for automatic monthly deductions |
| **Manual Payment** | Pay via platform using supported gateway |
| **Milestone Offset** | For contractor loans: repay from contract milestone releases |
| **Order Settlement** | For vendor credit: repay from order revenue automatically |

### 5.3 Early Repayment

You may repay early without penalty on most products. Early repayment improves your credit score for future applications.

### 5.4 Default Consequences

| Stage | Action |
|-------|--------|
| 7 days late | Reminder notification |
| 14 days late | Credit score penalty, platform flag |
| 30 days late | Account suspended, collections initiated |
| 60 days late | Legal action, credit bureau reporting (where applicable) |

---

## 6. Supplier Credit Lines

### 6.1 What Is a Supplier Credit Line?

Pre-approved credit extended to verified vendors for inventory stocking.

| Feature | Details |
|---------|---------|
| Credit Limit | Platform-assigned based on sales history |
| Available Balance | Real-time remaining credit |
| Drawdown | Automatic when stocking inventory |
| Repayment | Automatic from order settlements |

### 6.2 How It Works

1. Vendor receives approved credit line (e.g., KES 200,000).
2. Vendor stocks inventory using credit line funds.
3. When orders come in, revenue first repays the credit line.
4. Available balance replenishes as repayments clear.

### 6.3 Status

| Status | Meaning |
|--------|---------|
| `ACTIVE` | Credit available, drawdowns permitted |
| `SUSPENDED` | Drawdowns blocked, repayments still required |

---

## 7. For Vendors: Offering Credit

### 7.1 Buy-Now-Pay-Later for Your Customers

As a vendor, you can offer material credit to your buyers:

1. Enable **"Offer Financing"** in your vendor settings.
2. Set maximum credit per buyer tier.
3. Platform handles underwriting and collection.
4. You receive full payment upfront from the financing partner.

### 7.2 Benefits

- Close more sales (buyers don't need cash upfront)
- Get paid immediately (platform finances the buyer)
- Reduced default risk (platform bears credit risk)

---

## 8. Risk & Eligibility

### 8.1 Eligibility Criteria

| Requirement | Buyer | Vendor | Contractor |
|-------------|-------|--------|------------|
| Account verified | ✅ | ✅ | ✅ |
| Platform tenure | 30+ days | 90+ days | 60+ days |
| Completed transactions | 2+ orders | 10+ orders | 1+ contract |
| Dispute rate | <10% | <5% | <5% |
| Reliability score | N/A | >70 | >60 |

### 8.2 Rejection Reasons

Common reasons for rejection:
- Insufficient transaction history
- High dispute rate
- Existing overdue loan
- Application amount exceeds product max
- Target project/contract not found or ineligible

---

## 9. FAQ

**Q: Can I apply for financing before placing an order?**
A: Yes for working capital and contractor loans. For material order credit, you typically apply at checkout.

**Q: What currencies are supported?**
A: KES, USD, EUR. Local financing defaults to KES.

**Q: How long does approval take?**
A: 1–3 business days for standard applications. Instant for pre-approved credit lines.

**Q: Can I have multiple active loans?**
A: Yes, subject to total exposure limits based on your credit score.

**Q: What happens if my contract is cancelled?**
A: Contractor procurement loans may be recalled or restructured. Contact platform support immediately.

**Q: Is there a grace period?**
A: Most products offer a 3-day grace period before late fees apply.

---

*Procus v2 — Construction Materials, Unlocked.*
