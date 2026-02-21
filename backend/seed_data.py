import os
import django
import sys
from datetime import timedelta
from django.utils import timezone

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from accounts.models import User
from vendors.models import Vendor
from taxonomy.models import Category
from catalog.models import Product
from projects.models import Project
from contracts.models import Contract
from government.models import PublicTender
from regulation.models import InvestorProfile, InvestmentAgreement

User = get_user_model()

def seed():
    print("Starting data seeding...")

    # 1. Create Admin User
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@ujenzi.com',
            password='adminpassword123',
            first_name='System',
            last_name='Administrator',
            role='ADMIN'
        )
        print("✅ Admin created (admin/adminpassword123)")
    else:
        admin = User.objects.get(username='admin')
    
    admin_group, _ = Group.objects.get_or_create(name='ADMIN')
    admin.groups.add(admin_group)
    print("✅ Admin synchronized with ADMIN group")

    # 2. Create Users for different roles
    roles = [
        ('owner', 'owner@example.com', 'PROJECT_OWNER', 'Alice', 'Owner'),
        ('contractor', 'builder@example.com', 'CONTRACTOR', 'Bob', 'Builder'),
        ('vendor', 'supplier@example.com', 'VENDOR', 'Charlie', 'Supplier'),
        ('investor', 'capital@example.com', 'INVESTOR', 'David', 'Investor'),
        ('gov', 'tender@gov.com', 'GOVERNMENT', 'Gov', 'Authority'),
    ]

    groups = {
        'PROJECT_OWNER': 'PROJECT_OWNER',
        'CONTRACTOR': 'CONTRACTOR',
        'VENDOR': 'VENDOR',
        'INVESTOR': 'INVESTOR',
        'GOVERNMENT': 'GOVERNMENT_OWNER',
        'ADMIN': 'ADMIN'
    }

    users = {}
    for uname, email, role, fname, lname in roles:
        user, created = User.objects.get_or_create(
            username=uname,
            defaults={
                'email': email,
                'role': role,
                'first_name': fname,
                'last_name': lname,
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            
        # Assign to Django Group for RBAC
        group_name = groups.get(role)
        if group_name:
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
            
        print(f"✅ User synchronized: {uname} ({role}) -> Group: {group_name}")
        users[role] = user

    # 3. Create Vendor Profile
    vendor_profile, created = Vendor.objects.get_or_create(
        user=users['VENDOR'],
        defaults={
            'business_name': 'Global Construction Supplies',
            'registration_number': 'REG123456',
            'verified_status': 'APPROVED',
            'location': 'Nairobi, Kenya'
        }
    )
    if created: print("✅ Vendor profile created")

    # 4. Create Categories and Products
    cement_cat = Category.objects.get(name='Cement', taxonomy_type='MATERIAL')
    steel_cat = Category.objects.get(name='Steel', taxonomy_type='MATERIAL')

    products_data = [
        (vendor_profile, cement_cat, 'Dangote Cement 50kg', 'Strong Grade 42.5 cement.', 'Bag', 8.50, 1000),
        (vendor_profile, steel_cat, 'TMT Steel Bar 12mm', 'High strength reinforced steel bars.', 'Piece', 12.00, 500),
        (vendor_profile, cement_cat, 'River Sand (10 Ton)', 'Clean sieved river sand.', 'Truck', 150.00, 20),
    ]

    for v, cat, name, desc, unit, price, stock in products_data:
        Product.objects.get_or_create(
            name=name,
            defaults={
                'vendor': v,
                'category': cat,
                'description': desc,
                'unit': unit,
                'base_price': price,
                'stock_quantity': stock,
                'delivery_regions': ['NAIROBI', 'MOMBASA', 'KISUMU']
            }
        )
    print("✅ Catalog items seeded")

    # 5. Create Projects
    project, created = Project.objects.get_or_create(
        owner=users['PROJECT_OWNER'],
        title='Skyline Apartment Wing A',
        defaults={
            'description': 'A 12-story residential development in Westlands.',
            'location': 'Westlands, Nairobi',
            'estimated_budget': 1500000.00,
            'status': 'FUNDING_OPEN'
        }
    )
    if created: print("✅ Sample Project created")

    # 6. Create Contracts
    Contract.objects.get_or_create(
        owner=users['PROJECT_OWNER'],
        title='Masonry and Foundation Works - Wing A',
        defaults={
            'description_scope': 'Complete foundation excavation and masonry for first 3 floors.',
            'location': 'Westlands, Nairobi',
            'budget_min': 50000.00,
            'budget_max': 75000.00,
            'status': 'BIDDING'
        }
    )
    print("✅ Contract opportunities seeded")

    # 7. Create Public Tenders
    PublicTender.objects.get_or_create(
        title='Expressway Maintenance Project - 2026',
        defaults={
            'description': 'Routine maintenance of the Nairobi-Mombasa highway segments.',
            'issuing_authority': 'Roads Authority (KENHA)',
            'bid_deadline': timezone.now() + timedelta(days=30),
            'status': 'OPEN'
        }
    )
    print("✅ Public Tenders seeded")

    # 8. Investor Setup
    inv_profile, _ = InvestorProfile.objects.get_or_create(
        user=users['INVESTOR'],
        defaults={
            'kyc_status': 'VERIFIED',
            'accreditation_status': 'ACCREDITED',
            'jurisdiction': 'Kenya'
        }
    )
    
    InvestmentAgreement.objects.get_or_create(
        project=project,
        investor=users['INVESTOR'],
        amount=50000.00,
        defaults={
            'status': 'DRAFT'
        }
    )
    print("✅ Investor data seeded")

    print("\n🚀 Seeding Complete!")

if __name__ == '__main__':
    seed()
