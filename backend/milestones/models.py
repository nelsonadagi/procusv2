from django.db import models

class Milestone(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        COMPLETED = 'COMPLETED', 'Completed' # Contractor claims done
        APPROVED = 'APPROVED', 'Approved' # Owner confirms
        PAID = 'PAID', 'Paid'

    contract = models.ForeignKey('contracts.Contract', on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    def __str__(self):
        return f"{self.title} - {self.contract.title}"

class MilestonePayment(models.Model):
    milestone = models.OneToOneField(Milestone, on_delete=models.CASCADE, related_name='payment')
    payment_reference = models.CharField(max_length=255, blank=True)
    release_status = models.CharField(max_length=50, default='PENDING') # Placeholder
