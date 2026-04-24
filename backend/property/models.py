from django.db import models
from django.conf import settings


class PropertyListing(models.Model):
    class Type(models.TextChoices):
        LAND = 'LAND', 'Land'
        RESIDENTIAL = 'RESIDENTIAL', 'Residential'
        COMMERCIAL = 'COMMERCIAL', 'Commercial'
        INDUSTRIAL = 'INDUSTRIAL', 'Industrial'
        MIXED_USE = 'MIXED_USE', 'Mixed Use'
        HOSPITALITY = 'HOSPITALITY', 'Hospitality'
        RENOVATION = 'RENOVATION', 'Renovation'
        SPECIAL_PURPOSE = 'SPECIAL_PURPOSE', 'Special Purpose'

    class ListingType(models.TextChoices):
        SALE = 'SALE', 'Sale'
        LEASE = 'LEASE', 'Lease'
        DEVELOPMENT_OPPORTUNITY = 'DEVELOPMENT_OPPORTUNITY', 'Development Opportunity'
        COMPLETED_PROJECT = 'COMPLETED_PROJECT', 'Completed Project'

    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        ACTIVE = 'ACTIVE', 'Active'
        SOLD = 'SOLD', 'Sold'
        LEASED = 'LEASED', 'Leased'
        UNDER_OFFER = 'UNDER_OFFER', 'Under Offer'
        INACTIVE = 'INACTIVE', 'Inactive'

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='properties', verbose_name="Property Owner")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_properties', verbose_name="Property Manager")
    title = models.CharField(max_length=255, verbose_name="Property Title")
    description = models.TextField(verbose_name="Property Description", help_text="Detailed description of the property")

    # Location Intelligence
    country = models.ForeignKey('platform_settings.Country', on_delete=models.SET_NULL, null=True, blank=True, related_name='properties', verbose_name="Country")
    location_text = models.CharField(max_length=255, db_column='location', null=True, blank=True, verbose_name="Location Name")
    location = models.ForeignKey('platform_settings.Location', on_delete=models.SET_NULL, null=True, blank=True, related_name='properties', verbose_name="Specific Location")
    latitude = models.DecimalField(max_digits=12, decimal_places=9, null=True, blank=True, verbose_name="GPS Latitude")
    longitude = models.DecimalField(max_digits=12, decimal_places=9, null=True, blank=True, verbose_name="GPS Longitude")
    formatted_address = models.TextField(blank=True, verbose_name="Full Formatted Address")

    purpose = models.ForeignKey(
        'taxonomy.Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='property_listings',
        limit_choices_to={'taxonomy_type': 'PROPERTY'},
        verbose_name="Property Purpose",
    )
    asset_type = models.CharField(max_length=20, choices=Type.choices, verbose_name="Type of Asset")
    listing_type = models.CharField(max_length=30, choices=ListingType.choices, default=ListingType.SALE, verbose_name="Listing Type")
    price_estimate = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Estimated Price / Value")
    financing_allowed = models.BooleanField(default=False, verbose_name="Financing Allowed")
    inquiry_enabled = models.BooleanField(default=True, verbose_name="Inquiries Enabled")
    appointment_enabled = models.BooleanField(default=True, verbose_name="Appointments Enabled")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE, verbose_name="Current Listing Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    def __str__(self):
        return self.title


class DevelopmentMetadata(models.Model):
    property = models.OneToOneField(PropertyListing, on_delete=models.CASCADE, related_name='development_metadata')
    zoning_info = models.CharField(max_length=255)
    build_ready = models.BooleanField(default=False)
    utilities_available = models.JSONField(default=list) # e.g. ["Water", "Power"]
    development_stage = models.CharField(max_length=30, blank=True, default='')
    estimated_completion_budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    expected_completion_date = models.DateField(null=True, blank=True)
    recommended_use = models.CharField(max_length=255, blank=True, default='')


