#!/usr/bin/env python
"""
Seed script for logistics data - Carriers, Courier Profiles, Pricing Zones.
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

import logging
from decimal import Decimal
from django.contrib.auth import get_user_model

from logistics.models import Carrier, CourierProfile, PricingZone, PricingRule

User = get_user_model()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def seed_couriers():
    """Create courier users and profiles."""
    couriers_data = [
        {
            'username': 'g4s_admin',
            'email': 'admin@g4s.ke',
            'company_name': 'G4S Logistics Kenya',
            'registration_number': 'REG-G4S-001',
            'support_email': 'support@g4s.ke',
            'support_phone': '+254700000001',
            'code': 'G4S',
        },
        {
            'username': 'dhl_admin',
            'email': 'admin@dhl.ke',
            'company_name': 'DHL Express Kenya',
            'registration_number': 'REG-DHL-001',
            'support_email': 'support@dhl.ke',
            'support_phone': '+254700000002',
            'code': 'DHL',
        },
        {
            'username': 'sendy_admin',
            'email': 'admin@sendy.co.ke',
            'company_name': 'Sendy Ltd',
            'registration_number': 'REG-SENDY-001',
            'support_email': 'support@sendy.co.ke',
            'support_phone': '+254700000003',
            'code': 'SENDY',
        },
    ]
    
    created_profiles = []
    
    for data in couriers_data:
        # Create user
        user, user_created = User.objects.get_or_create(
            username=data['username'],
            defaults={
                'email': data['email'],
                'role': 'COURIER',
                'first_name': data['company_name'].split()[0],
                'last_name': 'Logistics'
            }
        )
        if user_created:
            user.set_password('courier123')
            user.save()
            logger.info(f"✅ Courier user created: {data['username']}/courier123")
        
        # Create courier profile
        profile, profile_created = CourierProfile.objects.get_or_create(
            user=user,
            defaults={
                'company_name': data['company_name'],
                'registration_number': data['registration_number'],
                'support_email': data['support_email'],
                'support_phone': data['support_phone'],
                'status': 'APPROVED',
                'is_active': True,
                'latitude': -1.2921,
                'longitude': 36.8219,
                'location_text': 'Nairobi, Kenya'
            }
        )
        if profile_created:
            logger.info(f"✅ Courier profile created: {data['company_name']}")
        
        created_profiles.append((profile, data['code']))
        
        # Create legacy Carrier entry (for backward compatibility)
        carrier, carrier_created = Carrier.objects.get_or_create(
            code=data['code'],
            defaults={
                'name': data['company_name'],
                'is_active': True,
                'profile': profile
            }
        )
        if carrier_created:
            logger.info(f"✅ Carrier entry created: {data['code']}")
    
    return created_profiles


def seed_pricing_zones(courier_profiles):
    """Create pricing zones and rules for each courier."""
    zones_data = [
        {
            'name': 'Nairobi Central',
            'zone_type': 'RADIUS',
            'center_lat': -1.2921,
            'center_lng': 36.8219,
            'radius_km': 10.0,
            'base_cost': Decimal('300.00'),
            'per_kg_cost': Decimal('50.00'),
        },
        {
            'name': 'Mombasa Island',
            'zone_type': 'RADIUS',
            'center_lat': -4.0435,
            'center_lng': 39.6682,
            'radius_km': 15.0,
            'base_cost': Decimal('500.00'),
            'per_kg_cost': Decimal('70.00'),
        },
        {
            'name': 'Kisumu City',
            'zone_type': 'RADIUS',
            'center_lat': -0.0917,
            'center_lng': 34.7680,
            'radius_km': 12.0,
            'base_cost': Decimal('600.00'),
            'per_kg_cost': Decimal('80.00'),
        },
        {
            'name': 'Nakuru Town',
            'zone_type': 'RADIUS',
            'center_lat': -0.3031,
            'center_lng': 36.0800,
            'radius_km': 8.0,
            'base_cost': Decimal('450.00'),
            'per_kg_cost': Decimal('60.00'),
        },
    ]
    
    for profile, code in courier_profiles:
        for zone_data in zones_data:
            # Make a copy to avoid modifying the original data
            zone_data_copy = zone_data.copy()
            pricing_data = {
                'base_cost': zone_data_copy.pop('base_cost'),
                'per_kg_cost': zone_data_copy.pop('per_kg_cost'),
            }
            zone_name = f"{profile.company_name} - {zone_data_copy['name']}"
            
            # Create zone
            zone, zone_created = PricingZone.objects.get_or_create(
                courier=profile,
                name=zone_data_copy['name'],
                defaults=zone_data_copy
            )
            if zone_created:
                logger.info(f"✅ Pricing zone created: {zone_name}")
            
            # Create pricing rule
            rule, rule_created = PricingRule.objects.get_or_create(
                courier=profile,
                zone=zone,
                defaults={
                    'base_cost': pricing_data['base_cost'],
                    'per_kg_cost': pricing_data['per_kg_cost'],
                    'min_weight': Decimal('0.00'),
                    'max_weight': Decimal('1000.00'),
                    'is_active': True
                }
            )
            if rule_created:
                logger.info(f"✅ Pricing rule created for: {zone_name}")


def run():
    """Main entry point for logistics seeding."""
    logger.info("=" * 50)
    logger.info("🚚 Starting Logistics Data Seeding")
    logger.info("=" * 50)
    
    try:
        # Seed couriers and get profiles
        profiles = seed_couriers()
        
        # Seed pricing zones
        seed_pricing_zones(profiles)
        
        logger.info("=" * 50)
        logger.info("✅ Logistics Seeding Complete!")
        logger.info("=" * 50)
        
    except Exception as e:
        logger.error(f"❌ Logistics seeding failed: {e}")
        raise


if __name__ == '__main__':
    run()
