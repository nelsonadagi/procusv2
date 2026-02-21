from django.db import models
from django.conf import settings

class FinanceProduct(models.Model):
    name = models.CharField(max_length=255) # Material Credit, etc.
    provider_name = models.CharField(max_length=255)
    max_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2) # e.g. 5.50
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class FinanceApplication(models.Model):
    class Status(models.TextChoices):
        SUBMITTED = 'SUBMITTED', 'Submitted'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'
        DISBURSED = 'DISBURSED', 'Disbursed'

    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='finance_applications')
    product = models.ForeignKey(FinanceProduct, on_delete=models.CASCADE)
    requested_amount = models.DecimalField(max_digits=12, decimal_places=2)
    purpose = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SUBMITTED)
    created_at = models.DateTimeField(auto_now_add=True)

class FinanceLoan(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        REPAID = 'REPAID', 'Repaid'
        DEFAULT = 'DEFAULT', 'Default'

    application = models.OneToOneField(FinanceApplication, on_delete=models.CASCADE, related_name='loan')
    principal_amount = models.DecimalField(max_digits=12, decimal_places=2)
    disbursed_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    repayment_due_date = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)

class FinanceRepayment(models.Model):
    loan = models.ForeignKey(FinanceLoan, on_delete=models.CASCADE, related_name='repayments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)
    payment_reference = models.CharField(max_length=255)

class SupplierCreditLine(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        SUSPENDED = 'SUSPENDED', 'Suspended'

    vendor = models.OneToOneField('vendors.Vendor', on_delete=models.CASCADE, related_name='credit_line')
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2)
    available_balance = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