class PropertySpecification(models.Model):
    class AreaUnit(models.TextChoices):
        SQM = 'SQM', 'Square Meters'
        SQFT = 'SQFT', 'Square Feet'
        ACRE = 'ACRE', 'Acre'
        HECTARE = 'HECTARE', 'Hectare'

    class FurnishingState(models.TextChoices):
        UNFURNISHED = 'UNFURNISHED', 'Unfurnished'
        PART_FURNISHED = 'PART_FURNISHED', 'Part Furnished'
        FURNISHED = 'FURNISHED', 'Furnished'
        FITTED = 'FITTED', 'Fitted'

    class ConditionRating(models.TextChoices):
        SHELL = 'SHELL', 'Shell'
        FAIR = 'FAIR', 'Fair'
        GOOD = 'GOOD', 'Good'
        EXCELLENT = 'EXCELLENT', 'Excellent'

    class OccupancyStatus(models.TextChoices):
        VACANT = 'VACANT', 'Vacant'
        OCCUPIED = 'OCCUPIED', 'Occupied'
        OWNER_OCCUPIED = 'OWNER_OCCUPIED', 'Owner Occupied'
        TENANTED = 'TENANTED', 'Tenanted'
        UNDER_CONSTRUCTION = 'UNDER_CONSTRUCTION', 'Under Construction'

    property = models.OneToOneField(PropertyListing, on_delete=models.CASCADE, related_name='specification')
    bedrooms = models.PositiveIntegerField(null=True, blank=True)
    bathrooms = models.PositiveIntegerField(null=True, blank=True)
    floors = models.PositiveIntegerField(null=True, blank=True)
    parking_spaces = models.PositiveIntegerField(null=True, blank=True)
    internal_area = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    internal_area_unit = models.CharField(max_length=10, choices=AreaUnit.choices, default=AreaUnit.SQM)
    lot_size = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    lot_size_unit = models.CharField(max_length=10, choices=AreaUnit.choices, default=AreaUnit.SQM)
    year_built = models.PositiveIntegerField(null=True, blank=True)
    renovation_year = models.PositiveIntegerField(null=True, blank=True)
    furnishing_state = models.CharField(max_length=20, choices=FurnishingState.choices, blank=True, default='')
    condition_rating = models.CharField(max_length=20, choices=ConditionRating.choices, blank=True, default='')
    energy_rating = models.CharField(max_length=20, blank=True, default='')
    occupancy_status = models.CharField(max_length=30, choices=OccupancyStatus.choices, blank=True, default='')


class PropertyFeature(models.Model):
    property = models.ForeignKey(PropertyListing, on_delete=models.CASCADE, related_name='features')
    category = models.CharField(max_length=100, blank=True, default='')
    code = models.CharField(max_length=50, blank=True, default='')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    is_highlighted = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'name']

    def __str__(self):
        return f'{self.property.title}: {self.name}'


class PropertyMediaAsset(models.Model):
    class MediaType(models.TextChoices):
        IMAGE = 'IMAGE', 'Image'
        VIDEO = 'VIDEO', 'Video'
        FLOOR_PLAN = 'FLOOR_PLAN', 'Floor Plan'
        DOCUMENT = 'DOCUMENT', 'Document'
        VIRTUAL_TOUR = 'VIRTUAL_TOUR', 'Virtual Tour'

    property = models.ForeignKey(PropertyListing, on_delete=models.CASCADE, related_name='media_assets')
    media_type = models.CharField(max_length=20, choices=MediaType.choices, default=MediaType.IMAGE)
    file = models.FileField(upload_to='property/media/', null=True, blank=True)
    external_url = models.URLField(blank=True, default='')
    title = models.CharField(max_length=255, blank=True, default='')
    caption = models.TextField(blank=True, default='')
    alt_text = models.CharField(max_length=255, blank=True, default='')
    sort_order = models.PositiveIntegerField(default=0)
    is_primary = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)

    class Meta:
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.title or f'{self.media_type} asset'


class PropertyOwnershipProfile(models.Model):
    class OwnershipType(models.TextChoices):
        INDIVIDUAL = 'INDIVIDUAL', 'Individual'
        COMPANY = 'COMPANY', 'Company'
        TRUST = 'TRUST', 'Trust'
        GOVERNMENT = 'GOVERNMENT', 'Government'
        OTHER = 'OTHER', 'Other'

    class VerificationStatus(models.TextChoices):
        UNVERIFIED = 'UNVERIFIED', 'Unverified'
        PENDING = 'PENDING', 'Pending'
        VERIFIED = 'VERIFIED', 'Verified'
        FLAGGED = 'FLAGGED', 'Flagged'

    property = models.OneToOneField(PropertyListing, on_delete=models.CASCADE, related_name='ownership_profile')
    legal_owner_name = models.CharField(max_length=255, blank=True, default='')
    ownership_type = models.CharField(max_length=20, choices=OwnershipType.choices, blank=True, default='')
    title_reference = models.CharField(max_length=255, blank=True, default='')
    deed_reference = models.CharField(max_length=255, blank=True, default='')
    has_liens = models.BooleanField(default=False)
    lien_notes = models.TextField(blank=True, default='')
    disclosure_notes = models.TextField(blank=True, default='')
    verification_status = models.CharField(max_length=20, choices=VerificationStatus.choices, default=VerificationStatus.UNVERIFIED)


