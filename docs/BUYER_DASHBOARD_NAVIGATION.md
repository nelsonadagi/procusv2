# Buyer Dashboard - Navigation Guide

## 🧭 How to Access the Buyer Dashboard

The Buyer Dashboard is now accessible from **multiple locations** for your convenience:

---

## 1️⃣ **Main Navigation Bar** (Always Visible When Logged In)

After logging in, look at the **top navigation bar**:

```
┌─────────────────────────────────────────────────────────┐
│ Ujenzi Marketplace                                      │
│                                                         │
│ Marketplace | Contracts | Tenders | 🔵 My Orders | ... │
│                                    ↑                    │
│                              CLICK HERE!                │
└─────────────────────────────────────────────────────────┘
```

**Link**: "**My Orders**" - Available to ALL authenticated users

**Direct URL**: http://localhost:8080/buyer/dashboard

---

## 2️⃣ **Homepage Welcome Banner**

When you're logged in and visit the homepage (`/`), you'll see:

```
┌─────────────────────────────────────────────┐
│ Welcome back, John! 👋                      │
│ You are logged in as a PROJECT_OWNER.       │
│                                             │
│ [Track My Orders] ← Click this button      │
└─────────────────────────────────────────────┘
```

This button appears for:
- PROJECT_OWNER users
- CONTRACTOR users

---

## 3️⃣ **Direct URL Access**

You can always bookmark or navigate directly to:

**http://localhost:8080/buyer/dashboard**

This works for any authenticated user, regardless of role.

---

## 📊 **What's in the Buyer Dashboard?**

Once you access the dashboard, you'll see **5 tabs**:

### 1. **Orders Tab** (Default)
- View all your orders
- Track order status (PLACED → DELIVERED → COMPLETED)
- Confirm delivery
- Cancel orders (if not yet shipped)
- Initiate disputes
- Rate vendors

### 2. **Quotes Tab**
- View your quote requests
- See vendor responses
- Compare prices and delivery fees
- Checkout from accepted quotes

### 3. **Profile Tab**
- Update your name, phone
- **Change your primary role** (NEW!)
- Set preferred region
- Update delivery preferences

### 4. **Addresses Tab**
- Manage delivery locations
- Add construction sites
- Set default address
- Delete old addresses

### 5. **Disputes Tab**
- View open disputes (future)
- Track resolution status (future)

---

## 🎯 **Quick Access Cheat Sheet**

| From | Action | Destination |
|------|--------|-------------|
| **Any page** | Click "My Orders" in nav | Buyer Dashboard |
| **Homepage** | Click "Track My Orders" | Buyer Dashboard |
| **Browser** | Type `/buyer/dashboard` | Buyer Dashboard |
| **Product page** | Request quote → View in dashboard | Quotes tab |

---

## 🔍 **Navigation Changes Made**

### Before (Old Navigation)
```
Marketplace | Contracts | Tenders | My Shop | My Bids | My Projects | My Purchases
                                                                      ↑
                                                          Only for some roles
```

### After (New Navigation)
```
Marketplace | Contracts | Tenders | My Orders | My Shop | My Bids | My Projects
                                    ↑
                          Available to ALL logged-in users
```

**Key Improvement**: 
- "My Orders" is now visible to **all authenticated users**
- Renamed from "My Purchases" to "My Orders" (clearer)
- Positioned prominently after core marketplace links

---

## 🚀 **Step-by-Step: First Time Access**

### For New Users:
1. **Register** at http://localhost:8080/register
2. **Login** (or you're auto-logged in)
3. Look at the **top navigation bar**
4. Click **"My Orders"**
5. You're now in the Buyer Dashboard!

### For Existing Users:
1. **Login** at http://localhost:8080/login
2. Click **"My Orders"** in the top nav
3. Done!

---

## 💡 **Pro Tips**

### Tip 1: Bookmark It
Add http://localhost:8080/buyer/dashboard to your bookmarks for quick access.

### Tip 2: Check After Requesting a Quote
After clicking "Request Quote" on a product:
1. Go to "My Orders" in nav
2. Click "Quotes" tab
3. See your quote request

### Tip 3: Multi-Role Users
If you're both a VENDOR and a buyer:
- "My Orders" → Track your purchases
- "My Shop" → Manage your inventory
Both links appear in the nav!

---

## 🐛 **Troubleshooting**

### "I don't see 'My Orders' in the navigation"
**Solution**: Make sure you're logged in. The link only appears for authenticated users.

### "The link is there but clicking it shows nothing"
**Solution**: 
1. Check browser console for errors (F12)
2. Verify backend is running: http://localhost:8000/api/orders/orders/
3. Check your auth token is valid

### "I see 'My Orders' but the page is empty"
**Solution**: This is normal if you haven't placed any orders yet! Try:
1. Go to Marketplace
2. Click "Request Quote" on a product
3. Return to "My Orders" → "Quotes" tab

---

## 📱 **Mobile Navigation**

On mobile devices, the navigation may collapse into a hamburger menu:

```
☰ Menu
├─ Marketplace
├─ Contracts
├─ Tenders
├─ My Orders ← Here!
├─ My Shop (if vendor)
└─ ...
```

---

## 🎨 **Visual Hierarchy**

The navigation is organized by **frequency of use**:

1. **Core Features** (Always visible)
   - Marketplace
   - Contracts
   - Tenders

2. **User-Specific** (When logged in)
   - **My Orders** ← Universal buyer dashboard

3. **Role-Specific** (Based on your role)
   - My Shop (Vendors)
   - My Bids (Contractors)
   - My Projects (Project Owners)
   - Invest (Investors)
   - Admin (Admins)

---

## ✅ **Summary**

**The Buyer Dashboard is now:**
- ✅ Accessible from main navigation ("My Orders")
- ✅ Available to ALL authenticated users
- ✅ Prominently positioned
- ✅ Clearly labeled
- ✅ Always visible (not hidden by role)

**You can access it:**
- From the nav bar (click "My Orders")
- From the homepage welcome banner
- By typing `/buyer/dashboard` in the URL

---

**Last Updated**: 2026-01-31  
**Status**: ✅ Navigation Fixed and Live  
**Access**: http://localhost:8080/buyer/dashboard
