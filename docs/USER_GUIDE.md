# 📖 User Guide — Procus v2

Welcome to the **Procus v2** User Guide. This document provides step-by-step instructions for each of the primary user roles on the platform.

---

## 📑 Table of Contents
1. [Registering on the Platform](#1-registering-on-the-platform)
2. [Base Workspace: Buyer and Project Owner](#2-base-workspace-buyer-and-project-owner)
3. [Specialized Role: Vendor](#3-specialized-role-vendor)
4. [Specialized Role: Contractor](#4-specialized-role-contractor)
5. [Specialized Role: Property Manager](#5-specialized-role-property-manager)
6. [Core Role: Project Owner](#6-core-role-project-owner)
7. [Specialized Role: Investor](#7-specialized-role-investor)
8. [Role: Admin (Platform Management)](#8-role-admin-platform-management)

---

## 1. Registering on the Platform

1. Navigate to the **Register** page.
2. Enter your email, first name, last name, and a secure password.
3. Click **Create Identity**.
4. Your account starts in the base `PROJECT_OWNER` workspace.
5. Once registered, log in to access the shared workspace and activate specialized workflows only when needed.

### Role Activation Policy

- `PROJECT_OWNER` is the default base role for normal users.
- `VENDOR`, `CONTRACTOR`, `INVESTOR`, `PROPERTY_MANAGER`, `COURIER`, and `GOVERNMENT` are specialized roles.
- Specialized roles should be activated after onboarding and admin approval.
- Users may hold multiple approved non-admin roles.
- `ADMIN` is separate and manually assigned.

---

## 2. Base Workspace: Buyer and Project Owner

Every normal account starts in the shared `PROJECT_OWNER` workspace. In practice, this is also where buyer-style procurement begins.

### 🛒 Browsing and Ordering
1. **Explore Catalogue**: Use the "Materials" section to browse products. Use filters to find exactly what you need (e.g., Cement, Steel, Timber).
2. **View Details**: Click on a product to see description, base price, currency, and availability. The price is shown in your selected country currency, converted from the product's stored source currency.
3. **Add to Order**: Enter the quantity and click **Order Now**.
4. **Checkout**: Review your order summary and confirm the delivery address.

### 🏠 Property Discovery And Lead Capture
1. **Browse Properties**: Use the property marketplace to search by location, asset type, development profile, and estimated value.
2. **Open Property Detail**: Review the asset summary, development metadata, financing options, linked project details, and suggested materials or services.
3. **Make Inquiry**: Public visitors may submit an inquiry without logging in if they provide callback phone number or email.
4. **Schedule Visit**: Choose an available viewing slot from the property calendar when appointment booking is enabled.
5. **Follow-Up**: Property inquiries and appointment requests should trigger notifications and a communication thread so the owner or manager can respond quickly.

### 📦 Tracking and Disputes
1. **Order Dashboard**: Monitor your orders in "My Orders".
2. **Status Tracking**: See when your order moves from `PLACED` to `SHIPPED` to `DELIVERED`.
3. **File Dispute**: If there is an issue with the quality or delivery, use the **Open Dispute** button to freeze the payment until resolved by an admin.

---

## 3. Specialized Role: Vendor

Vendor access is a specialized approved workflow layered onto the base account.

### 🏗️ Product Management
1. **Create Identity**: Register a platform account from the main **Register** page.
2. **Activate Vendor Onboarding**: Open the Vendor Dashboard. If you do not yet have a supplier profile, the dashboard will prompt you to continue to **Vendor Registration** where you submit:
   - business name
   - registration number
   - operating location
   - delivery settings
   - categories served
3. **Wait for Approval**: Your supplier profile remains `PENDING` until an admin approves it. Vendor access should be treated as an approved specialization, not just a self-declared role.
4. **Approved Access**: Once approved, your account can operate the vendor workspace without losing the base buyer-owner workspace.
5. **List Products**: Use the **Inventory** tab to add new materials. Select a real material category, choose the product currency, set unit price, stock quantity, reorder threshold, and publish status.
6. **Bulk Import**: Use **Download Template** to get the CSV format, then use **Import CSV** to bulk-create products and initial stock.
7. **Inventory Ledger**: The inventory view only shows products owned by your vendor profile. Use **Adjust** to add or remove stock with a note and reference.
8. **Movement History**: Use **History** to review inventory commits, restocks, imports, and manual adjustments for each product.
9. **Inventory Updates**: Use **Edit** and **Delete** to maintain your catalog, but prefer stock adjustments for operational quantity changes.

### 🚚 Order Fulfillment
1. **Incoming Orders**: View new orders in your "Vendor Management" console.
2. **Status Updates**: As you process the order, move the status through `CONFIRMED`, `PACKING`, `SHIPPED`, and `DELIVERED`.
3. **Delivery Estimate**: When confirming an order, enter the estimated delivery date so the buyer can track the commitment window.
4. **Fulfillment Rate**: Your reputation as a vendor is tracked by your fulfillment rate and delivery timeliness.

---

## 4. Specialized Role: Contractor

Contractors are verified service providers who bid on construction tenders.

### 🛡️ Getting Verified
1. **Activate Contractor Onboarding**: Open the contractor workspace and fill out the Contractor Registration form.
2. **Certifications**: Upload your licenses and certifications.
3. **Admin Review**: Wait for a platform admin to verify your credentials. Contractor access should be treated as an approved specialization, and you should not bid until verified.

### 🔨 Bidding and Execution
1. **Find Tenders**: Browse the "Contracts" marketplace for posted tenders.
2. **Submit Bid**: Enter your proposed cost and timeline.
3. **Winning Jobs**: If a Project Owner awards you the contract, it will appear in your "Active Jobs".
4. **Milestones**: Complete work according to the defined milestones. Once an owner approves a milestone, funds are released to you.

---

## 5. Specialized Role: Property Manager

Property managers operate standalone property assets inside the platform while preserving links to finance, project creation, and downstream procurement.

### 🏢 Property Operations
1. **Activate Property Manager Onboarding**: Open the property workspace and complete the onboarding flow to be approved as a `PROPERTY_MANAGER`.
2. **List Properties**: Create and manage listings for land, residential, commercial, industrial, mixed-use, hospitality, renovation, and completed-project assets. Set the pricing currency on the listing so the platform can convert the displayed price into the selected country currency.
3. **Define Availability**: Configure viewing slots so visitors can book visits from the property calendar.
4. **Handle Inquiries**: Respond to public and authenticated inquiries from the property detail page.
5. **Enable Finance**: Mark properties as financing-eligible where acquisition, renovation, or completion finance should be offered.
6. **Link To Projects**: Convert or connect a development opportunity into a platform project when procurement, contracts, and execution need to be formalized.

## 6. Core Role: Project Owner

`PROJECT_OWNER` is the base role for new normal users and remains the anchor workspace even when the user later gains more approved roles.

### 🧭 Owner Workspace
1. Open `/owner/dashboard` to reach the Project Control Center.
2. Use **Start New Project** to open `/projects/new`.
3. Use **Post a Tender** to open `/contracts/new`.
4. Keep projects and contracts separate in the UI: projects are the execution record, contracts are the procurement record.

### 🏗️ Creating a Project
1. **Set Up Project**: Define your project (name, location, budget).
2. **Link Property When Needed**: Connect the project to a property if the site or completed asset should stay visible inside the property marketplace.
3. **Start From Property Or Project**: A project owner may begin with a property opportunity first or create a project directly and link the property later.
4. **Requirements (BoQ)**: Add the materials and services you need (e.g., "500 Bags of Cement", "Plumbing Services").
5. **Post Tenders**: Create a tender for the services required.

### 🤝 Hiring and Paying
1. **Review Bids**: Compare bids from different contractors. Look at their reliability scores and past reviews.
2. **Award Contract**: Select the best bid to start the work.
3. **Escrow Funding**: Deposit project funds into the secure Escrow account.
4. **Finance Either Path**: Financing may support property acquisition/completion or project completion depending on how the opportunity is structured.
5. **Approve Work**: As the contractor completes milestones, review the work and click **Approve**. This automatically triggers the payment release from escrow.

## 7. Specialized Role: Investor

Investors provide capital to construction projects, material orders, and property developments in exchange for structured returns or equity stakes.

> **Full Reference**: See [`INVESTOR_GUIDE.md`](./INVESTOR_GUIDE.md) for the complete investor documentation.

### 📈 Investing

1. **Activate Investor Onboarding**
   - Open the investor workspace and request the `INVESTOR` role.
   - Complete KYC verification: upload government-issued ID and proof of address.
   - Wait for admin review. Status: `PENDING → VERIFIED`.
   - (Optional) Apply for accredited investor status for large commitments.

2. **Project Discovery**
   - Browse **Projects** (`/projects`) and filter by **"Seeking Investment"**.
   - Evaluate projects using the funding progress bar, budget gap, requirements list, and linked contracts.
   - Review owner track record, timeline, and location risk before pledging.

3. **Pledge Capital**
   - Open a fundable project detail page.
   - Enter your pledge amount in the **Funding & Investment** sidebar.
   - Click **Pledge Commitment**.
   - Your pledge is non-binding at this stage (`PLEDGED` status).

4. **Confirm Commitment**
   - After discussing terms with the project owner, confirm your pledge.
   - Funds transfer to a dedicated escrow account.
   - Status moves: `PLEDGED → CONFIRMED`.

5. **Sign Agreement**
   - Review the legally binding `InvestmentAgreement` generated by the platform.
   - Click **Execute Sign** in your Investor Dashboard.
   - Agreement status: `DRAFT → SIGNED → FUNDED`.

### 🔄 Secondary Market

1. **Manage Stakes**: View your portfolio at `/investor/dashboard` under **Portfolio Vital**.
2. **List for Sale**: Go to `/market/secondary`, select a stake, set asking price and yield.
3. **Buy Stakes**: Browse listings, review project status and seller history, confirm purchase.
4. **Settlement**: Platform validates compliance, executes transfer, and releases funds.

> **Limitation**: No open public trading. All transfers are OTC with platform oversight.

### 💰 Returns & Distributions

- **Milestone-linked**: Receive distributions as project milestones are approved.
- **Completion-based**: Full payout when project reaches `COMPLETED` status.
- **Revenue share**: Periodic distributions based on project revenue.
- Distributions flow from escrow → your linked bank account via `SettlementTransaction`.

### ⚠️ Risk Summary

- Construction projects carry inherent cost overrun, delay, and contractor failure risks.
- The platform facilitates escrow but does not guarantee returns.
- Investments are illiquid until project completion or secondary market sale.
- Diversify across multiple projects and start with smaller commitments.

> **See [`INVESTOR_GUIDE.md`](./INVESTOR_GUIDE.md) for full risk disclosure, FAQ, and detailed workflows.**

---

## 8. Role: Admin (Platform Management)

Admins oversee the health and regulatory compliance of the entire ecosystem.

### 🔬 Operational Oversight
1. **Audit Logs**: Monitor the `AUDIT_LOG_STREAM` to review recorded platform actions.
2. **Security Monitoring**: Review throttling and access-scope violations from the security module.
3. **Verifications**: Contractor verification is currently surfaced in the admin dashboard. Vendor verification and investor KYC review are not yet fully exposed there.
4. **Dispute Resolution**: Backend dispute resolution exists, but the dedicated admin dispute workspace is not yet available in the dashboard UI.

### ⚙️ System Configuration
1. **Platform Identity**: Update branding, contact info, and default regions.
2. **Currencies**: Manage exchange rates and active currencies relative to KES as the platform reference currency. The UI converts displayed money into the selected country's currency using the stored source currency on each record.
   The default rate sync provider is Frankfurter, with ExchangeRate-API available as a fallback that admins can switch to in settings.
3. **Countries**: Manage active operating countries and choose the default country. Selecting a country should automatically resolve its local currency in the UI and drive currency selection in create forms.
4. **Roles and Users**: Activate users, reassign roles, and manage Django groups through settings tools.
   Treat specialized roles as approval outcomes where possible, rather than arbitrary self-service profile values.
5. **Approval Discipline**: Normal users may hold multiple approved non-admin roles. `ADMIN` should remain a separate operator identity.
6. **Taxonomy**: Manage the categories for products and services (Material, Service, Project types).

### 📌 Current Admin Reality

The admin dashboard is partially operational today.

Strongest admin surfaces:

- system configuration
- currencies
- countries
- taxonomy
- security monitoring
- audit logs
- property registry visibility
- regulatory reports surface

Still incomplete:

- vendor verification in admin dashboard
- investor KYC review in admin dashboard
- dispute arbitration UI
- full operator management in the dedicated admin panel

For a code-accurate admin reference, use `docs/ADMIN_FUNCTIONALITY_STATUS.md`.

---

*Procus v2 — Empowering the Construction Ecosystem.*
