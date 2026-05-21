from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from notifications.services import notify_user
from catalog.models import ProductCertification


class Command(BaseCommand):
    help = "Check all product certifications for upcoming expiry and notify vendors."

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Number of days before expiry to trigger notification (default: 30)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Print what would be done without creating notifications.',
        )

    def handle(self, *args, **options):
        days = options['days']
        dry_run = options['dry_run']
        threshold = timezone.now().date() + timedelta(days=days)

        expiring = ProductCertification.objects.filter(
            expires_on__lte=threshold,
            expires_on__gte=timezone.now().date(),
        ).select_related('product', 'product__vendor', 'product__vendor__user', 'registry')

        notified = 0
        for cert in expiring:
            vendor = cert.product.vendor
            if not vendor or not vendor.user:
                continue

            product_name = cert.product.name
            cert_name = cert.display_name or (cert.registry.name if cert.registry else 'Certification')
            expiry_date = cert.expires_on

            message = (
                f"Your {cert_name} certification for {product_name} "
                f"expires on {expiry_date}. Renew to maintain compliance."
            )

            if dry_run:
                self.stdout.write(
                    f"[DRY-RUN] Would notify {vendor.user.email}: {message}"
                )
                continue

            notify_user(
                vendor.user,
                'SYSTEM',
                f"Certification expiring soon: {cert_name}",
                message,
                data={
                    "product_uuid": str(cert.product.uuid),
                    "cert_id": cert.id,
                    "expires_on": str(expiry_date),
                },
            )
            notified += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Checked {expiring.count()} certifications. "
                f"{'Would notify' if dry_run else 'Notified'} {notified} vendors."
            )
        )
