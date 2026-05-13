#!/usr/bin/env python
"""
Backfill and correct country data across vendors, products, contracts, and projects.

Uses vendor.location_hierarchy as the source of truth for vendor country inference.
Re-backfills product.country from vendor.country.

Run with:
    python manage.py fix_country_data --dry-run     # preview changes
    python manage.py fix_country_data               # apply changes
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q, F
from platform_settings.models import Country
from vendors.models import Vendor
from catalog.models import Product
from contracts.models import Contract
from projects.models import Project


COUNTRY_NAME_MAP = {
    'kenya': 'KE',
    'uganda': 'UG',
    'tanzania': 'TZ',
    'rwanda': 'RW',
    'burundi': 'BI',
    'south sudan': 'SS',
    'ethiopia': 'ET',
}


def infer_country_from_text(text):
    """Infer ISO code from free-text location."""
    if not text:
        return None
    text_lower = text.lower()
    for name, code in COUNTRY_NAME_MAP.items():
        if name in text_lower:
            return code
    return None


class Command(BaseCommand):
    help = "Backfill and correct country data across marketplace entities"

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Preview changes without writing to the database',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        mode = "DRY RUN" if dry_run else "LIVE"
        self.stdout.write("=" * 60)
        self.stdout.write(f"COUNTRY DATA FIX — {mode}")
        self.stdout.write("=" * 60)

        # Build country lookup caches
        countries_by_code = {c.iso_code.upper(): c for c in Country.objects.all()}
        countries_by_name = {}
        for c in Country.objects.all():
            countries_by_name[c.name.lower()] = c
            for alias, code in COUNTRY_NAME_MAP.items():
                if code == c.iso_code.upper():
                    countries_by_name[alias] = c

        if not countries_by_code:
            self.stdout.write(self.style.ERROR("❌ No countries in database. Run seed_platform_core first."))
            return

        # ── Step 1: Fix vendors without country ──
        self.stdout.write("\n🏢 Step 1: Fix vendors without country")
        vendors_to_fix = Vendor.objects.filter(country__isnull=True)
        vendor_fixes = 0

        for vendor in vendors_to_fix:
            inferred = None

            # Try location_hierarchy first
            if vendor.location_hierarchy:
                hierarchy_country = vendor.location_hierarchy.get('country')
                if hierarchy_country:
                    inferred = countries_by_name.get(hierarchy_country.lower())

            # Try location_text fallback
            if not inferred and vendor.location_text:
                code = infer_country_from_text(vendor.location_text)
                if code:
                    inferred = countries_by_code.get(code)

            # Try formatted_address fallback
            if not inferred and vendor.formatted_address:
                code = infer_country_from_text(vendor.formatted_address)
                if code:
                    inferred = countries_by_code.get(code)

            if inferred:
                self.stdout.write(
                    f"   {vendor.business_name}: NULL → {inferred.iso_code} "
                    f"(from {vendor.location_hierarchy.get('country') or vendor.location_text or vendor.formatted_address})"
                )
                if not dry_run:
                    vendor.country = inferred
                    vendor.save(update_fields=['country'])
                vendor_fixes += 1

        self.stdout.write(f"   Vendors fixed: {vendor_fixes}")

        # ── Step 2: Re-backfill product.country from vendor.country ──
        self.stdout.write("\n📦 Step 2: Re-backfill product.country from vendor.country")
        products_to_fix = Product.objects.filter(
            Q(country__isnull=True) | ~Q(country=F('vendor__country'))
        ).filter(vendor__country__isnull=False).select_related('vendor__country', 'country')

        product_fixes = 0
        for product in products_to_fix:
            vendor_country = product.vendor.country
            if product.country != vendor_country:
                old = product.country.iso_code if product.country else 'NULL'
                new = vendor_country.iso_code
                self.stdout.write(f"   {product.name}: {old} → {new}")
                if not dry_run:
                    product.country = vendor_country
                    product.save(update_fields=['country'])
                product_fixes += 1

        self.stdout.write(f"   Products fixed: {product_fixes}")

        # ── Step 3: Fix products still without country (vendor also has no country) ──
        self.stdout.write("\n📦 Step 3: Fix products with no country AND vendor with no country")
        orphan_products = Product.objects.filter(
            country__isnull=True, vendor__country__isnull=True
        ).select_related('vendor')

        orphan_fixes = 0
        for product in orphan_products:
            inferred = None
            if product.country_of_origin:
                inferred = countries_by_name.get(product.country_of_origin.lower())
            if not inferred:
                inferred = countries_by_code.get('KE')  # ultimate fallback

            old = 'NULL'
            new = inferred.iso_code if inferred else 'NULL'
            self.stdout.write(f"   {product.name}: {old} → {new} (orphan fallback)")
            if not dry_run and inferred:
                product.country = inferred
                product.save(update_fields=['country'])
            orphan_fixes += 1

        self.stdout.write(f"   Orphan products fixed: {orphan_fixes}")

        # ── Step 4: Fix contracts without country ──
        self.stdout.write("\n📋 Step 4: Fix contracts without country")
        contracts_to_fix = Contract.objects.filter(country__isnull=True).select_related('owner')
        contract_fixes = 0

        for contract in contracts_to_fix:
            inferred = None
            # Try owner's profile country if available
            if hasattr(contract.owner, 'profile') and contract.owner.profile:
                if getattr(contract.owner.profile, 'country', None):
                    inferred = contract.owner.profile.country

            # Try location text
            if not inferred and contract.location:
                code = infer_country_from_text(contract.location)
                if code:
                    inferred = countries_by_code.get(code)

            # Ultimate fallback: default country
            if not inferred:
                inferred = Country.objects.filter(is_default=True).first() or Country.objects.first()

            if inferred:
                self.stdout.write(f"   {contract.title}: NULL → {inferred.iso_code}")
                if not dry_run:
                    contract.country = inferred
                    contract.save(update_fields=['country'])
                contract_fixes += 1

        self.stdout.write(f"   Contracts fixed: {contract_fixes}")

        # ── Step 5: Fix projects without country ──
        self.stdout.write("\n🏗️ Step 5: Fix projects without country")
        projects_to_fix = Project.objects.filter(country__isnull=True).select_related('owner')
        project_fixes = 0

        for project in projects_to_fix:
            inferred = None
            # Try location_text
            if project.location_text:
                code = infer_country_from_text(project.location_text)
                if code:
                    inferred = countries_by_code.get(code)

            # Try formatted_address
            if not inferred and project.formatted_address:
                code = infer_country_from_text(project.formatted_address)
                if code:
                    inferred = countries_by_code.get(code)

            # Try owner's country
            if not inferred:
                if hasattr(project.owner, 'profile') and project.owner.profile:
                    if getattr(project.owner.profile, 'country', None):
                        inferred = project.owner.profile.country

            # Ultimate fallback
            if not inferred:
                inferred = Country.objects.filter(is_default=True).first() or Country.objects.first()

            if inferred:
                self.stdout.write(f"   {project.title}: NULL → {inferred.iso_code}")
                if not dry_run:
                    project.country = inferred
                    project.save(update_fields=['country'])
                project_fixes += 1

        self.stdout.write(f"   Projects fixed: {project_fixes}")

        # ── Summary ──
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("SUMMARY")
        self.stdout.write("=" * 60)
        self.stdout.write(f"Vendors fixed:      {vendor_fixes}")
        self.stdout.write(f"Products fixed:     {product_fixes}")
        self.stdout.write(f"Orphan products:    {orphan_fixes}")
        self.stdout.write(f"Contracts fixed:    {contract_fixes}")
        self.stdout.write(f"Projects fixed:     {project_fixes}")

        if dry_run:
            self.stdout.write(self.style.WARNING("\n⚠️ This was a dry run. No changes were saved."))
            self.stdout.write("Run without --dry-run to apply changes.")
        else:
            self.stdout.write(self.style.SUCCESS("\n✅ All changes applied."))

        self.stdout.write("=" * 60)
