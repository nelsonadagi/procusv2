from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Project(models.Model):
    class Status(models.TextChoices):
        LISTED = 'LISTED', _('📋 Planning Phase')
        FUNDING_OPEN = 'FUNDING_OPEN', _('💰 Seeking Investment')
        EXECUTION_STARTED = 'EXECUTION_STARTED', _('🏗️ Construction in Progress')
        COMPLETED = 'COMPLETED', _('✅ Project Complete')

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='projects',
        verbose_name="Project Owner"
    )
    category = models.ForeignKey(
        'taxonomy.Category', 
        on_delete=models.PROTECT, 
        related_name='projects', 
        limit_choices_to={'taxonomy_type': 'PROJECT'}, 
        null=True, 
        blank=True,
        verbose_name="Project Type"
    )
    title = models.CharField(max_length=255, verbose_name="Project Name")
    description = models.TextField(verbose_name="Project Description")
    
    # Location Intelligence
    country = models.ForeignKey(
        'platform_settings.Country', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='projects',
        verbose_name="Country"
    )
    location_text = models.CharField(
        max_length=255, 
        db_column='location', 
        null=True, 
        blank=True,
        verbose_name="Project Location"
    )
    location = models.ForeignKey(
        'platform_settings.Location', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='projects',
        verbose_name="Location Details"
    )
    latitude = models.DecimalField(
        max_digits=12, 
        decimal_places=9, 
        null=True, 
        blank=True,
        verbose_name="GPS Latitude"
    )
    longitude = models.DecimalField(
        max_digits=12, 
        decimal_places=9, 
        null=True, 
        blank=True,
        verbose_name="GPS Longitude"
    )
    formatted_address = models.TextField(blank=True, verbose_name="Full Address")
    
    estimated_budget = models.DecimalField(
        max_digits=15, 
        decimal_places=2,
        verbose_name="Estimated Total Budget"
    )
    funding_required = models.BooleanField(
        default=False,
        verbose_name="Seeking Investment"
    )
    status = models.CharField(
        max_length=30, 
        choices=Status.choices, 
        default=Status.LISTED,
        verbose_name="Project Status"
    )
    cover_photo = models.ImageField(
        upload_to='project_covers/%Y/%m/',
        null=True,
        blank=True,
        verbose_name="Cover Photo"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created On")

    class Meta:
        verbose_name = "Construction Project"
        verbose_name_plural = "Construction Projects"

    def __str__(self):
        return self.title


class ProjectRequirement(models.Model):
    class Type(models.TextChoices):
        MATERIAL = 'MATERIAL', _('📦 Building Materials')
        CONTRACTOR = 'CONTRACTOR', _('👷 Skilled Contractor')
        SERVICE = 'SERVICE', _('🔧 Professional Service')

    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name='requirements',
        verbose_name="For Project"
    )
    type = models.CharField(
        max_length=20, 
        choices=Type.choices,
        verbose_name="What's Needed"
    )
    description = models.CharField(
        max_length=255,
        verbose_name="Specific Requirements"
    )
    quantity = models.CharField(
        max_length=100,
        help_text="e.g. '500 Bags of Cement', '2 Teams of Masons'",
        verbose_name="Quantity / Scale"
    )

    class Meta:
        verbose_name = "Project Requirement"
        verbose_name_plural = "Project Requirements"

    def __str__(self):
        return f"{self.get_type_display()} - {self.description}"


class InvestmentCommitment(models.Model):
    class Status(models.TextChoices):
        PLEDGED = 'PLEDGED', _('🤝 Investment Pledged')
        CONFIRMED = 'CONFIRMED', _('✅ Funds Committed')
        CANCELLED = 'CANCELLED', _('❌ Cancelled')

    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name='commitments',
        verbose_name="Project"
    )
    investor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='commitments',
        verbose_name="Investor"
    )
    amount_committed = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        verbose_name="Investment Amount"
    )
    status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.PLEDGED,
        verbose_name="Commitment Status"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Pledged On")

    class Meta:
        verbose_name = "Investment Commitment"
        verbose_name_plural = "Investment Commitments"

    def __str__(self):
        return f"{self.investor.username} - {self.amount_committed}"


class ProjectContractLink(models.Model):
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name='linked_contracts',
        verbose_name="Project"
    )
    contract = models.ForeignKey(
        'contracts.Contract', 
        on_delete=models.CASCADE, 
        related_name='linked_project',
        verbose_name="Related Contract"
    )

    class Meta:
        verbose_name = "Project Contract Link"
        verbose_name_plural = "Project Contract Links"


class ProjectUpdate(models.Model):
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name='updates',
        verbose_name="Project"
    )
    update_text = models.TextField(verbose_name="Update Message")
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name="Posted By"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Posted On")

    class Meta:
        verbose_name = "Project Update"
        verbose_name_plural = "Project Updates"
        ordering = ['-created_at']

    def __str__(self):
        return f"Update on {self.project.title} - {self.created_at.date()}"
