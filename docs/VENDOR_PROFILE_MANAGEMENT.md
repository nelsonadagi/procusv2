# Vendor Profile Management - Complete Guide

## 📍 **Where Vendors Manage Their Profile**

**Answer**: Vendors manage their profile in the **Vendor Dashboard** under the **"My Profile"** tab.

**Access Path:**
```
Register account as VENDOR → Login → Vendor Dashboard
If no vendor profile exists: Vendor Dashboard → Complete onboarding → /vendors/register
If vendor profile exists: Vendor Dashboard → 👤 My Profile Tab
```

---

## 🎯 **Features Added**

### **1. Tabbed Dashboard Interface**

The Vendor Dashboard now has **3 main tabs** once onboarding is complete:

```
┌──────────────────────────────────────────────┐
│ 👤 My Profile  │  📦 Inventory  │  📋 Orders │
└──────────────────────────────────────────────┘
```

| Tab | Description |
|-----|-------------|
| **👤 My Profile** | View and edit business information, see verification status, view performance metrics |
| **📦 Inventory** | Manage products (existing functionality) |
| **📋 Orders** | Order management (placeholder for future) |

---

## 👤 **My Profile Tab - Features**

### **Verification Status Banner**

Shows current vendor verification status with color-coded banners:

#### **PENDING** (Orange)
```
┌─────────────────────────────────────────────┐
│ ⏳ Verification Status: PENDING              │
│ Your application is under review. You'll be │
│ notified once approved.                     │
└─────────────────────────────────────────────┘
```

#### **APPROVED** (Green)
```
┌─────────────────────────────────────────────┐
│ ✓ Verification Status: APPROVED             │
│ Your vendor account is verified and active! │
└─────────────────────────────────────────────┘
```

#### **REJECTED** (Red)
```
┌─────────────────────────────────────────────┐
│ ✗ Verification Status: REJECTED             │
│ Your application was not approved. Please   │
│ contact support.                            │
└─────────────────────────────────────────────┘
```

#### **SUSPENDED** (Pink)
```
┌─────────────────────────────────────────────┐
│ ⚠️ Verification Status: SUSPENDED           │
│ Your account has been suspended. Contact    │
│ support for assistance.                     │
└─────────────────────────────────────────────┘
```

---

### **Business Information Section**

Vendors can view and edit:

| Field | Editable | Required | Description |
|-------|----------|----------|-------------|
| **Business Name** | ✅ Yes | ✅ Yes | Company/business name |
| **Registration Number** | ✅ Yes | ✅ Yes | Business registration number |
| **Location** | ✅ Yes | ✅ Yes | City, Country |
| **Categories Served** | ✅ Yes | ❌ No | Comma-separated categories (e.g., Cement, Steel, Bricks) |

**Example:**
```
Business Name: ABC Construction Supplies
Registration Number: BN123456
Location: Nairobi, Kenya
Categories Served: Cement, Steel, Bricks, Tiles
```

---

### **Account Information Section** (Read-Only)

Displays non-editable account details:

| Field | Value |
|-------|-------|
| **Username** | john_vendor |
| **Email** | john@example.com |

---

### **Performance Metrics Section** (Read-Only)

Shows vendor performance statistics in a beautiful grid:

```
┌──────────────────┬──────────────────┬──────────────────┬──────────────────┐
│ Fulfillment Rate │ Cancellation Rate│ Delivery         │ Average Rating   │
│                  │                  │ Timeliness       │                  │
│      95.5%       │      2.3%        │      98.0%       │   4.8 ⭐         │
│                  │                  │                  │  (124 reviews)   │
└──────────────────┴──────────────────┴──────────────────┴──────────────────┘
```

**Metrics Explained:**

| Metric | Description |
|--------|-------------|
| **Fulfillment Rate** | % of orders successfully fulfilled |
| **Cancellation Rate** | % of orders cancelled |
| **Delivery Timeliness** | % of orders delivered on time |
| **Average Rating** | Average customer rating (1-5 stars) |
| **Total Reviews** | Number of customer reviews |

