# 🚚 Logistics V2: Courier Self-Registration & Management Architecture

**Version:** 2.0  
**Status:** Draft  
**Date:** 2026-02-21  

---

## 1. System Overview

This document outlines the architecture for a **multi-tenant, self-service logistics platform** where couriers can register, configure their APIs, define pricing zones, and manage shipments. The system emphasizes **security, validation, and automated governance**.

### High-Level Architecture

```mermaid
graph TD
    subgraph "Courier Portal"
        CR[Courier Registration]
        PC[Pricing Config]
        AC[API Config]
        WH[Webhook Setup]
    end

    subgraph "Admin Console"
        AV[Validation Workflow]
        GOV[Governance & SLA]
        AUD[Audit Logs]
    end

    subgraph "Core Engine"
        PE[Pricing Engine]
        TE[Tracking Engine]
        AE[Adapter Engine]
    end

    subgraph "External World"
        EXT_API[Courier APIs (DHL, G4S, etc.)]
        DRIVERS[Driver GPS Apps]
    end

    CR --> AV
    PC --> PE
    AC --> AE
    WH --> TE
    AE <--> EXT_API
    DRIVERS --> TE
    TE --> GOV
```

---

## 2. Database Schema Design

### 2.1 Courier Identity & Validation
```python
class CourierProfile(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('PENDING', 'Pending Review'),
        ('UNDER_REVIEW', 'Under Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('SUSPENDED', 'Suspended')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=100)
    tax_pin = models.CharField(max_length=50)
    
    # Validation
    status = models.CharField(choices=STATUS_CHOICES, default='DRAFT')
    rejection_reason = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(User, related_name='reviewed_couriers', null=True)
    reviewed_at = models.DateTimeField(null=True)

class CourierDocument(models.Model):
    TYPE_CHOICES = [
        ('LICENSE', 'Transport License'),
        ('INSURANCE', 'Insurance Certificate'),
        ('REGISTRATION', 'Business Registration')
    ]
    
    courier = models.ForeignKey(CourierProfile, on_delete=models.CASCADE)
    document_type = models.CharField(choices=TYPE_CHOICES)
    file = models.FileField(upload_to='courier_docs/')
    is_verified = models.BooleanField(default=False)
    expiry_date = models.DateField(null=True)
```

### 2.2 API Configuration (Adapter Pattern)
```python
class CourierApiConfig(models.Model):
    courier = models.OneToOneField(CourierProfile, on_delete=models.CASCADE)
    base_url = models.URLField()
    api_key = models.CharField(max_length=255) # Encrypted
    api_secret = models.CharField(max_length=255) # Encrypted
    
    # Endpoint Mapping
    create_order_endpoint = models.CharField(max_length=255, default='/orders')
    cancel_order_endpoint = models.CharField(max_length=255, default='/orders/cancel')
    track_order_endpoint = models.CharField(max_length=255, default='/track')
    
    # Field Mapping (JSON)
    # e.g., {"recipient_name": "to_name", "recipient_phone": "to_mobile"}
    field_mapping = models.JSONField(default=dict)
    status_mapping = models.JSONField(default=dict)
    
    is_active = models.BooleanField(default=False)
```

### 2.3 Pricing Engine
```python
class PricingZone(models.Model):
    TYPE_CHOICES = [('POLYGON', 'Polygon'), ('RADIUS', 'Radius')]
    
    courier = models.ForeignKey(CourierProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    zone_type = models.CharField(choices=TYPE_CHOICES)
    
    # GeoJSON or Center+Radius
    geometry = models.JSONField(null=True) 
    center_lat = models.FloatField(null=True)
    center_lng = models.FloatField(null=True)
    radius_km = models.FloatField(null=True)

class PricingRule(models.Model):
    courier = models.ForeignKey(CourierProfile, on_delete=models.CASCADE)
    zone = models.ForeignKey(PricingZone, on_delete=models.CASCADE)
    
    base_cost = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Weight Slabs
    min_weight = models.DecimalField(default=0)
    max_weight = models.DecimalField(default=1000)
    per_kg_cost = models.DecimalField(default=0)
    
    # Express Surcharges
    express_multiplier = models.DecimalField(default=1.5)
```

---

## 3. API Definitions

### 3.1 Courier Registration (`/api/logistics/couriers/register/`)
*   **POST**: Create a new draft profile.
*   **Payload**:
    ```json
    {
      "company_name": "Swift Logistics",
      "registration_number": "REG12345",
      "contact_email": "admin@swift.com"
    }
    ```

### 3.2 Document Upload (`/api/logistics/documents/`)
*   **POST**: Upload license/insurance.
*   **Payload**: `Multipart/Form-Data` (file, type).

### 3.3 API Configuration (`/api/logistics/config/api/`)
*   **PUT**: Update API credentials and endpoints.
*   **POST /test-connection**: Trigger a test request to validate credentials.

### 3.4 Admin Validation (`/api/admin/couriers/{id}/validate/`)
*   **POST**: Approve or Reject.
*   **Payload**:
    ```json
    {
      "action": "APPROVE", // or REJECT
      "reason": "Documents verified. API test passed."
    }
    ```

---

## 4. Technical Workflows

### 4.1 Courier Self-Registration Flow
1.  Courier signs up -> `CourierProfile` created with status `DRAFT`.
2.  Courier uploads documents -> Admin notified.
3.  Courier configures API -> System attempts "Ping" to external API.
4.  Courier submits for review -> Status `PENDING`.

### 4.2 Admin Validation Workflow (CRITICAL)
1.  Admin views "Pending Couriers" queue.
2.  **Document Check**: Admin manually verifies uploaded PDFs.
3.  **API Check**: Admin clicks "Test API". Backend sends a dummy payload to the configured `base_url` using the mapped fields.
    *   If success (200 OK): API status marked `VERIFIED`.
    *   If fail: Error log shown to Admin.
4.  **Final Decision**:
    *   **Approve**: Status -> `APPROVED`. Courier is now live in the marketplace.
    *   **Reject**: Status -> `REJECTED`. Reason sent to Courier via email.

### 4.3 Tracking & Webhook Flow
1.  **Configuration**: Courier provides a webhook URL in their portal.
2.  **Validation**: System sends a `ping` event with a challenge. Courier endpoint must respond correctly.
3.  **Ingestion**:
    *   External system POSTs update to `/api/webhooks/courier/{courier_id}/`.
    *   System validates signature (HMAC).
    *   System translates external status (e.g., "OutForDelivery") to internal status (`OUT_FOR_DELIVERY`) using `status_mapping`.
    *   `TrackingEvent` created -> WebSocket notification sent to Buyer.

---

## 5. Security & Governance

*   **Credential Encryption**: All API keys/secrets stored using `Fernet` symmetric encryption (via `django-fernet-fields`).
*   **Rate Limiting**: Per-courier API limits to prevent flooding.
*   **SLA Monitoring**: Background job checks `Shipment.created_at` vs `Shipment.delivered_at`. If average > SLA, flag courier for review.
*   **Auto-Suspension**: If `webhook_failure_rate > 10%`, auto-suspend integration and notify Admin.

---

## 6. Implementation Roadmap

1.  **Phase 1 (Schema)**: Create `CourierProfile`, `CourierApiConfig`, `PricingZone` models.
2.  **Phase 2 (Logic)**: Implement `BaseCourierAdapter` and dynamic JSON mapping.
3.  **Phase 3 (Admin)**: Build the Admin Validation ViewSet and "Test API" action.
4.  **Phase 4 (Frontend)**: Build the Courier Portal UI (Vue 3).