class PropertyPricingProfile(models.Model):
    class PricingStrategy(models.TextChoices):
        FIXED = 'FIXED', 'Fixed'
        NEGOTIABLE = 'NEGOTIABLE', 'Negotiable'
        PRICE_ON_APPLICATION = 'PRICE_ON_APPLICATION', 'Price on Application'
        PER_UNIT = 'PER_UNIT', 'Per Unit'

    property = models.OneToOneField(PropertyListing, on_delete=models.CASCADE, related_name='pricing_profile')
    currency = models.CharField(max_length=3, default='KES')
    asking_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    rent_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    pricing_strategy = models.CharField(max_length=25, choices=PricingStrategy.choices, default=PricingStrategy.FIXED)
    requires_deposit = models.BooleanField(default=False)
    deposit_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    price_per_area_unit = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    area_unit = models.CharField(max_length=10, choices=PropertySpecification.AreaUnit.choices, default=PropertySpecification.AreaUnit.SQM)
    service_charge_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    insurance_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    financing_notes = models.TextField(blank=True, default='')


class PropertyShowing(models.Model):
    class EventType(models.TextChoices):
        OPEN_HOUSE = 'OPEN_HOUSE', 'Open House'
        PRIVATE_SHOWING = 'PRIVATE_SHOWING', 'Private Showing'

    class OccurrenceType(models.TextChoices):
        SINGLE = 'SINGLE', 'Single'
        RECURRING = 'RECURRING', 'Recurring'
        APPOINTMENT_ONLY = 'APPOINTMENT_ONLY', 'Appointment Only'

    property = models.ForeignKey(PropertyListing, on_delete=models.CASCADE, related_name='showings')
    event_type = models.CharField(max_length=20, choices=EventType.choices, default=EventType.PRIVATE_SHOWING)
    occurrence_type = models.CharField(max_length=20, choices=OccurrenceType.choices, default=OccurrenceType.SINGLE)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    recurrence_rule = models.CharField(max_length=120, blank=True, default='')
    recurrence_end_at = models.DateTimeField(null=True, blank=True)
    contact_person = models.CharField(max_length=255, blank=True, default='')
    phone = models.CharField(max_length=50, blank=True, default='')
    instructions = models.TextField(blank=True, default='')
    virtual_tour_url = models.URLField(blank=True, default='')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['start_at']

    def __str__(self):
        return f'{self.property.title}: {self.event_type}'


class PropertyProjectLink(models.Model):
    property = models.ForeignKey(PropertyListing, on_delete=models.CASCADE, related_name='linked_projects')
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='linked_properties')


class PropertyInquiry(models.Model):
    class InquiryType(models.TextChoices):
        GENERAL = 'GENERAL', 'General'
        VIEWING = 'VIEWING', 'Viewing'
        FINANCING = 'FINANCING', 'Financing'
        PARTNERSHIP = 'PARTNERSHIP', 'Partnership'
        MATERIALS = 'MATERIALS', 'Materials'
        SERVICE = 'SERVICE', 'Service'

    class Status(models.TextChoices):
        NEW = 'NEW', 'New'
        CONTACTED = 'CONTACTED', 'Contacted'
        QUALIFIED = 'QUALIFIED', 'Qualified'
        CLOSED = 'CLOSED', 'Closed'
        SPAM = 'SPAM', 'Spam'

    property = models.ForeignKey(PropertyListing, on_delete=models.CASCADE, related_name='inquiries')
    inquirer_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='property_inquiries')
    inquiry_type = models.CharField(max_length=20, choices=InquiryType.choices, default=InquiryType.GENERAL)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=50, blank=True)
    preferred_contact_method = models.CharField(max_length=20, blank=True, default='')
    message = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    chat_room = models.ForeignKey('chat.ChatRoom', on_delete=models.SET_NULL, null=True, blank=True, related_name='property_inquiries')
    created_at = models.DateTimeField(auto_now_add=True)


class PropertyAvailabilityWindow(models.Model):
    property = models.ForeignKey(PropertyListing, on_delete=models.CASCADE, related_name='availability_windows')
    managed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='property_availability_windows')
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    recurrence_rule = models.CharField(max_length=100, blank=True, default='')
    slot_duration_minutes = models.PositiveIntegerField(default=60)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start_at']


class PropertyAppointment(models.Model):
    class Status(models.TextChoices):
        REQUESTED = 'REQUESTED', 'Requested'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'
        NO_SHOW = 'NO_SHOW', 'No Show'

    property = models.ForeignKey(PropertyListing, on_delete=models.CASCADE, related_name='appointments')
    availability_window = models.ForeignKey(PropertyAvailabilityWindow, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')
    visitor_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='property_appointments')
    full_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=50, blank=True)
    scheduled_start = models.DateTimeField()
    scheduled_end = models.DateTimeField()
    notes = models.TextField(blank=True, default='')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.REQUESTED)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_property_appointments')
    chat_room = models.ForeignKey('chat.ChatRoom', on_delete=models.SET_NULL, null=True, blank=True, related_name='property_appointments')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['scheduled_start']
