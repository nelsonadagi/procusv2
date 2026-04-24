from django.db import models
from django.utils.translation import gettext_lazy as _


class Bid(models.Model):
    class Status(models.TextChoices):
        SUBMITTED = 'SUBMITTED', _('📤 Bid Submitted')
        SHORTLISTED = 'SHORTLISTED', _('⭐ Shortlisted')
        REJECTED = 'REJECTED', _('❌ Not Selected')
        AWARDED = 'AWARDED', _('🏆 Bid Won!')

    contract = models.ForeignKey(
        'contracts.Contract', 
        on_delete=models.CASCADE, 
        related_name='bids',
        verbose_name="For Contract"
    )
    contractor = models.ForeignKey(
        'contractors.ContractorProfile', 
        on_delete=models.CASCADE, 
        related_name='bids',
        verbose_name="Submitted By"
    )
    proposed_cost = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        verbose_name="Proposed Price"
    )
    proposed_timeline_days = models.IntegerField(
        verbose_name="Estimated Timeline (days)"
    )
    message = models.TextField(
        blank=True,
        verbose_name="Cover Letter / Proposal"
    )
    status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.SUBMITTED,
        verbose_name="Bid Status"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Submitted On")

    class Meta:
        verbose_name = "Contractor Bid"
        verbose_name_plural = "Contractor Bids"

    def __str__(self):
        return f"Bid by {self.contractor.company_name} for {self.contract.title}"
