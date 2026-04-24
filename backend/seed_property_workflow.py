#!/usr/bin/env python
"""
Dedicated seed script for property workflow samples.
Safe to rerun independently; all writes are idempotent.
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

import logging
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils import timezone

from finance.models import FinanceApplication, FinanceProduct
from platform_settings.models import Country, Location
from projects.models import Project
from property.models import (
    PropertyAppointment,
    PropertyAvailabilityWindow,
    PropertyInquiry,
    PropertyListing,
    DevelopmentMetadata,
    PropertySpecification,
    PropertyFeature,
    PropertyMediaAsset,
    PropertyOwnershipProfile,
    PropertyPricingProfile,
    PropertyShowing,
    PropertyProjectLink,
)
from taxonomy.models import Category, TaxonomyType

User = get_user_model()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s', stream=sys.stdout)


def log_seed_banner(title):
    logger.info("=" * 60)
    logger.info(title)
    logger.info("=" * 60)


def log_seed_result(label, identifier, created):
    action = "created" if created else "updated"
    logger.info(f"✅ {label} {action}: {identifier}")


PROPERTY_PURPOSES = [
    (1, "Residential", "RES", None, "Main", "Residential"),
    (2, "Single-family homes", "SFH", "RES", "Sub", "Residential"),
    (3, "Apartments", "APT", "RES", "Sub", "Residential"),
    (4, "Condominiums", "CON", "RES", "Sub", "Residential"),
    (5, "Townhouses", "TWH", "RES", "Sub", "Residential"),
    (6, "Duplexes", "DUP", "RES", "Sub", "Residential"),
    (7, "Commercial", "COM", None, "Main", "Commercial"),
    (8, "Office buildings", "OFB", "COM", "Sub", "Commercial"),
    (9, "Retail spaces", "RET", "COM", "Sub", "Commercial"),
    (10, "Restaurants", "RST", "COM", "Sub", "Commercial"),
    (11, "Warehouses", "WAR", "COM", "Sub", "Commercial"),
    (12, "Industrial properties", "IND", "COM", "Sub", "Commercial"),
    (13, "Mixed-use", "MIX", None, "Main", "Commercial"),
    (14, "Investment", "INV", None, "Main", "Commercial"),
    (15, "Vacation homes", "VAC", "RES", "Sub", "Residential"),
    (16, "Student housing", "STU", "RES", "Sub", "Residential"),
    (17, "Senior housing", "SEN", "RES", "Sub", "Residential"),
    (18, "Hospitality", "HOS", None, "Main", "Commercial"),
    (19, "Hotels", "HTL", "HOS", "Sub", "Commercial"),
    (20, "Resorts", "RST2", "HOS", "Sub", "Commercial"),
    (21, "Bed and Breakfasts", "BBB", "HOS", "Sub", "Commercial"),
    (22, "Healthcare", "HEA", None, "Main", "Community"),
    (23, "Hospitals", "HSP", "HEA", "Sub", "Community"),
    (24, "Clinics", "CLI", "HEA", "Sub", "Community"),
    (25, "Medical offices", "MED", "HEA", "Sub", "Community"),
    (26, "Educational", "EDU", None, "Main", "Community"),
    (27, "Schools", "SCH", "EDU", "Sub", "Community"),
    (28, "Colleges", "COL", "EDU", "Sub", "Community"),
    (29, "Training centers", "TRA", "EDU", "Sub", "Community"),
    (30, "Agricultural", "AGR", None, "Main", "Agricultural"),
    (31, "Farms", "FAR", "AGR", "Sub", "Agricultural"),
    (32, "Ranches", "RAN", "AGR", "Sub", "Agricultural"),
    (33, "Agricultural land", "ALD", "AGR", "Sub", "Agricultural"),
    (34, "Recreational", "REC", None, "Main", "Community"),
    (35, "Sports complexes", "SPC", "REC", "Sub", "Community"),
    (36, "Golf courses", "GOL", "REC", "Sub", "Community"),
    (37, "Entertainment venues", "ENT", "REC", "Sub", "Community"),
    (38, "Government/Public Use", "GOV", None, "Main", "Community"),
    (39, "Government offices", "GOO", "GOV", "Sub", "Community"),
    (40, "Public parks", "PAR", "GOV", "Sub", "Community"),
    (41, "Civic centers", "CIV", "GOV", "Sub", "Community"),
    (42, "Religious", "REL", None, "Main", "Community"),
    (43, "Churches", "CHU", "REL", "Sub", "Community"),
    (44, "Mosques", "MOS", "REL", "Sub", "Community"),
    (45, "Temples", "TEM", "REL", "Sub", "Community"),
    (46, "Synagogues", "SYN", "REL", "Sub", "Community"),
    (47, "Nonprofit", "NON", None, "Main", "Community"),
    (48, "Nonprofit organization properties", "NOP", "NON", "Sub", "Community"),
    (49, "Development", "DEV", None, "Main", "Commercial"),
    (50, "Land for development projects", "LDP", "DEV", "Sub", "Commercial"),
    (51, "Special Purpose", "SPP", None, "Main", "Special Purpose"),
    (52, "Theaters", "THE", "SPP", "Sub", "Special Purpose"),
    (53, "Museums", "MUS", "SPP", "Sub", "Special Purpose"),
    (54, "Historical landmarks", "HLM", "SPP", "Sub", "Special Purpose"),
    (55, "Community centers", "CMC", "SPP", "Sub", "Special Purpose"),
]

PROPERTY_LISTING_TYPE_DATA = [
    (1, "For Sale", "FS", None, "Main"),
    (2, "For Rent", "FR", None, "Main"),
]

SAMPLE_PROPERTIES = [
    {
        'title': '456 Oak Avenue',
        'location_text': 'Westlands, Nairobi',
        'formatted_address': '456 Oak Avenue, Westlands, Nairobi, Kenya',
        'asset_type': PropertyListing.Type.RESIDENTIAL,
        'listing_type': PropertyListing.ListingType.SALE,
        'purpose_name': 'Condominiums',
        'bedrooms': 2,
        'bathrooms': 2,
        'internal_area': 1200,
        'lot_size': None,
        'price_estimate': 9800000.00,
        'latitude': -1.267410000,
        'longitude': 36.810220000,
    },
    {
        'title': '789 Pine Lane',
        'location_text': 'Kilimani, Nairobi',
        'formatted_address': '789 Pine Lane, Kilimani, Nairobi, Kenya',
        'asset_type': PropertyListing.Type.RESIDENTIAL,
        'listing_type': PropertyListing.ListingType.LEASE,
        'purpose_name': 'Townhouses',
        'bedrooms': 3,
        'bathrooms': 2,
        'internal_area': 1800,
        'lot_size': 0.15,
        'price_estimate': 320000.00,
        'latitude': -1.292100000,
        'longitude': 36.783650000,
    },
    {
        'title': '101 Maple Street',
        'location_text': 'Runda, Nairobi',
        'formatted_address': '101 Maple Street, Runda, Nairobi, Kenya',
        'asset_type': PropertyListing.Type.RESIDENTIAL,
        'listing_type': PropertyListing.ListingType.SALE,
        'purpose_name': 'Single-family homes',
        'bedrooms': 4,
        'bathrooms': 3,
        'internal_area': 2500,
        'lot_size': 0.30,
        'price_estimate': 24500000.00,
        'latitude': -1.220580000,
        'longitude': 36.819440000,
    },
    {
        'title': '202 Cedar Drive',
        'location_text': 'Kileleshwa, Nairobi',
        'formatted_address': '202 Cedar Drive, Kileleshwa, Nairobi, Kenya',
        'asset_type': PropertyListing.Type.RESIDENTIAL,
        'listing_type': PropertyListing.ListingType.LEASE,
        'purpose_name': 'Apartments',
        'bedrooms': 1,
        'bathrooms': 1,
        'internal_area': 800,
        'lot_size': None,
        'price_estimate': 145000.00,
        'latitude': -1.280660000,
        'longitude': 36.782950000,
    },
    {
        'title': '303 Birch Street',
        'location_text': 'Lavington, Nairobi',
        'formatted_address': '303 Birch Street, Lavington, Nairobi, Kenya',
        'asset_type': PropertyListing.Type.RESIDENTIAL,
        'listing_type': PropertyListing.ListingType.SALE,
        'purpose_name': 'Duplexes',
        'bedrooms': 5,
        'bathrooms': 4,
        'internal_area': 3000,
        'lot_size': 0.35,
        'price_estimate': 36500000.00,
        'latitude': -1.279450000,
        'longitude': 36.761980000,
    },
]


def ensure_property_users():
    owner, owner_created = User.objects.update_or_create(
        username='owner',
        defaults={
            'email': 'owner@example.com',
            'role': User.Role.PROJECT_OWNER,
            'first_name': 'Alice',
            'last_name': 'Owner',
            'is_staff': False,
            'is_superuser': False,
        },
    )
    owner.set_password('password123')
    owner.save(update_fields=['password'])
    log_seed_result("Property seed owner", f"{owner.username}/password123", owner_created)

    property_manager, manager_created = User.objects.update_or_create(
        username='property_manager',
        defaults={
            'email': 'property@ujenzi.com',
            'role': User.Role.PROJECT_OWNER,
            'first_name': 'Priya',
            'last_name': 'Property',
            'is_staff': False,
            'is_superuser': False,
        },
    )
    property_manager.set_password('password123')
    property_manager.save(update_fields=['password'])
    property_manager.grant_role(User.Role.PROPERTY_MANAGER)
    log_seed_result("Property manager", f"{property_manager.username}/password123", manager_created)

    investor, investor_created = User.objects.update_or_create(
        username='investor',
        defaults={
            'email': 'capital@example.com',
            'role': User.Role.PROJECT_OWNER,
            'first_name': 'David',
            'last_name': 'Investor',
            'is_staff': False,
            'is_superuser': False,
        },
    )
    investor.set_password('password123')
    investor.save(update_fields=['password'])
    investor.grant_role(User.Role.INVESTOR)
    log_seed_result("Property seed investor", f"{investor.username}/password123", investor_created)

    return owner, property_manager, investor


def seed_property_taxonomy():
    purpose_map = {}
    root_lookup = {}

    for row_id, name, property_code, parent_code, hierarchy_type, category in PROPERTY_PURPOSES:
        parent = root_lookup.get(parent_code) if parent_code else None
        slug = f"property-purpose-{slugify(name)}-{row_id}"
        item, created = Category.objects.update_or_create(
            slug=slug,
            taxonomy_type=TaxonomyType.PROPERTY,
            defaults={'name': name, 'parent': parent, 'active': True},
        )
        purpose_map[name] = item
        if hierarchy_type == 'Main':
            root_lookup[property_code] = item
        log_seed_result("Property purpose taxonomy", name, created)

    listing_type_root, created = Category.objects.update_or_create(
        slug='property-listing-types',
        taxonomy_type=TaxonomyType.PROPERTY,
        defaults={'name': 'Property Listing Types', 'active': True},
    )
    log_seed_result("Property listing taxonomy root", listing_type_root.name, created)

    for _, name, type_code, _, _ in PROPERTY_LISTING_TYPE_DATA:
        child, created = Category.objects.update_or_create(
            slug=f'property-listing-{slugify(name)}-{type_code.lower()}',
            taxonomy_type=TaxonomyType.PROPERTY,
            defaults={'name': name, 'parent': listing_type_root, 'active': True},
        )
        log_seed_result("Property listing taxonomy", child.name, created)

    return purpose_map


def upsert_location(country, name, city, state, address, latitude, longitude):
    location, _ = Location.objects.update_or_create(
        name=name,
        country=country,
        defaults={
            'address': address,
            'city': city,
            'state': state,
            'latitude': latitude,
            'longitude': longitude,
        },
    )
    return location


def seed_property_listings(owner, property_manager, purpose_map):
    kenya = Country.objects.filter(iso_code='KE').first()
    nairobi_state = 'Nairobi County'

    property_specs = [
        {
            'title': 'Riverside Mixed-Use Development Site',
            'description': 'Prime mixed-use property with strong frontage, financing enabled, and project-conversion potential.',
            'asset_type': PropertyListing.Type.MIXED_USE,
            'listing_type': PropertyListing.ListingType.DEVELOPMENT_OPPORTUNITY,
            'purpose': purpose_map.get('Land for development projects') or purpose_map.get('Development'),
            'price_estimate': 8500000.00,
            'location_text': 'Riverside, Nairobi',
            'formatted_address': 'Riverside Drive, Nairobi, Kenya',
            'latitude': -1.270050000,
            'longitude': 36.806370000,
            'financing_allowed': True,
            'inquiry_enabled': True,
            'appointment_enabled': True,
            'manager': property_manager,
            'country': kenya,
            'location': upsert_location(kenya, 'Riverside', 'Nairobi', nairobi_state, 'Riverside Drive, Nairobi, Kenya', -1.270050000, 36.806370000),
        },
        {
            'title': 'Completed Warehouse Cluster - Athi River',
            'description': 'Income-generating warehouse asset available as a completed project/property financing opportunity.',
            'asset_type': PropertyListing.Type.INDUSTRIAL,
            'listing_type': PropertyListing.ListingType.COMPLETED_PROJECT,
            'purpose': purpose_map.get('Warehouses'),
            'price_estimate': 12500000.00,
            'location_text': 'Athi River, Machakos',
            'formatted_address': 'Mombasa Road, Athi River, Kenya',
            'latitude': -1.456120000,
            'longitude': 36.983210000,
            'financing_allowed': True,
            'inquiry_enabled': True,
            'appointment_enabled': True,
            'manager': property_manager,
            'country': kenya,
            'location': upsert_location(kenya, 'Athi River Logistics', 'Athi River', 'Machakos County', 'Mombasa Road, Athi River, Kenya', -1.456120000, 36.983210000),
        },
    ]

    for sample in SAMPLE_PROPERTIES:
        property_specs.append(
            {
                'title': sample['title'],
                'description': f"{sample['purpose_name']} positioned for modern property discovery and financing workflows.",
                'asset_type': sample['asset_type'],
                'listing_type': sample['listing_type'],
                'purpose': purpose_map.get(sample['purpose_name']),
                'price_estimate': sample['price_estimate'],
                'location_text': sample['location_text'],
                'formatted_address': sample['formatted_address'],
                'latitude': sample['latitude'],
                'longitude': sample['longitude'],
                'financing_allowed': sample['listing_type'] == PropertyListing.ListingType.SALE,
                'inquiry_enabled': True,
                'appointment_enabled': True,
                'manager': property_manager,
                'country': kenya,
                'location': upsert_location(
                    kenya,
                    sample['location_text'],
                    'Nairobi',
                    nairobi_state,
                    sample['formatted_address'],
                    sample['latitude'],
                    sample['longitude'],
                ),
            }
        )

    seeded_properties = []
    for spec in property_specs:
        prop, created = PropertyListing.objects.update_or_create(
            owner=owner,
            title=spec['title'],
            defaults=spec,
        )
        log_seed_result("Property", prop.title, created)
        seeded_properties.append(prop)

    return seeded_properties


def get_core_property_examples(properties):
    property_by_title = {prop.title: prop for prop in properties}
    riverside = property_by_title.get('Riverside Mixed-Use Development Site')
    warehouse = property_by_title.get('Completed Warehouse Cluster - Athi River')

    if not riverside or not warehouse:
        raise ValueError("Core property workflow samples are missing from the seeded property list.")

    return riverside, warehouse


def seed_property_metadata(properties):
    riverside, warehouse = get_core_property_examples(properties)
    metadata_specs = [
        (
            riverside,
            {
                'zoning_info': 'Mixed-use commercial and residential zoning approved',
                'build_ready': True,
                'utilities_available': ['Water', 'Power', 'Sewer', 'Fiber'],
                'development_stage': 'SERVICED_SITE',
                'estimated_completion_budget': 3500000.00,
                'recommended_use': 'High-rise residential and retail podium',
            },
        ),
        (
            warehouse,
            {
                'zoning_info': 'Industrial logistics use approved',
                'build_ready': True,
                'utilities_available': ['Water', 'Power', 'Road Access'],
                'development_stage': 'COMPLETED',
                'estimated_completion_budget': 0,
                'recommended_use': 'Warehousing and light distribution',
            },
        ),
    ]

    for prop, defaults in metadata_specs:
        _, created = DevelopmentMetadata.objects.update_or_create(
            property=prop,
            defaults=defaults,
        )
        log_seed_result("Property development metadata", prop.title, created)


def seed_property_profiles(properties):
    riverside, warehouse = get_core_property_examples(properties)

    specification_specs = [
        (
            riverside,
            {
                'bedrooms': 0,
                'bathrooms': 0,
                'floors': 0,
                'parking_spaces': 40,
                'internal_area': None,
                'internal_area_unit': PropertySpecification.AreaUnit.SQM,
                'lot_size': 1.80,
                'lot_size_unit': PropertySpecification.AreaUnit.ACRE,
                'furnishing_state': '',
                'condition_rating': PropertySpecification.ConditionRating.GOOD,
                'occupancy_status': PropertySpecification.OccupancyStatus.VACANT,
            },
        ),
        (
            warehouse,
            {
                'bedrooms': 0,
                'bathrooms': 6,
                'floors': 2,
                'parking_spaces': 18,
                'internal_area': 4200,
                'internal_area_unit': PropertySpecification.AreaUnit.SQM,
                'lot_size': 2.5,
                'lot_size_unit': PropertySpecification.AreaUnit.ACRE,
                'year_built': 2022,
                'condition_rating': PropertySpecification.ConditionRating.EXCELLENT,
                'occupancy_status': PropertySpecification.OccupancyStatus.TENANTED,
            },
        ),
    ]

    for prop, defaults in specification_specs:
        _, created = PropertySpecification.objects.update_or_create(property=prop, defaults=defaults)
        log_seed_result("Property specification", prop.title, created)

    ownership_specs = [
        (
            riverside,
            {
                'legal_owner_name': 'Alice Owner Holdings',
                'ownership_type': PropertyOwnershipProfile.OwnershipType.COMPANY,
                'title_reference': 'RV-NAI-2044',
                'deed_reference': 'DEED-RIV-2291',
                'has_liens': False,
                'disclosure_notes': 'Development approvals in process review file available on request.',
                'verification_status': PropertyOwnershipProfile.VerificationStatus.PENDING,
            },
        ),
        (
            warehouse,
            {
                'legal_owner_name': 'Alice Owner Logistics',
                'ownership_type': PropertyOwnershipProfile.OwnershipType.COMPANY,
                'title_reference': 'ATHI-LOG-440',
                'deed_reference': 'DEED-ATHI-440',
                'has_liens': False,
                'disclosure_notes': 'Existing tenancy schedule can be shared with qualified prospects.',
                'verification_status': PropertyOwnershipProfile.VerificationStatus.VERIFIED,
            },
        ),
    ]

    for prop, defaults in ownership_specs:
        _, created = PropertyOwnershipProfile.objects.update_or_create(property=prop, defaults=defaults)
        log_seed_result("Property ownership profile", prop.title, created)

    pricing_specs = [
        (
            riverside,
            {
                'currency': 'KES',
                'asking_price': 8500000.00,
                'pricing_strategy': PropertyPricingProfile.PricingStrategy.NEGOTIABLE,
                'requires_deposit': True,
                'deposit_amount': 500000.00,
                'price_per_area_unit': 4722222.22,
                'area_unit': PropertySpecification.AreaUnit.ACRE,
                'service_charge_amount': 0,
                'tax_percentage': 2.00,
                'insurance_percentage': 1.50,
                'financing_notes': 'Suitable for acquisition plus completion finance.',
            },
        ),
        (
            warehouse,
            {
                'currency': 'KES',
                'asking_price': 12500000.00,
                'rent_amount': 950000.00,
                'pricing_strategy': PropertyPricingProfile.PricingStrategy.FIXED,
                'requires_deposit': True,
                'deposit_amount': 1000000.00,
                'price_per_area_unit': 2976.19,
                'area_unit': PropertySpecification.AreaUnit.SQM,
                'service_charge_amount': 125000.00,
                'tax_percentage': 2.50,
                'insurance_percentage': 1.75,
                'financing_notes': 'Acquisition facility available for yield-focused buyers.',
            },
        ),
    ]

    for prop, defaults in pricing_specs:
        _, created = PropertyPricingProfile.objects.update_or_create(property=prop, defaults=defaults)
        log_seed_result("Property pricing profile", prop.title, created)

    feature_specs = {
        riverside: [
            {'category': 'Site', 'name': 'Corner Frontage', 'description': 'Strong street visibility', 'is_highlighted': True, 'sort_order': 1},
            {'category': 'Utilities', 'name': 'Fiber Ready', 'description': 'Fiber and utility backbone available', 'is_highlighted': True, 'sort_order': 2},
            {'category': 'Planning', 'name': 'Mixed-Use Approval Path', 'description': 'Suitable for retail plus residential podium', 'sort_order': 3},
        ],
        warehouse: [
            {'category': 'Logistics', 'name': 'Truck Access', 'description': 'Designed for heavy goods access', 'is_highlighted': True, 'sort_order': 1},
            {'category': 'Security', 'name': 'Controlled Gatehouse', 'description': 'Access-controlled compound', 'is_highlighted': True, 'sort_order': 2},
            {'category': 'Operations', 'name': 'Loading Bays', 'description': 'Multiple loading bays with staging area', 'sort_order': 3},
        ],
    }

    for prop, features in feature_specs.items():
        prop.features.all().delete()
        PropertyFeature.objects.bulk_create([PropertyFeature(property=prop, **feature) for feature in features])
        logger.info(f"✅ Property features updated: {prop.title}")

    media_specs = {
        riverside: [
            {
                'media_type': PropertyMediaAsset.MediaType.IMAGE,
                'external_url': 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=80',
                'title': 'Riverside site overview',
                'caption': 'Primary hero image',
                'alt_text': 'Riverside mixed-use development site',
                'sort_order': 1,
                'is_primary': True,
            },
            {
                'media_type': PropertyMediaAsset.MediaType.VIRTUAL_TOUR,
                'external_url': 'https://example.com/riverside-tour',
                'title': 'Virtual site walkthrough',
                'caption': 'Investor briefing tour',
                'alt_text': 'Virtual property tour',
                'sort_order': 2,
            },
        ],
        warehouse: [
            {
                'media_type': PropertyMediaAsset.MediaType.IMAGE,
                'external_url': 'https://images.unsplash.com/photo-1511818966892-d7d671e672a2?auto=format&fit=crop&w=1200&q=80',
                'title': 'Warehouse exterior',
                'caption': 'Primary hero image',
                'alt_text': 'Completed warehouse cluster',
                'sort_order': 1,
                'is_primary': True,
            },
            {
                'media_type': PropertyMediaAsset.MediaType.FLOOR_PLAN,
                'external_url': 'https://example.com/warehouse-plan.pdf',
                'title': 'Logistics floor plan',
                'caption': 'Distribution layout',
                'alt_text': 'Warehouse floor plan',
                'sort_order': 2,
            },
        ],
    }

    for prop, assets in media_specs.items():
        prop.media_assets.all().delete()
        PropertyMediaAsset.objects.bulk_create([PropertyMediaAsset(property=prop, **asset) for asset in assets])
        logger.info(f"✅ Property media assets updated: {prop.title}")


def seed_property_project_link(property_listing):
    project = Project.objects.filter(title='Skyline Apartment Wing A').first()
    if not project:
        logger.warning("⚠️ No project found for property linkage, skipping project link")
        return None

    _, created = PropertyProjectLink.objects.update_or_create(
        property=property_listing,
        project=project,
        defaults={},
    )
    log_seed_result("Property project link", f"{property_listing.title} -> {project.title}", created)
    return project


def seed_property_showings(properties, property_manager, owner):
    showing_specs = [
        (
            properties[0],
            {
                'event_type': PropertyShowing.EventType.OPEN_HOUSE,
                'occurrence_type': PropertyShowing.OccurrenceType.SINGLE,
                'start_at': timezone.now().replace(minute=0, second=0, microsecond=0) + timedelta(days=4, hours=11),
                'end_at': timezone.now().replace(minute=0, second=0, microsecond=0) + timedelta(days=4, hours=14),
                'contact_person': property_manager.get_full_name() or property_manager.username,
                'phone': '+254700123456',
                'instructions': 'Bring identification for access to the managed site.',
                'virtual_tour_url': 'https://example.com/riverside-tour',
                'is_active': True,
            },
        ),
        (
            properties[1],
            {
                'event_type': PropertyShowing.EventType.PRIVATE_SHOWING,
                'occurrence_type': PropertyShowing.OccurrenceType.APPOINTMENT_ONLY,
                'start_at': timezone.now().replace(minute=0, second=0, microsecond=0) + timedelta(days=5, hours=10),
                'end_at': timezone.now().replace(minute=0, second=0, microsecond=0) + timedelta(days=5, hours=16),
                'contact_person': owner.get_full_name() or owner.username,
                'phone': '+254711222333',
                'instructions': 'Tenancy schedule available during managed visit.',
                'is_active': True,
            },
        ),
    ]

    for prop, defaults in showing_specs:
        _, created = PropertyShowing.objects.update_or_create(
            property=prop,
            event_type=defaults['event_type'],
            defaults=defaults,
        )
        log_seed_result("Property showing", prop.title, created)


def seed_property_availability(properties, property_manager, owner):
    availability_specs = [
        (
            properties[0],
            timezone.now() + timedelta(days=2, hours=9),
            timezone.now() + timedelta(days=2, hours=13),
        ),
        (
            properties[1],
            timezone.now() + timedelta(days=3, hours=10),
            timezone.now() + timedelta(days=3, hours=14),
        ),
    ]

    windows = {}
    for prop, start_at, end_at in availability_specs:
        window, created = PropertyAvailabilityWindow.objects.update_or_create(
            property=prop,
            managed_by=property_manager or owner,
            start_at=start_at.replace(minute=0, second=0, microsecond=0),
            defaults={
                'end_at': end_at.replace(minute=0, second=0, microsecond=0),
                'slot_duration_minutes': 60,
                'is_active': True,
            },
        )
        windows[prop.title] = window
        log_seed_result("Property availability window", prop.title, created)

    return windows


def seed_property_inquiries(properties, investor):
    inquiry_specs = [
        (
            properties[0],
            {
                'full_name': 'Anonymous Development Prospect',
                'email': 'prospect@example.com',
                'phone_number': '',
                'preferred_contact_method': 'email',
                'inquiry_type': PropertyInquiry.InquiryType.FINANCING,
                'message': 'Interested in acquisition plus development finance.',
            },
        ),
        (
            properties[1],
            {
                'full_name': investor.get_full_name() or 'Capital Investor',
                'email': investor.email,
                'phone_number': '+254711000111',
                'preferred_contact_method': 'phone',
                'inquiry_type': PropertyInquiry.InquiryType.GENERAL,
                'message': 'Would like to discuss yield, tenancy, and acquisition structure.',
                'inquirer_user': investor,
            },
        ),
    ]

    for prop, defaults in inquiry_specs:
        inquiry, created = PropertyInquiry.objects.update_or_create(
            property=prop,
            full_name=defaults['full_name'],
            message=defaults['message'],
            defaults=defaults,
        )
        log_seed_result("Property inquiry", f"{prop.title} / {inquiry.full_name}", created)


def seed_property_appointments(property_listing, window):
    appointment, created = PropertyAppointment.objects.update_or_create(
        property=property_listing,
        full_name='Site Visit Guest',
        scheduled_start=window.start_at,
        defaults={
            'availability_window': window,
            'email': 'visit@example.com',
            'phone_number': '+254722123456',
            'scheduled_end': window.start_at + timedelta(hours=1),
            'notes': 'Needs briefing on development potential.',
            'created_by': None,
            'visitor_user': None,
        },
    )
    log_seed_result("Property appointment", f"{property_listing.title} / {appointment.full_name}", created)


def seed_property_finance(owner, investor, properties, project):
    finance_products = [
        {
            'name': 'Property Acquisition Facility',
            'provider_name': 'Procus Capital',
            'max_amount': 20000000.00,
            'interest_rate': 11.50,
        },
        {
            'name': 'Project Completion Loan',
            'provider_name': 'BuildBank',
            'max_amount': 10000000.00,
            'interest_rate': 13.25,
        },
        {
            'name': 'Materials Procurement Credit',
            'provider_name': 'SupplyLine Finance',
            'max_amount': 3000000.00,
            'interest_rate': 9.75,
        },
    ]

    created_products = {}
    for spec in finance_products:
        product, created = FinanceProduct.objects.update_or_create(
            name=spec['name'],
            defaults={**spec, 'active': True},
        )
        created_products[spec['name']] = product
        log_seed_result("Finance product", product.name, created)

    _, created = FinanceApplication.objects.update_or_create(
        applicant=owner,
        product=created_products['Property Acquisition Facility'],
        target_type=FinanceApplication.TargetType.PROPERTY,
        property=properties[1],
        defaults={
            'project': None,
            'requested_amount': 5000000.00,
            'purpose_category': FinanceApplication.PurposeCategory.ACQUISITION,
            'purpose': 'Acquire completed warehouse cluster with light refinancing component.',
            'status': FinanceApplication.Status.SUBMITTED,
        },
    )
    log_seed_result("Property finance application", properties[1].title, created)

    if project:
        _, created = FinanceApplication.objects.update_or_create(
            applicant=investor,
            product=created_products['Project Completion Loan'],
            target_type=FinanceApplication.TargetType.PROJECT,
            project=project,
            defaults={
                'property': None,
                'requested_amount': 2500000.00,
                'purpose_category': FinanceApplication.PurposeCategory.COMPLETION,
                'purpose': 'Support project completion and final-stage execution financing.',
                'status': FinanceApplication.Status.SUBMITTED,
            },
        )
        log_seed_result("Project finance application", project.title, created)


def run():
    log_seed_banner("🏠 Starting Property Workflow Seed")

    owner, property_manager, investor = ensure_property_users()
    purpose_map = seed_property_taxonomy()
    properties = seed_property_listings(owner, property_manager, purpose_map)
    seed_property_metadata(properties)
    seed_property_profiles(properties)
    project = seed_property_project_link(properties[0])
    seed_property_showings(properties, property_manager, owner)
    windows = seed_property_availability(properties, property_manager, owner)
    seed_property_inquiries(properties, investor)
    seed_property_appointments(properties[0], windows[properties[0].title])
    seed_property_finance(owner, investor, properties, project)

    log_seed_banner("✅ Property Workflow Seed Complete")


if __name__ == '__main__':
    run()
