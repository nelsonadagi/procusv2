from django.db import models

class Bid(models.Model):
    class Status(models.TextChoices):
        SUBMITTED = 'SUBMITTED', 'Submitted'
        SHORTLISTED = 'SHORTLISTED', 'Shortlisted'
        REJECTED = 'REJECTED', 'Rejected'
        AWARDED = 'AWARDED', 'Awarded'

    contract = models.ForeignKey('contracts.Contract', on_delete=models.CASCADE, related_name='bids')
    contractor = models.ForeignKey('contractors.ContractorProfile', on_delete=models.CASCADE, related_name='bids')
    proposed_cost = models.DecimalField(max_digits=12, decimal_places=2)
    proposed_timeline_days = models.IntegerField()
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SUBMITTED)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid {self.id} for {self.contract.title}"
