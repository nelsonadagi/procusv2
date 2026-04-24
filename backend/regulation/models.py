from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class InvestorProfile(models.Model):
    class KYCStatus(models.TextChoices):
        PENDING = 'PENDING', _('⏳ Verification in Progress')
        VERIFIED = 'VERIFIED', _('✅ Identity Verified')
        REJECTED = 'REJECTED', _('❌ Verification Failed')
        
    class AccreditationStatus(models.TextChoices):
        PENDING = 'PENDING', _('⏳ Under Review')
        ACCREDITED = 'ACCREDITED', _('✅ Accredited Investor')
        NONE = 'NONE', _('📝 Not Accredited')

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='investor_profile',
        verbose_name="Account Owner"
    )
    kyc_status = models.CharField(
        max_length=20, 
        choices=KYCStatus.choices, 
        default=KYCStatus.PENDING,
        verbose_name="Identity Verification"
    )
    accreditation_status = models.CharField(
        max_length=20, 
        choices=AccreditationStatus.choices, 
        default=AccreditationStatus.NONE,
        verbose_name="Investment Accreditation"
    )
    jurisdiction = models.CharField(
        max_length=100, 
        default='Global',
        verbose_name="Country of Residence"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Profile Created")

    class Meta:
        verbose_name = "Investor Profile"
        verbose_name_plural = "Investor Profiles"

    def __str__(self):
        return f"Investor: {self.user.get_full_name() or self.user.username}"


class InvestmentAgreement(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', _('📝 Draft - Awaiting Signatures')
        SIGNED = 'SIGNED', _('✏️ Signed by All Parties')
        FUNDED = 'FUNDED', _('💰 Funds Transferred')
        CANCELLED = 'CANCELLED', _('❌ Cancelled')

    project = models.ForeignKey(
        'projects.Project', 
        on_delete=models.CASCADE, 
        related_name='agreements',
        verbose_name="Investment In"
    )
    investor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='investment_agreements',
        verbose_name="Investor"
    )
    amount = models.DecimalField(
        max_digits=14, 
        decimal_places=2,
        verbose_name="Investment Amount"
    )
    agreement_terms_url = models.URLField(
        blank=True,
        verbose_name="Contract Document"
    )
    status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.DRAFT,
        verbose_name="Agreement Status"
    )
    signed_at = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name="Date Signed"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created On")

    class Meta:
        verbose_name = "Investment Agreement"
        verbose_name_plural = "Investment Agreements"

    def __str__(self):
        return f"{self.investor.username} → {self.project.title}"


class InvestmentTransaction(models.Model):
    class Type(models.TextChoices):
        FUNDING = 'FUNDING', _('💰 Investment Deposit')
        RELEASE = 'RELEASE', _('💸 Funds Released to Project')
        RETURN = 'RETURN', _('↩️ Return of Investment')

    agreement = models.ForeignKey(
        InvestmentAgreement, 
        on_delete=models.CASCADE, 
        related_name='transactions',
        verbose_name="Part of Agreement"
    )
    escrow_account_id = models.IntegerField(
        null=True, 
        blank=True,
        verbose_name="Escrow Account (if used)"
    )
    type = models.CharField(
        max_length=20, 
        choices=Type.choices,
        verbose_name="Transaction Type"
    )
    amount = models.DecimalField(
        max_digits=14, 
        decimal_places=2,
        verbose_name="Amount"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Transaction Date")

    class Meta:
        verbose_name = "Investment Transaction"
        verbose_name_plural = "Investment Transactions"

    def __str__(self):
        return f"{self.get_type_display()} - {self.amount}"


class InvestorReport(models.Model):
    project = models.ForeignKey(
        'projects.Project', 
        on_delete=models.CASCADE, 
        related_name='reports',
        verbose_name="For Project"
    )
    investor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='reports',
        verbose_name="Prepared For"
    )
    report_period = models.CharField(
        max_length=50,
        help_text="e.g. 'Q1 2026', 'January 2026'",
        verbose_name="Reporting Period"
    )
    performance_summary = models.TextField(
        verbose_name="Performance Summary"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Report Date")

    class Meta:
        verbose_name = "Investor Report"
        verbose_name_plural = "Investor Reports"

    def __str__(self):
        return f"Report for {self.investor.username} - {self.report_period}"
