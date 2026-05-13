#!/usr/bin/env python
"""
Wipes all marketplace data and re-runs the full seed suite.

WARNING: This deletes products, vendors, projects, contracts, tenders,
and all related data. User accounts and RBAC roles are preserved.

Run with:
    python manage.py reset_and_seed

Or inside Docker:
    docker-compose exec backend python manage.py reset_and_seed
"""
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = "Wipe marketplace data and re-seed from scratch"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("=" * 60))
        self.stdout.write(self.style.WARNING("  MARKETPLACE DATA RESET"))
        self.stdout.write(self.style.WARNING("=" * 60))

        # Import models here to avoid import-time DB queries
        from catalog.models import Product, ProductImage, ProductCertification, ProductAttribute, ProductDocument
        from vendors.models import Vendor
        from contractors.models import ContractorProfile
        from logistics.models import CourierProfile
        from projects.models import Project, ProjectRequirement, InvestmentCommitment, ProjectUpdate, ProjectContractLink
        from contracts.models import Contract
        from government.models import PublicTender
        from regulation.models import InvestorProfile, InvestmentAgreement

        deletion_steps = [
            ("Investment agreements", InvestmentAgreement),
            ("Investor profiles", InvestorProfile),
            ("Project contract links", ProjectContractLink),
            ("Project updates", ProjectUpdate),
            ("Investment commitments", InvestmentCommitment),
            ("Project requirements", ProjectRequirement),
            ("Projects", Project),
            ("Contracts", Contract),
            ("Public tenders", PublicTender),
            ("Product certifications", ProductCertification),
            ("Product attributes", ProductAttribute),
            ("Product documents", ProductDocument),
            ("Product images", ProductImage),
            ("Products", Product),
            ("Contractor profiles", ContractorProfile),
            ("Courier profiles", CourierProfile),
            ("Vendor profiles", Vendor),
        ]

        for label, model in deletion_steps:
            try:
                model.objects.all().delete()
                self.stdout.write(f"  🗑️  Cleared {label}")
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"  ⚠️  Could not clear {label}: {e}"))

        self.stdout.write("\n" + self.style.SUCCESS("✅ Marketplace data wiped.") + "\n")

        # Re-seed
        self.stdout.write(self.style.NOTICE("🌱 Re-seeding data...\n"))

        import seed_data
        seed_data.run_all()

        self.stdout.write("\n" + self.style.SUCCESS("=" * 60))
        self.stdout.write(self.style.SUCCESS("  RESET & SEED COMPLETE"))
        self.stdout.write(self.style.SUCCESS("=" * 60))
        self.stdout.write("\nDefault credentials:")
        self.stdout.write("  Admin:    admin / adminpassword123")
        self.stdout.write("  Others:   <username> / password123")
