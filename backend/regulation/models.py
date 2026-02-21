from django.db import models
from django.conf import settings

class InvestorProfile(models.Model):
    class KYCStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        VERIFIED = 'VERIFIED', 'Verified'
        REJECTED = 'REJECTED', 'Rejected'
        
    class AccreditationStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        ACCREDITED = 'ACCREDITED', 'Accredited'
        NONE = 'NONE', 'None'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='investor_profile')
    kyc_status = models.CharField(max_length=20, choices=KYCStatus.choices, default=KYCStatus.PENDING)
    accreditation_status = models.CharField(max_length=20, choices=AccreditationStatus.choices, default=AccreditationStatus.NONE)
    jurisdiction = models.CharField(max_length=100, default='Global')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Investor: {self.user.username}"

class InvestmentAgreement(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        SIGNED = 'SIGNED', 'Signed'
        FUNDED = 'FUNDED', 'Funded'
        CANCELLED = 'CANCELLED', 'Cancelled'

    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='agreements')
    investor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='investment_agreements')
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    agreement_terms_url = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    signed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class InvestmentTransaction(models.Model):
    class Type(models.TextChoices):
        FUNDING = 'FUNDING', 'Funding'
        RELEASE = 'RELEASE', 'Release'
        RETURN = 'RETURN', 'Return'

    agreement = models.ForeignKey(InvestmentAgreement, on_delete=models.CASCADE, related_name='transactions')
    # Link to escrow optionally, or just track ledger here
    escrow_account_id = models.IntegerField(null=True, blank=True) 
    type = models.CharField(max_length=20, choices=Type.choices)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class InvestorReport(models.Model):
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='reports')
    investor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports')
    report_period = models.CharField(max_length=50) # e.g. "Q1 2026"
    performance_summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
