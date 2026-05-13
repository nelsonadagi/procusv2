#!/usr/bin/env python
"""
Diagnose country data integrity across the platform.

Run with:
    python manage.py diagnose_country_data

Reports:
- Country registry status
- Vendor country coverage
- Product country coverage
- Contract country coverage
- Project country coverage
- Products whose vendor country differs from product country
"""
from django.core.management.base import BaseCommand
from django.db.models import Count, Q, F
from platform_settings.models import Country
from vendors.models import Vendor
from catalog.models import Product
from contracts.models import Contract
from projects.models import Project


class Command(BaseCommand):
    help = "Diagnose country data integrity across all marketplace entities"

    def handle(self, *args, **options):
        self.stdout.write("=" * 60)
        self.stdout.write("COUNTRY DATA DIAGNOSIS")
        self.stdout.write("=" * 60)

        # 1. Country Registry
        countries = Country.objects.all()
        self.stdout.write(f"\n📍 Registered Countries: {countries.count()}")
        for c in countries:
            default_mark = " (DEFAULT)" if c.is_default else ""
            self.stdout.write(f"   • {c.flag_emoji} {c.name} — iso_code={c.iso_code}{default_mark}")

        if not countries.exists():
            self.stdout.write(self.style.ERROR("   ❌ NO COUNTRIES FOUND — seed platform_settings immediately!"))
            return

        default_country = countries.filter(is_default=True).first()
        if not default_country:
            self.stdout.write(self.style.WARNING("   ⚠️ No default country set!"))

        # 2. Vendor Country Coverage
        total_vendors = Vendor.objects.count()
        vendors_with_country = Vendor.objects.filter(country__isnull=False).count()
        vendors_without_country = total_vendors - vendors_with_country
        self.stdout.write(f"\n🏢 Vendors: {total_vendors} total")
        self.stdout.write(f"   • With country: {vendors_with_country}")
        self.stdout.write(f"   • Without country: {vendors_without_country}")
        if vendors_without_country > 0:
            self.stdout.write(self.style.WARNING(
                f"   ⚠️ {vendors_without_country} vendors missing country — products from these vendors "
                f"may have been backfilled with default country ({default_country.iso_code if default_country else 'N/A'})"
            ))

        # 3. Product Country Coverage
        total_products = Product.objects.count()
        products_with_country = Product.objects.filter(country__isnull=False).count()
        products_without_country = total_products - products_with_country
        self.stdout.write(f"\n📦 Products: {total_products} total")
        self.stdout.write(f"   • With country FK: {products_with_country}")
        self.stdout.write(f"   • Without country FK: {products_without_country}")

        # Products by country
        self.stdout.write("\n   Products by country:")
        for c in countries:
            count = Product.objects.filter(country=c).count()
            self.stdout.write(f"      {c.iso_code}: {count}")

        # 4. Products where product.country != vendor.country
        mismatched = Product.objects.filter(
            country__isnull=False,
            vendor__country__isnull=False
        ).exclude(country=F('vendor__country')).select_related('country', 'vendor__country')[:20]

        mismatched_count = Product.objects.filter(
            country__isnull=False,
            vendor__country__isnull=False
        ).exclude(country=F('vendor__country')).count()

        if mismatched_count:
            self.stdout.write(self.style.WARNING(
                f"\n⚠️ {mismatched_count} products have country DIFFERENT from vendor's country"
            ))
            for p in mismatched:
                self.stdout.write(
                    f"   • {p.name} (product={p.country.iso_code}, vendor={p.vendor.country.iso_code})"
                )
        else:
            self.stdout.write("\n✅ All products match their vendor's country")

        # 5. Products with country=NULL but vendor has country
        orphan_products = Product.objects.filter(
            country__isnull=True,
            vendor__country__isnull=False
        ).select_related('vendor__country')
        orphan_count = orphan_products.count()
        if orphan_count:
            self.stdout.write(self.style.WARNING(
                f"\n⚠️ {orphan_count} products have no country but vendor does — "
                f"these will show only when vendor's country is selected"
            ))

        # 6. Products with country=NULL and vendor.country=NULL
        double_null = Product.objects.filter(country__isnull=True, vendor__country__isnull=True).count()
        if double_null:
            self.stdout.write(self.style.ERROR(
                f"\n❌ {double_null} products have NO country AND vendor has no country — "
                f"these will DISAPPEAR when any country filter is applied"
            ))

        # 7. Contract & Project summary
        self.stdout.write(f"\n📋 Contracts: {Contract.objects.count()} total")
        self.stdout.write(f"   • With country: {Contract.objects.filter(country__isnull=False).count()}")
        self.stdout.write(f"   • Without country: {Contract.objects.filter(country__isnull=True).count()}")

        self.stdout.write(f"\n🏗️ Projects: {Project.objects.count()} total")
        self.stdout.write(f"   • With country: {Project.objects.filter(country__isnull=False).count()}")
        self.stdout.write(f"   • Without country: {Project.objects.filter(country__isnull=True).count()}")

        # 8. Vendor location_hierarchy insights
        vendors_with_hierarchy = Vendor.objects.exclude(location_hierarchy={}).exclude(location_hierarchy=None)
        self.stdout.write(f"\n📍 Vendors with location_hierarchy: {vendors_with_hierarchy.count()}")
        for v in vendors_with_hierarchy[:10]:
            hierarchy_country = v.location_hierarchy.get('country', 'N/A') if v.location_hierarchy else 'N/A'
            vendor_country = v.country.iso_code if v.country else 'NULL'
            if hierarchy_country != vendor_country and hierarchy_country != 'N/A':
                self.stdout.write(
                    f"   • {v.business_name}: hierarchy.country={hierarchy_country}, vendor.country={vendor_country}"
                )

        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("DIAGNOSIS COMPLETE")
        self.stdout.write("=" * 60)
