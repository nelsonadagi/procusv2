#!/usr/bin/env python
"""
Dedicated seed script for platform core data.
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
    seed_countries,
    seed_taxonomy,
    seed_users,
    seed_vendors,
    seed_contractor,
    seed_courier,
)


def run():
    log_seed_banner("🌍 Starting Platform Core Seed")
    seed_countries()
    categories = seed_taxonomy()
    users = seed_users()
    seed_vendors(users, categories)
    seed_contractor(users)
    seed_courier(users)
    log_seed_banner("✅ Platform Core Seed Complete")


if __name__ == '__main__':
    run()
