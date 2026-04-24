from django.contrib import admin

from .models import (
    PropertyListing,
    DevelopmentMetadata,
    PropertySpecification,
    PropertyFeature,
    PropertyMediaAsset,
    PropertyOwnershipProfile,
    PropertyPricingProfile,
    PropertyShowing,
    PropertyProjectLink,
    PropertyInquiry,
    PropertyAvailabilityWindow,
    PropertyAppointment,
)


admin.site.register(PropertyListing)
admin.site.register(DevelopmentMetadata)
admin.site.register(PropertySpecification)
admin.site.register(PropertyFeature)
admin.site.register(PropertyMediaAsset)
admin.site.register(PropertyOwnershipProfile)
admin.site.register(PropertyPricingProfile)
admin.site.register(PropertyShowing)
admin.site.register(PropertyProjectLink)
admin.site.register(PropertyInquiry)
admin.site.register(PropertyAvailabilityWindow)
admin.site.register(PropertyAppointment)
