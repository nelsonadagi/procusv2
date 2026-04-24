#!/usr/bin/env python
"""
Create additional descriptive users for testing.
This complements seed_data.py by creating more test accounts.
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

import logging
from django.contrib.auth import get_user_model

User = get_user_model()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s', stream=sys.stdout)


def log_seed_banner(title):
    logger.info("=" * 60)
    logger.info(title)
    logger.info("=" * 60)


def create_additional_users():
    """Create additional descriptive users for testing the approval-driven role model."""
    users_to_create = [
        ('owner_jane', 'owner_jane@ujenzi.com', 'PROJECT_OWNER', [], 'Jane', 'Owner'),
        ('vendor_mall', 'vendor_mall@ujenzi.com', 'PROJECT_OWNER', ['VENDOR'], 'Mall', 'Supplier'),
        ('contractor_expert', 'contractor_expert@ujenzi.com', 'PROJECT_OWNER', ['CONTRACTOR'], 'Expert', 'Builder'),
        ('investor_wealth', 'investor_wealth@ujenzi.com', 'PROJECT_OWNER', ['INVESTOR'], 'Wealth', 'Capital'),
        ('property_ops', 'property_ops@ujenzi.com', 'PROJECT_OWNER', ['PROPERTY_MANAGER'], 'Pat', 'Property'),
        ('gov_authority', 'gov_authority@ujenzi.com', 'PROJECT_OWNER', ['GOVERNMENT'], 'Gov', 'Official'),
        ('admin_plus', 'admin_plus@ujenzi.com', 'ADMIN', [], 'Plus', 'Admin'),
        ('courier_fast', 'courier@fast.ke', 'PROJECT_OWNER', ['COURIER'], 'Fast', 'Delivery'),
    ]

    password = 'Starten1@'

    log_seed_banner("👥 Starting Descriptive User Seed")
    
    for username, email, primary_role, approved_roles, first_name, last_name in users_to_create:
        user, created = User.objects.update_or_create(
            username=username,
            defaults={
                'email': email,
                'role': primary_role,
                'first_name': first_name,
                'last_name': last_name,
            },
        )
        user.set_password(password)
        if primary_role == User.Role.ADMIN:
            user.role = User.Role.ADMIN
            user.roles = []
            user.is_staff = True
        else:
            user.role = User.Role.PROJECT_OWNER
            user.roles = []
            user.is_staff = False
        user.save(update_fields=['password', 'role', 'roles', 'is_staff'])

        for approved_role in approved_roles:
            user.grant_role(approved_role)
        
        status = "Created" if created else "Updated password for"
        logger.info(f"✅ {status} {username} (Primary: {user.role}, Approved: {user.roles})")

    logger.info(f"\n✅ All additional users created with password: {password}")
    log_seed_banner("✅ Descriptive User Seed Complete")


if __name__ == '__main__':
    create_additional_users()
