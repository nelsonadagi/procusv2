from django.contrib import admin
from .models import KYCVerification, JurisdictionRule

admin.site.register(KYCVerification)
admin.site.register(JurisdictionRule)
