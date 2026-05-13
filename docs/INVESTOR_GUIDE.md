# 📈 Investor Guide — Procus v2

> Complete guide for capital providers funding construction projects and material procurement through the Procus platform.

---

## 📑 Table of Contents

1. [Getting Started as an Investor](#1-getting-started-as-an-investor)
2. [Understanding Investment Types](#2-understanding-investment-types)
3. [Project Discovery & Evaluation](#3-project-discovery--evaluation)
4. [The Pledge & Commitment Flow](#4-the-pledge--commitment-flow)
5. [Escrow & Capital Protection](#5-escrow--capital-protection)
6. [Investment Agreements & Legal](#6-investment-agreements--legal)
7. [Portfolio Management](#7-portfolio-management)
8. [Returns & Distributions](#8-returns--distributions)
9. [Secondary Market](#9-secondary-market)
10. [Risk Disclosure](#10-risk-disclosure)
11. [FAQ](#11-faq)

---

## 1. Getting Started as an Investor

### 1.1 Role Activation

1. Register a platform account at `/register` (defaults to `PROJECT_OWNER`).
2. Navigate to the **Investor Workspace** and request the `INVESTOR` role activation.
3. Complete the **KYC Verification** workflow:
   - Upload government-issued ID or passport
   - Provide proof of address (utility bill or bank statement)
   - Submit jurisdiction of residence
4. Wait for admin review. KYC status moves: `PENDING → VERIFIED` or `REJECTED`.
5. (Optional) Apply for **Accredited Investor** status if your jurisdiction requires it for large commitments.

> **Note**: You may hold multiple roles. Many investors also operate as `PROJECT_OWNER` to initiate their own developments.

### 1.2 Your Investor Dashboard

Access your dashboard at `/investor/dashboard`.

**Sections:**
- **Portfolio Vital**: Total capital committed, active project nodes, compliance status
- **Agreement Logs**: All signed and pending investment agreements
- **Compliance Vault**: KYC status, accreditation level, jurisdiction settings

---

## 2. Understanding Investment Types

### 2.1 Project Equity / Completion Finance

Invest capital into a construction project in exchange for a stake or structured return.

| Attribute | Description |
|-----------|-------------|
| Target | `Project` entity with `funding_required=true` |
| Return Type | Revenue share, fixed yield, or equity stake |
| Duration | Tied to project timeline (start → completion) |
| Risk Level | Medium–High (construction risk, market risk) |
| Minimum Pledge | Set by project owner |

### 2.2 Material Procurement Finance

Fund material orders for buyers who need credit to purchase construction supplies.

| Attribute | Description |
|-----------|-------------|
| Target | `Order` or `QuoteRequest` via `FinanceApplication` |
| Return Type | Interest on loan principal |
| Duration | Short-term (30–90 days typical) |
| Risk Level | Lower (shorter duration, order-backed) |
| Collateral | Order value + buyer transaction history |

### 2.3 Property Acquisition / Renovation Finance

Finance property purchases or renovations listed on the property marketplace.

| Attribute | Description |
|-----------|-------------|
| Target | `PropertyListing` with `financing_allowed=true` |
| Return Type | Mortgage-style interest or profit share on resale |
| Duration | Medium-term (6–24 months) |
| Risk Level | Medium (property market risk) |

### 2.4 Contractor Working Capital

Provide working capital loans to verified contractors.

| Attribute | Description |
|-----------|-------------|
| Target | `Contractor` profile with reliability score |
| Return Type | Interest on loan |
| Duration | Short-term (aligned to contract milestones) |
| Risk Level | Medium (contractor credit scoring applies) |

---

## 3. Project Discovery & Evaluation

### 3.1 Finding Fundable Projects

1. Navigate to **Projects** (`/projects`).
2. Apply the **"Seeking Investment"** filter to show only projects with `funding_required=true`.
3. Review project cards for:
   - **Budget**: Estimated total vs. amount already pledged
   - **Location**: Construction site geography
   - **Status**: `LISTED` (planning) or `FUNDING_OPEN` (actively raising)
   - **Requirements**: Materials and services needed (BoQ preview)
   - **Linked Contracts**: Whether procurement has begun

### 3.2 Evaluation Checklist

Before pledging, review the project detail page for:

| Factor | What to Look For |
|--------|------------------|
| Owner Track Record | Past projects, completion rate, ratings |
| Budget Realism | Does estimated budget align with requirements? |
| Funding Gap | `estimated_budget` minus total committed |
| Timeline | Start date, end date, milestone structure |
| Contracts | Are tenders posted? Any bids received? |
| Location Risk | Jurisdiction, access, permits status |
| Updates Feed | Is the owner actively communicating progress? |

> **Tip**: Projects with status `FUNDING_OPEN` and active tender postings indicate serious execution intent.

### 3.3 Understanding the Funding Progress Bar

The project card shows a visual progress bar:

```
[████████░░░░░░░░░░] 35% funded
KES 3,500,000 pledged of KES 10,000,000 budget
```

- **Green zone** (>75%): Project likely to reach funding target
- **Yellow zone** (25–75%): Moderate funding momentum
- **Red zone** (<25%): Early stage or low interest

---

## 4. The Pledge & Commitment Flow

### 4.1 Making a Pledge

1. Open a fundable project detail page.
2. In the **Funding & Investment** sidebar panel, enter your pledge amount.
3. Click **Pledge Commitment**.

**Validation Rules:**
- Amount must be positive
- Project must have `funding_required=true`
- Total committed + your pledge cannot exceed `estimated_budget`
- You cannot pledge more than once per project (update existing pledge instead)

**Status Flow:**
```
You submit pledge
    ↓
InvestmentCommitment created with status: PLEDGED
    ↓
Project owner reviews commitments
    ↓
Owner may contact you via platform chat
    ↓
When ready, you CONFIRM the pledge (funds transfer)
    ↓
Status moves: PLEDGED → CONFIRMED
```

### 4.2 Pledge vs. Confirmed Commitment

| Stage | Money Transferred? | Binding? | Reversible? |
|-------|-------------------|----------|-------------|
| `PLEDGED` | No | No (expression of interest) | Yes, cancel anytime |
| `CONFIRMED` | Yes (to escrow) | Yes | Only by mutual agreement or dispute |

> **Important**: A `PLEDGED` status is non-binding. The project owner may reach out to discuss terms before you confirm. Only `CONFIRMED` commitments trigger escrow account creation and capital deployment.

### 4.3 Cancelling a Pledge

You may cancel a `PLEDGED` commitment at any time from your Investor Dashboard:
1. Go to **Agreement Logs**
2. Find the pending pledge
3. Click **Withdraw Commitment**

Cancelled pledges free up budget capacity for other investors.

---

## 5. Escrow & Capital Protection

### 5.1 How Escrow Protects Your Investment

When your commitment reaches `CONFIRMED` status:

1. **Escrow Account Created**: A dedicated escrow account is linked to the project's contract(s).
2. **Funds Held**: Your capital sits in escrow, not directly with the contractor or project owner.
3. **Milestone-Linked Release**: Funds are released only when:
   - Contractor marks a milestone as `COMPLETED`
   - Project owner `APPROVES` the milestone
   - No active dispute holds exist on the escrow account

### 5.2 Escrow States

| State | Meaning |
|-------|---------|
| `ACTIVE` | Funds secured, releases possible |
| `RELEASED` | All funds distributed per milestones |
| `CLOSED` | Account settled, no further transactions |

### 5.3 Dispute Freeze

If a dispute is filed on a contract:
- An `EscrowHold` is automatically created
- All fund releases are blocked until the dispute is resolved
- Admin arbitrates: may order refund to investors or release to contractor

> **Your Protection**: Disputes freeze capital, preventing unilateral withdrawals while arbitration occurs.

### 5.4 Viewing Escrow Status

From your Investor Dashboard:
- **Agreement Logs** → click any confirmed agreement
- View escrow balance, transaction history, and pending releases

---

## 6. Investment Agreements & Legal

### 6.1 The Agreement Lifecycle

```
DRAFT (platform generates agreement)
    ↓
SIGNED (you review and sign digitally)
    ↓
FUNDED (escrow receives capital)
    ↓
ACTIVE (project execution)
    ↓
COMPLETED / CANCELLED
```

### 6.2 Signing an Agreement

1. After pledging, the project owner may initiate an `InvestmentAgreement`.
2. You receive a notification: "Agreement ready for signature."
3. Review the agreement terms document (PDF link).
4. Click **Execute Sign** in your Investor Dashboard.
5. Agreement status moves: `DRAFT → SIGNED`.

### 6.3 Agreement Contents

Standard agreements include:
- Investment amount and currency
- Project details and timeline
- Return structure (yield %, revenue share %, or equity %)
- Risk disclosure acknowledgment
- Dispute resolution clause
- Jurisdiction and governing law

> **Warning**: Read every agreement before signing. Platform provides the framework, but terms are set by project owners. Seek independent legal advice for large commitments.

---

## 7. Portfolio Management

### 7.1 Your Portfolio Overview

The **Portfolio Vital** section displays:

| Metric | Description |
|--------|-------------|
| Total Capital Committed | Sum of all confirmed investments |
| Active Project Nodes | Number of projects you have stakes in |
| Pending Pledges | Non-binding pledges awaiting confirmation |
| Avg. Yield | Weighted average of projected returns |
| Compliance Status | KYC and accreditation standing |

### 7.2 Tracking Individual Investments

Each investment card shows:
- Project name and status
- Amount invested
- Current project phase (`LISTED` / `FUNDING_OPEN` / `EXECUTION_STARTED` / `COMPLETED`)
- Milestone progress (X of Y approved)
- Next expected action (e.g., "Milestone 2 pending contractor completion")

### 7.3 Investor Reports

When available, project owners may publish periodic `InvestorReport` documents:
- Reporting period (e.g., "Q1 2026")
- Performance summary (work completed, budget spent vs. planned)
- Photo updates from site
- Risk alerts or timeline changes

Access reports from the project detail page or your dashboard.

---

## 8. Returns & Distributions

### 8.1 When Do You Get Paid Back?

Return timing depends on the investment structure:

| Structure | Payout Trigger |
|-----------|---------------|
| Milestone-linked | Each approved milestone releases a portion |
| Completion-based | Full payout on project `COMPLETED` status |
| Revenue share | Periodic distributions based on project revenue |
| Fixed yield | Principal + interest at end of term |

### 8.2 Distribution Flow

1. Milestone approved → escrow release triggered
2. Funds move from escrow to your platform-linked bank account
3. `SettlementTransaction` record created for audit
4. You receive notification: "Distribution received: KES XXXXX"

### 8.3 Tax Considerations

- The platform does not withhold taxes.
- You are responsible for reporting investment income in your jurisdiction.
- Use **Regulatory Reports** (if available in your region) for tax filing support.

---

## 9. Secondary Market

### 9.1 What Is the Secondary Market?

The secondary market allows you to sell your investment stakes to other approved investors before the project completes — providing liquidity without waiting for full project maturity.

### 9.2 Listing a Stake for Sale

1. Go to **Secondary Market** (`/market/secondary`).
2. Click **Sell Stake**.
3. Select the project stake you wish to sell.
4. Set:
   - **Volume**: Amount of stake to sell
   - **Asking Price**: What you want to receive
   - **Target Yield**: Advertised yield for the buyer
5. Submit listing. Status: `REQUESTED`.

### 9.3 Buying a Stake

1. Browse active listings on the Secondary Market.
2. Review stake details: project status, seller history, yield.
3. Click **Buy Stake**.
4. Confirm purchase. Funds enter escrow until ownership transfer completes.

### 9.4 Settlement & Transfer

1. Platform validates compliance (accreditation, jurisdiction rules).
2. Admin/regulator approval (if required by jurisdiction).
3. `StakeTransfer` executed: ownership moves from seller to buyer.
4. Funds released to seller's bank account.

> **Limitations**: No open public trading. No tokenization unless explicitly regulated in your jurisdiction. All transfers are over-the-counter with platform oversight.

---

## 10. Risk Disclosure

### 10.1 Construction Risk

Construction projects face inherent risks:
- **Cost overruns**: Budget may exceed estimates
- **Delays**: Weather, permits, or supply chain issues
- **Contractor failure**: Contractor may abandon work or underperform
- **Market changes**: Property values may fluctuate

### 10.2 Platform Risk

- The platform facilitates matching and escrow but does not guarantee returns.
- Payment gateway integration is in progressive rollout (M-Pesa, Stripe, Flutterwave).
- KYC verification reduces fraud risk but does not eliminate it.

### 10.3 Liquidity Risk

- Primary investments are illiquid until project completion.
- Secondary market availability depends on buyer demand and regulatory approval.
- Early exit may require selling at a discount.

### 10.4 Mitigation Strategies

| Strategy | How to Apply |
|----------|--------------|
| Diversification | Spread capital across multiple projects and types |
| Due Diligence | Review owner history, budget realism, and location |
| Escrow Verification | Confirm escrow account exists before confirming pledges |
| Milestone Monitoring | Track contractor progress via milestone updates |
| Start Small | Test the platform with smaller commitments first |

---

## 11. FAQ

**Q: Can I invest if I am not accredited?**
A: Yes for smaller pledges. Some jurisdictions or large projects may require accreditation. Check the project detail page for requirements.

**Q: What happens if a project fails to reach its funding target?**
A: `PLEDGED` commitments are automatically released. `CONFIRMED` commitments remain in escrow until the owner cancels the project or restructures terms.

**Q: How do I link my bank account for distributions?**
A: Go to **Settings → Bank Accounts** and add your account details. The platform supports local rails (M-Pesa) and international transfers.

**Q: Can I invest in multiple projects?**
A: Yes. There is no limit on the number of projects you can pledge to or confirm.

**Q: Who do I contact for support?**
A: Use the in-platform chat or email support. For disputes, use the **Open Dispute** button on the relevant project or contract.

**Q: Is my capital insured?**
A: No. This is investment, not a deposit product. Capital is at risk. Escrow protects against misappropriation but does not guarantee against project failure.

---

*Procus v2 — Construction Capital, Democratized.*