---

## ✏️ **Editing Profile**

### **How to Edit:**

1. **Navigate to Profile Tab**
   ```
   Vendor Dashboard → 👤 My Profile
   ```

2. **Click "Edit Profile" Button**
   ```
   ┌─────────────────────────────────────┐
   │ Business Profile    [✏️ Edit Profile]│
   └─────────────────────────────────────┘
   ```

3. **Form Fields Become Editable**
   - All input fields unlock
   - Categories can be edited as comma-separated text

4. **Make Changes**
   - Update business name
   - Update registration number
   - Update location
   - Update categories (e.g., "Cement, Steel, Bricks, Tiles")

5. **Save or Cancel**
   ```
   [Cancel]  [💾 Save Changes]
   ```

### **What Vendors CAN Edit:**
- ✅ Business Name
- ✅ Registration Number
- ✅ Location
- ✅ Categories Served

### **What Vendors CANNOT Edit:**
- ❌ Verification Status (admin-only)
- ❌ Username
- ❌ Email
- ❌ Performance Metrics (auto-calculated)

---

## 🔄 **Profile Update Flow**

```
1. Vendor clicks "Edit Profile"
           ↓
2. Form fields become editable
           ↓
3. Vendor updates information
           ↓
4. Vendor clicks "Save Changes"
           ↓
5. API Call: PATCH /vendors/{id}/
           ↓
6. Success message displayed
           ↓
7. Profile refreshed with new data
           ↓
8. Edit mode disabled
```

---

## 🔐 **Security & Permissions**

### **Vendor Profile Update Rules:**

1. **Vendors can update:**
   - ✅ Their own business information
   - ✅ Business name, registration number, location
   - ✅ Categories served

2. **Vendors CANNOT update:**
   - ❌ `verified_status` (protected by backend)
   - ❌ Performance metrics (auto-calculated)
   - ❌ Other vendors' profiles

3. **Backend Protection:**
   ```python
   def perform_update(self, serializer):
       if not self.request.user.is_staff:
           # Remove verified_status from validated_data
           if 'verified_status' in serializer.validated_data:
               serializer.validated_data.pop('verified_status')
       serializer.save()
   ```

---

## 🧭 **Onboarding State**

If a user has selected the `VENDOR` role but has not yet created a vendor profile:

1. The Vendor Dashboard shows an onboarding-required state.
2. The primary action routes to `/vendors/register`.
3. The registration form submits `POST /api/vendors/`.
4. The created profile starts in `PENDING` status until admin approval.

---

## 📊 **Profile Display Modes**

### **View Mode** (Default)
```
┌─────────────────────────────────────────┐
│ Business Profile    [✏️ Edit Profile]   │
├─────────────────────────────────────────┤
│ Business Name: ABC Construction Supplies│
│ Registration Number: BN123456           │
│ Location: Nairobi, Kenya                │
│ Categories: [Cement] [Steel] [Bricks]   │
└─────────────────────────────────────────┘
```

### **Edit Mode**
```
┌─────────────────────────────────────────┐
│ Business Profile                        │
├─────────────────────────────────────────┤
│ Business Name: [ABC Construction...]   │
│ Registration Number: [BN123456]         │
│ Location: [Nairobi, Kenya]              │
│ Categories: [Cement, Steel, Bricks]     │
│                                         │
│              [Cancel] [💾 Save Changes] │
└─────────────────────────────────────────┘
```

---

## 🎨 **UI/UX Features**

