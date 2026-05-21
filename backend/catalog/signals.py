from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from notifications.services import notify_user
from .models import ProductCertification


@receiver(post_save, sender=ProductCertification)
def notify_certification_added(sender, instance, created, **kwargs):
    """Notify vendor when a certification is added to their product."""
    if created and instance.product and instance.product.vendor:
        vendor = instance.product.vendor
        notify_user(
            vendor.user,
            'SYSTEM',
            f"Certification added to {instance.product.name}",
            f"{instance.display_name or instance.registry.name if instance.registry else 'Certification'} was added.",
            data={"product_uuid": str(instance.product.uuid), "action": "view_product"},
        )


def check_expiring_certifications():
    """Check for certifications expiring within 30 days and notify vendors.
    This function is designed to be called from a cron job or Celery task.
    """
    from .models import ProductCertification

    threshold = timezone.now().date() + timedelta(days=30)
    expiring = ProductCertification.objects.filter(
        expires_on__lte=threshold,
        expires_on__gte=timezone.now().date(),
        product__status='ACTIVE',
    ).select_related('product', 'product__vendor', 'product__vendor__user', 'registry')

    notified = 0
    for cert in expiring:
        vendor = cert.product.vendor
        if not vendor or not vendor.user:
            continue

        days_left = (cert.expires_on - timezone.now().date()).days
        urgency = "urgently" if days_left <= 7 else "soon"

        notify_user(
            vendor.user,
            'SYSTEM',
            f"Certification expiring {urgency}: {cert.product.name}",
            f"{cert.display_name or cert.registry.name if cert.registry else 'Certification'} expires in {days_left} days. Renew to maintain compliance and buyer trust.",
            data={"product_uuid": str(cert.product.uuid), "action": "view_product", "cert_id": cert.id},
        )
        notified += 1

    return notified
