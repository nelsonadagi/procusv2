from django.db import models
from django.conf import settings

class Project(models.Model):
    class Status(models.TextChoices):
        LISTED = 'LISTED', 'Listed'
        FUNDING_OPEN = 'FUNDING_OPEN', 'Funding Open'
        EXECUTION_STARTED = 'EXECUTION_STARTED', 'Execution Started'
        COMPLETED = 'COMPLETED', 'Completed'

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')
    category = models.ForeignKey('taxonomy.Category', on_delete=models.PROTECT, related_name='projects', limit_choices_to={'taxonomy_type': 'PROJECT'}, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    estimated_budget = models.DecimalField(max_digits=15, decimal_places=2)
    funding_required = models.BooleanField(default=False)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.LISTED)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ProjectRequirement(models.Model):
    class Type(models.TextChoices):
        MATERIAL = 'MATERIAL', 'Material'
        CONTRACTOR = 'CONTRACTOR', 'Contractor'
        SERVICE = 'SERVICE', 'Service'

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='requirements')
    type = models.CharField(max_length=20, choices=Type.choices)
    description = models.CharField(max_length=255)
    quantity = models.CharField(max_length=100) # e.g. "500 Bags", "2 Teams"

    def __str__(self):
        return f"{self.type} - {self.description}"

class InvestmentCommitment(models.Model):
    class Status(models.TextChoices):
        PLEDGED = 'PLEDGED', 'Pledged'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='commitments')
    investor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='commitments')
    amount_committed = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLEDGED)
    created_at = models.DateTimeField(auto_now_add=True)

class ProjectContractLink(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='linked_contracts')
    contract = models.ForeignKey('contracts.Contract', on_delete=models.CASCADE, related_name='linked_project')

class ProjectUpdate(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='updates')
    update_text = models.TextField()
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