### **1. Status-Based Color Coding**
- **PENDING**: Orange background (#fff3e0)
- **APPROVED**: Green background (#e8f5e9)
- **REJECTED**: Red background (#ffebee)
- **SUSPENDED**: Pink background (#fce4ec)

### **2. Category Tags**
Categories are displayed as colorful tags:
```
[Cement] [Steel] [Bricks] [Tiles]
```

### **3. Gradient Metric Cards**
Performance metrics use beautiful gradient backgrounds:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### **4. Loading States**
Spinner animation while fetching profile:
```
    ⟳
Loading profile...
```

### **5. Form Validation**
- Required fields marked with red asterisk (*)
- Helpful hints below inputs
- Character counters where applicable

---

## 🔧 **API Integration**

### **Fetch Vendor Profile**
```http
GET /api/vendors/me/
Authorization: Token <vendor_token>
```

**Response:**
```json
{
  "id": 5,
  "username": "john_vendor",
  "email": "john@example.com",
  "business_name": "ABC Construction Supplies",
  "registration_number": "BN123456",
  "verified_status": "APPROVED",
  "location": "Nairobi, Kenya",
  "categories_served": ["Cement", "Steel", "Bricks"],
  "fulfillment_rate": 95.5,
  "cancellation_rate": 2.3,
  "delivery_timeliness": 98.0,
  "average_rating": 4.8,
  "total_reviews": 124,
  "created_at": "2026-01-15T10:30:00Z"
}
```

### **Update Vendor Profile**
```http
PATCH /api/vendors/5/
Authorization: Token <vendor_token>
Content-Type: application/json

{
  "business_name": "ABC Construction Supplies Ltd",
  "registration_number": "BN123456",
  "location": "Nairobi, Kenya",
  "categories_served": ["Cement", "Steel", "Bricks", "Tiles"]
}
```

**Response:**
```json
{
  "id": 5,
  "business_name": "ABC Construction Supplies Ltd",
  "registration_number": "BN123456",
  "location": "Nairobi, Kenya",
  "categories_served": ["Cement", "Steel", "Bricks", "Tiles"],
  ...
}
```

---

## 🧪 **Testing Checklist**

### **Profile Viewing**
- [ ] Navigate to Vendor Dashboard
- [ ] Click "My Profile" tab
- [ ] Verify profile loads correctly
- [ ] Verify verification status banner shows
- [ ] Verify business information displays
- [ ] Verify account information displays
- [ ] Verify performance metrics display

### **Profile Editing**
- [ ] Click "Edit Profile" button
- [ ] Verify form fields become editable
- [ ] Update business name
- [ ] Update registration number
- [ ] Update location
- [ ] Update categories (comma-separated)
- [ ] Click "Save Changes"
- [ ] Verify success message
- [ ] Verify profile updates

### **Edit Cancellation**
- [ ] Click "Edit Profile"
- [ ] Make some changes
- [ ] Click "Cancel"
- [ ] Verify changes are reverted
- [ ] Verify form returns to view mode

### **Verification Status**
- [ ] Test with PENDING status vendor
- [ ] Test with APPROVED status vendor
- [ ] Test with REJECTED status vendor
- [ ] Test with SUSPENDED status vendor
- [ ] Verify correct banner colors and messages

### **Security**
- [ ] Try to edit `verified_status` via form
- [ ] Verify backend prevents the change
- [ ] Verify only own profile can be edited

---

## 📱 **Responsive Design**

The profile section is fully responsive:

**Desktop:**
- Metrics grid: 4 columns
- Form fields: 2 columns

**Tablet:**
- Metrics grid: 2 columns
- Form fields: 2 columns

**Mobile:**
- Metrics grid: 1 column
- Form fields: 1 column (full width)

---

## ✅ **Summary**

**Question**: Where does a vendor manage their profile?

**Answer**: **Vendor Dashboard → 👤 My Profile Tab**

**What Vendors Can Do:**
- ✅ View verification status
- ✅ Edit business information
- ✅ Update categories served
- ✅ View performance metrics
- ✅ See account details

**What Vendors See:**
- 🎨 Color-coded verification status banner
- 📊 Performance metrics in gradient cards
- 📝 Editable business information form
- 🏷️ Category tags
- 📧 Account information (read-only)

**Key Features:**
- ✅ Tabbed interface (Profile, Inventory, Orders)
- ✅ Edit/View mode toggle
- ✅ Real-time form validation
- ✅ Beautiful UI with gradients and animations
- ✅ Responsive design
- ✅ Secure backend protection

The vendor profile management system is now **fully functional** and provides a professional, user-friendly experience! 🚀
