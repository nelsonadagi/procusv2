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
    status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.PENDING,
        verbose_name="Contract Status"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Posted On")

    class Meta:
        verbose_name = "Work Contract"
        verbose_name_plural = "Work Contracts"

    def __str__(self):
        return self.title
