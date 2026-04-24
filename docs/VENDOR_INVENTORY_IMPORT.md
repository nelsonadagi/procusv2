# Vendor Inventory Import & Filtering

## 📦 **Feature Overview**

This update introduces two key enhancements for vendors:
1.  **"My Products" Filtering**: The inventory view now strictly shows only products belonging to the logged-in vendor.
2.  **Bulk Product Import**: Vendors can now upload a CSV file to bulk create products.
3.  **Inventory Ledger Controls**: Vendors can adjust stock with notes/references and inspect movement history per product.

---

## 🔒 **My Products Filtering**

**How it works:**
- The inventory view uses the vendor-scoped endpoint directly:
  ```http
  GET /api/v1/products/me/
  ```
- This ensures vendors never see other vendors' products in their inventory management view.

---

## 📥 **CSV Import Guide**

Vendors can import products using a CSV file.

### **1. CSV Format**

The CSV file must have a header row with the following columns (headers are case-insensitive):

| Column Header | Required | Description | Example |
|---------------|----------|-------------|---------|
| `Name` | ✅ Yes | Product name | `Dangote Cement 50kg` |
| `Category` | ✅ Yes | Valid material category name | `Cement` |
| `Price` or `base_price` | ❌ No | Price per unit (default: 0) | `650` |
| `Unit` | ❌ No | Unit of measure (default: 'unit') | `bag` |
| `Stock` or `stock_quantity` | ❌ No | Quantity available (default: 0) | `100` |
| `Description` | ❌ No | Detailed description | `High quality cement...` |
| `Short Description` | ❌ No | Brief summary | `50kg bag` |
| `Brand` | ❌ No | Brand name | `Dangote` |

**Example CSV Content:**
```csv
Name,Category,Price,Unit,Stock,Brand
Blue Triangle Cement,Cement,700,bag,500,Blue Triangle
Twisted Steel Bar Y12,Steel,1200,piece,200,Apex
```

### **2. How to Import**

1.  Navigate to **Vendor Dashboard** > **Inventory**.
2.  **Recommended:** Click the **"📄 Download Template"** link to get a ready-to-use CSV file.
3.  Click the **"📥 Import CSV"** button.
4.  Select your filled `.csv` file.
5.  The system will process the file and report:
    - Number of products created.
    - Any warnings or errors (e.g., missing categories).

### **3. Validation Rules**

- **Category**: Must match an existing category in the system (e.g., "Cement", "Steel", "Aggregates"). If a category is not found, that row will fail.
- **Name**: Required. Rows without a name are skipped.

---

## 🛠 **Technical Implementation details**

### **Backend**
- **Endpoint**: `POST /api/v1/products/import_products/`
- **Permission**: Vendor only.
- **Logic**: Iterates through CSV rows, looks up categories by name/slug, and creates `Product` entries linked to the request user's vendor profile.

### **Frontend**
- **Component**: `VendorInventorySection.vue`
- **Logic**: Uses a hidden file input to trigger file selection, uploads via `FormData`, and refreshes the vendor-scoped inventory feed after import.
- **Feedback**: Displays success message with count and any row-level errors.

---

## 🧾 **Operational Inventory Controls**

- Use `POST /api/v1/products/{product_uuid}/adjust-inventory/` for real stock adjustments.
- Use `GET /api/v1/products/{product_uuid}/inventory-history/` to review movement logs.
- Product editing can still change stock, but vendor operations should prefer explicit adjustments so the ledger stays meaningful.

---

## ✅ **Testing Checklist**

- [ ] **Filter Check**: Login as Vendor A. Verify you DO NOT see Vendor B's products.
- [ ] **Import Success**: Upload a valid CSV. Verify products appear in the list.
- [ ] **Import Error**: Upload a CSV with a non-existent category. Verify error message.
- [ ] **File Type**: Upload a non-CSV file. Verify rejection.
