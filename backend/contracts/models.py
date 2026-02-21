from django.db import models
from django.conf import settings

class Contract(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending Approval'
        POSTED = 'POSTED', 'Posted'
        BIDDING = 'BIDDING', 'Bidding'
        AWARDED = 'AWARDED', 'Awarded'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contracts')
    title = models.CharField(max_length=255)
    description_scope = models.TextField()
    location = models.CharField(max_length=255)
    budget_min = models.DecimalField(max_digits=12, decimal_places=2)
    budget_max = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
