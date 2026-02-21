from django.db import models

class Delivery(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        DISPATCHED = 'DISPATCHED', 'Dispatched'
        DELIVERED = 'DELIVERED', 'Delivered'

    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE, related_name='delivery')
    delivery_status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    delivery_address = models.TextField()
    delivered_at = models.DateTimeField(null=True, blank=True)
