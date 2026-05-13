from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Contract(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('⏳ Draft - Pending Review')
        POSTED = 'POSTED', _('📢 Posted - Accepting Bids')
        BIDDING = 'BIDDING', _('🏆 Bidding in Progress')
        AWARDED = 'AWARDED', _('🎯 Contractor Selected')
        IN_PROGRESS = 'IN_PROGRESS', _('🏗️ Work in Progress')
        COMPLETED = 'COMPLETED', _('✅ Successfully Completed')

    class Currency(models.TextChoices):
        KES = 'KES', _('Kenyan Shilling')
        USD = 'USD', _('US Dollar')
        EUR = 'EUR', _('Euro')

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='contracts',
        verbose_name="Posted By"
    )
    title = models.CharField(max_length=255, verbose_name="Job Title")
    description_scope = models.TextField(
        verbose_name="Scope of Work",
        help_text="Detailed description of the work required"
    )
    location = models.CharField(max_length=255, verbose_name="Work Location")
    budget_min = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Minimum Budget"
    )
    budget_max = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Maximum Budget"
    )
    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.KES,
        verbose_name="Currency"
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Contract Status"
    )

    # Scheduling
    bid_deadline = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Bid Submission Deadline"
    )
    project_start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Project Start Date"
    )
    project_end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Project Completion Date"
    )

    # Geography
    country = models.ForeignKey(
        'platform_settings.Country',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contracts',
        verbose_name="Country"
    )

    # Categorization
    category = models.ForeignKey(
        'taxonomy.Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contracts',
        verbose_name="Work Category"
    )

    # Media
    featured_image = models.ImageField(
        upload_to='contract_images/%Y/%m/',
        null=True,
        blank=True,
        verbose_name="Featured Image"
    )

    # Terms
    payment_terms = models.TextField(
        blank=True,
        verbose_name="Payment Terms",
        help_text="e.g. '30% advance, 40% at midpoint, 30% on completion'"
    )
    eligibility_criteria = models.TextField(
        blank=True,
        verbose_name="Eligibility Criteria",
        help_text="Minimum contractor class, experience, insurance requirements"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Posted On")

    class Meta:
        verbose_name = "Work Contract"
        verbose_name_plural = "Work Contracts"

    def __str__(self):
        return self.title


class ContractAttachment(models.Model):
    class AttachmentType(models.TextChoices):
        DRAWING = 'DRAWING', _('Drawings')
        BOQ = 'BOQ', _('Bill of Quantities')
        SPEC = 'SPEC', _('Technical Specification')
        REPORT = 'REPORT', _('Site Report')
        PHOTO = 'PHOTO', _('Site Photo')
        OTHER = 'OTHER', _('Other')

    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE,
        related_name='attachments',
        verbose_name="Contract"
    )
    file = models.FileField(
        upload_to='contract_attachments/%Y/%m/',
        verbose_name="Attachment File"
    )
    attachment_type = models.CharField(
        max_length=20,
        choices=AttachmentType.choices,
        default=AttachmentType.OTHER,
        verbose_name="Type"
    )
    title = models.CharField(
        max_length=255,
        verbose_name="Title"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Uploaded On")

    class Meta:
        verbose_name = "Contract Attachment"
        verbose_name_plural = "Contract Attachments"
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.title} ({self.contract.title})"
