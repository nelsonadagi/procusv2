#!/usr/bin/env python
"""
Dedicated seed script for marketplace workflow data.
Safe to rerun independently; all writes are idempotent.
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from seed_data import (
    log_seed_banner,
    seed_taxonomy,
    seed_users,
    seed_vendors,
    seed_products,
    seed_projects_and_contracts,
    seed_government_tenders,
    seed_investor_data,
)


def run():
    log_seed_banner("🏗️ Starting Marketplace Workflow Seed")
    categories = seed_taxonomy()
    users = seed_users()
    vendors = seed_vendors(users, categories)
    seed_products(vendors, categories)
    project = seed_projects_and_contracts(users)
    seed_government_tenders()
    seed_investor_data(users, project)
    log_seed_banner("✅ Marketplace Workflow Seed Complete")


if __name__ == '__main__':
    run()
