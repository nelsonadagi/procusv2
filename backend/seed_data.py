#!/usr/bin/env python
"""
Main seed script for the Ujenzi Marketplace.
Creates test data for all major models.
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

import logging
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from accounts.models import User
from vendors.models import Vendor
from contractors.models import ContractorProfile
from logistics.models import CourierProfile
from taxonomy.models import Category
from catalog.models import (
    Product,
    ProductCertificationRegistry,
    ProductCertification,
    ProductAttribute,
    ProductDocument,
)
from projects.models import Project
from contracts.models import Contract
from government.models import PublicTender
from regulation.models import InvestorProfile, InvestmentAgreement
from platform_settings.models import Country

User = get_user_model()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s', stream=sys.stdout)


ATTRIBUTE_LIBRARY = [
    {
        "name": "Material Type",
        "description": "Specifies the primary substance (e.g., concrete, steel, wood, brick)",
    },
    {
        "name": "Dimensions",
        "description": "Length, width, height, and thickness of the material",
    },
    {
        "name": "Weight",
        "description": "Mass per unit (e.g., per square meter or per piece)",
    },
    {
        "name": "Color",
        "description": "The visual appearance or pigment of the material",
    },
    {
        "name": "Density",
        "description": "Mass per unit volume, indicating how compact the material is",
    },
    {
        "name": "Strength",
        "description": "Tensile, compressive, and shear strength",
    },
    {
        "name": "Durability",
        "description": "Resistance to wear, decay, and weathering",
    },
    {
        "name": "Thermal Conductivity",
        "description": "Ability to conduct heat",
    },
    {
        "name": "Fire Resistance",
        "description": "Ability to withstand fire and heat exposure",
    },
    {
        "name": "Moisture Resistance",
        "description": "Ability to resist water absorption and damage",
    },
    {
        "name": "Flexibility",
        "description": "Ability to bend without breaking",
    },
    {
        "name": "Acoustic Properties",
        "description": "Sound absorption and insulation characteristics",
    },
    {
        "name": "Surface Finish",
        "description": "Texture and smoothness of the material's surface",
    },
    {
        "name": "Installation Method",
        "description": "Techniques required for installing the material",
    },
    {
        "name": "Cost",
        "description": "Price per unit, including variations based on quantity",
    },
    {
        "name": "Sustainability",
        "description": "Environmental impact, including recyclability and energy efficiency",
    },
    {
        "name": "Chemical Resistance",
        "description": "Ability to resist chemical corrosion and degradation",
    },
    {
        "name": "Transparency",
        "description": "Degree of light transmission through the material",
    },
    {
        "name": "Load-bearing Capacity",
        "description": "Maximum load the material can support",
    },
    {
        "name": "Abrasion Resistance",
        "description": "Resistance to surface wear from friction",
    },
    {
        "name": "Coefficient of Expansion",
        "description": "How the material expands or contracts with temperature changes",
    },
    {
        "name": "Aesthetic Appeal",
        "description": "Visual attractiveness, including patterns and finishes",
    },
    {
        "name": "Manufacturing Tolerance",
        "description": "Acceptable deviations in dimensions and properties during production",
    },
    {
        "name": "Regulatory Compliance",
        "description": "Adherence to building codes and standards",
    },
    {
        "name": "Supplier Information",
        "description": "Details about the manufacturer or supplier",
    },
]

MATERIAL_CATEGORY_EXPORT = [
    {'name': 'DEMOLITIONS AND ALTERATIONS', 'description': 'Tasks involving the demolition and alteration of existing structures.', 'cat_id': 'A001'},
    {'name': 'SITE CLEARANCE', 'description': 'Preparation of the site by removing debris, vegetation, and other obstructions.', 'cat_id': 'B002'},
    {'name': 'EXCAVATIONS & EARTHWORKS', 'description': 'Work involving excavation and earthmoving activities.', 'cat_id': 'C003'},
    {'name': 'CONCRETE WORKS', 'description': 'Tasks related to the mixing, pouring, and finishing of concrete.', 'cat_id': 'D004'},
    {'name': 'WALLING', 'description': 'Construction of walls using various materials.', 'cat_id': 'E005'},
    {'name': 'WATER-PROOFING', 'description': 'Application of water-proofing materials to protect structures.', 'cat_id': 'F006'},
    {'name': 'ROOF COVERING', 'description': 'Installation and maintenance of roof coverings.', 'cat_id': 'G007'},
    {'name': 'DOORS', 'description': 'Installation and maintenance of doors.', 'cat_id': 'H008'},
    {'name': 'WINDOWS', 'description': 'Installation and maintenance of windows.', 'cat_id': 'J009'},
    {'name': 'IRONMONGERY', 'description': 'Supply and installation of ironmongery items.', 'cat_id': 'K010'},
    {'name': 'TIMBER BOARDS AND PARTITIONS', 'description': 'Use of timber boards and partitions in construction.', 'cat_id': 'L011'},
    {'name': 'GLASS AND GLAZING', 'description': 'Installation of glass and glazing materials.', 'cat_id': 'M012'},
    {'name': 'EXTERNAL FINISHES', 'description': 'Application of external finishes to buildings.', 'cat_id': 'N013'},
    {'name': 'INTERNAL FINISHES', 'description': 'Application of internal finishes to buildings.', 'cat_id': 'P014'},
    {'name': 'FITTINGS', 'description': 'Installation of fittings in buildings.', 'cat_id': 'Q015'},
    {'name': 'PAINTING AND DECORATING', 'description': 'Painting and decorating tasks.', 'cat_id': 'R016'},
    {'name': 'EXTERNAL WORKS', 'description': 'Tasks involving external works such as landscaping and paving.', 'cat_id': 'S017'},
    {'name': 'LANDSCAPING WORKS', 'description': 'Design and execution of landscaping projects.', 'cat_id': 'T018'},
    {'name': 'ELECTRICAL INSTALLATIONS', 'description': 'Installation and maintenance of electrical systems.', 'cat_id': 'U019'},
    {'name': 'PLUMBING AND DRAINAGE', 'description': 'Installation and maintenance of plumbing and drainage systems.', 'cat_id': 'V020'},
    {'name': 'FIRE ALARM SYSTEM/FIRE FIGHTING EQUIPMENT', 'description': 'Installation and maintenance of fire alarm systems and fire fighting equipment.', 'cat_id': 'W021'},
    {'name': 'PLANT HIRE CHARGES', 'description': 'Costs associated with hiring construction equipment.', 'cat_id': 'X022'},
    {'name': 'FURNITURE', 'description': 'Supply and installation of furniture.', 'cat_id': 'Y023'},
    {'name': 'ELEMENTAL COST ANALYSIS', 'description': 'Analysis of costs for different elements of the project.', 'cat_id': 'Z024'},
]

SUPPLIER_EXPORT = [
    {'name': 'Kenbro Industries', 'contact_email': 'contact@kenbroindustries.com', 'location': 'Nairobi, Kenya', 'supplier_type': 'wholesale', 'website': 'https://www.kenbroindustries.com'},
    {'name': 'Kenbro Industries Limited', 'contact_email': 'contact@kenbroindustries_limited.com', 'location': 'Nairobi, Kenya', 'supplier_type': 'wholesale', 'website': 'https://www.kenbroindustries_limited.com'},
    {'name': 'Kenya Builders & Concrete Co., Kenya Limited', 'contact_email': 'contact@kenyabuilders_concrete.com', 'location': 'Nairobi, Kenya', 'supplier_type': 'retail', 'website': 'https://www.kenya_builders_concrete.com'},
    {'name': 'Kubik, Inc.', 'contact_email': 'contact@kubik_inc.com', 'location': 'Nairobi, Kenya', 'supplier_type': 'service', 'website': 'https://www.kubik_inc.com'},
    {'name': 'Mabati Rolling Mills Ltd - Member of the SAFAL Group', 'contact_email': 'contact@mabati_rollings_mills.com', 'location': 'Mombasa, Kenya', 'supplier_type': 'material', 'website': 'https://www.mabati_rollings_mills.com'},
    {'name': 'Mjenzi Application', 'contact_email': 'contact@mjenzis_application.com', 'location': 'Nairobi, Kenya', 'supplier_type': 'service', 'website': 'https://www.mjenzis_application.com'},
    {'name': 'Mogaya Contractors', 'contact_email': 'contact@mogaya_contractors.com', 'location': 'Nairobi, Kenya', 'supplier_type': 'service', 'website': 'https://www.mogaya_contractors.com'},
    {'name': 'Mombasa Sealing', 'contact_email': 'contact@mombasa_sealing.com', 'location': 'Mombasa, Kenya', 'supplier_type': 'material', 'website': 'https://www.mombasa_sealing.com'},
    {'name': 'Muthokinju Paints and cement', 'contact_email': 'contact@muthokinju_paint_cement.com', 'location': 'Nakuru, Kenya', 'supplier_type': 'material', 'website': 'https://www.muthokinju_paint_cement.com'},
    {'name': 'NOVEL PAINTS', 'contact_email': 'contact@novel_paints.com', 'location': 'Nairobi, Kenya', 'supplier_type': 'material', 'website': 'https://www.novel_paints.com'},
    {'name': 'Nanjing Africa Co., Kenya Limited', 'contact_email': 'contact@nanjing_africa_co_limited.com', 'location': 'Nairobi, Kenya', 'supplier_type': 'material', 'website': 'https://www.nanjing_africa_co_limited.com'},
]

SPECIFICATION_PRODUCT_EXPORT = [
    {'name': 'Bath tubs', 'specificationid': 'SP1', 'materialid': 'DA0019', 'margin': 10, 'units': 'NO', 'cpurate': 2500, 'category_code': 'Q015'},
    {'name': 'Ideal Standard Studio Range Coloured or white washbasin and pedestal', 'specificationid': 'SP2', 'materialid': 'PV0201', 'margin': 10, 'units': 'NO', 'cpurate': 15265, 'category_code': 'V020'},
    {'name': '1.5 KW Emersion Heater', 'specificationid': 'SP6', 'materialid': 'PV0206', 'margin': 10, 'units': 'NO', 'cpurate': 1550, 'category_code': 'V020'},
    {'name': '10 Gallons (S/B) 14 G Hot Water Cylinder', 'specificationid': 'SP7', 'materialid': 'PV0206', 'margin': 10, 'units': 'NO', 'cpurate': 8925, 'category_code': 'V020'},
    {'name': '10 mm Diameter bars', 'specificationid': 'SP9', 'materialid': 'CD00411', 'margin': 10, 'units': 'KG', 'cpurate': 170, 'category_code': 'D004'},
    {'name': '10 mm thick parquet floor tiles - Mahogany', 'specificationid': 'SP11', 'materialid': 'IP0142', 'margin': 10, 'units': 'SM', 'cpurate': 3225, 'category_code': 'P014'},
    {'name': '100 mm dia. PVC pressure pipes', 'specificationid': 'SP17', 'materialid': 'PV0203', 'margin': 10, 'units': 'M', 'cpurate': 300, 'category_code': 'V020'},
    {'name': '100 mm thick surface bed Class 15/20(1:3:6)', 'specificationid': 'SP19', 'materialid': 'CD0041', 'margin': 10, 'units': 'SM', 'cpurate': 1000, 'category_code': 'D004'},
    {'name': '1000 liters galvanized C.W.S. tank with cover', 'specificationid': 'SP21', 'materialid': 'PV0205', 'margin': 10, 'units': 'NO', 'cpurate': 12500, 'category_code': 'V020'},
    {'name': '1150 MM HIGH STAINLESS STEEL SLAB URINALS COMPLETE WITH FITTINGS', 'specificationid': 'SP27', 'materialid': 'PV0201', 'margin': 10, 'units': 'NO', 'cpurate': 69000, 'category_code': 'V020'},
    {'name': '15 mm laminated anti-bandit glass - 28 mm (.76PVB Clear )', 'specificationid': 'SP34', 'materialid': 'GM0122', 'margin': 10, 'units': 'SM', 'cpurate': 21505, 'category_code': 'M012'},
    {'name': '160 mm thick clay blocks', 'specificationid': 'SP43', 'materialid': 'CD0047', 'margin': 10, 'units': 'SM', 'cpurate': 1400, 'category_code': 'E005'},
    {'name': '1800 x 2100 mm high double leaf sliding aluminum door', 'specificationid': 'SP44', 'materialid': 'DA0013', 'margin': 10, 'units': 'NO', 'cpurate': 54625, 'category_code': 'H008'},
    {'name': '2-zone Fire Alarm Panel flush mounted on the wall complete with 72-hour standby battery as MENVIER MF 9316', 'specificationid': 'SP47', 'materialid': 'FW0211', 'margin': 10, 'units': 'NO', 'cpurate': 34500, 'category_code': 'W021'},
    {'name': '20 mm medium density fibre board door shutter faced with veneer both sides, grooved and chamfered to detail overall size, 1120 x 2245 mm high', 'specificationid': 'SP52', 'materialid': 'FY0231', 'margin': 10, 'units': 'NO', 'cpurate': 6960, 'category_code': 'Y023'},
    {'name': '25 mm thick T&G ceiling - Cypress', 'specificationid': 'SP67', 'materialid': 'IP0143', 'margin': 10, 'units': 'SM', 'cpurate': 3000, 'category_code': 'P014'},
    {'name': 'Acoustic ceilings - Hunter Douglas suspended aluminium ceilings', 'specificationid': 'SP129', 'materialid': 'IP0143', 'margin': 10, 'units': 'SM', 'cpurate': 2530, 'category_code': 'P014'},
    {'name': 'Aluminum Casement Windows: Heavy duty powder coated aluminum windows including frames, ironmongery, and 8 mm thick clear sheet glass', 'specificationid': 'SP140', 'materialid': 'DA0014', 'margin': 10, 'units': 'SM', 'cpurate': 12000, 'category_code': 'J009'},
    {'name': 'Armoured cables 600/1000V - 2 core 10 mm²', 'specificationid': 'SP146', 'materialid': 'EU01910', 'margin': 10, 'units': 'LM', 'cpurate': 630, 'category_code': 'U019'},
    {'name': 'B.R.C mesh type A142', 'specificationid': 'SP179', 'materialid': 'CD00411', 'margin': 10, 'units': 'SM', 'cpurate': 450, 'category_code': 'D004'},
    {'name': 'Booster Pump: Hawig German Hobby Booster Pump C/W pressure switch, pressure tank and anti-vibration hose', 'specificationid': 'SP201', 'materialid': 'FW0213', 'margin': 10, 'units': 'NO', 'cpurate': 450000, 'category_code': 'W021'},
    {'name': 'Ceramic floor tiles - 300 x 600 mm coloured/rustic', 'specificationid': 'SP268', 'materialid': 'IP0142', 'margin': 10, 'units': 'SM', 'cpurate': 2000, 'category_code': 'P014'},
    {'name': 'Clear sheet Glass - 6 mm thick glass in panes 0.50 - 1.00 M2', 'specificationid': 'SP305', 'materialid': 'GM0122', 'margin': 10, 'units': 'SM', 'cpurate': 2000, 'category_code': 'M012'},
    {'name': 'Construction Plant and Machinery Concrete mixer: 14 Cu. Ft', 'specificationid': 'SP325', 'materialid': 'PX0221', 'margin': 10, 'units': 'DAILY', 'cpurate': 18515, 'category_code': 'X022'},
    {'name': 'Consumer unit 12 way 100A isolator', 'specificationid': 'SP335', 'materialid': 'EU0192', 'margin': 10, 'units': 'NO', 'cpurate': 6210, 'category_code': 'U019'},
    {'name': 'Flush timber door, 50 mm thick solid flush door leaf size 820 x 2060 mm overall (Mahogany Veneered)', 'specificationid': 'SP467', 'materialid': 'DA0013', 'margin': 10, 'units': 'NO', 'cpurate': 10150, 'category_code': 'H008'},
    {'name': 'Granite Flooring - 20 mm thick granite floor slabs, absolute black', 'specificationid': 'SP499', 'materialid': 'IP0142', 'margin': 10, 'units': 'SM', 'cpurate': 23400, 'category_code': 'P014'},
    {'name': 'LED Fittings 4 ft 2 x 18 watt with power factor greater than 0.9', 'specificationid': 'SP595', 'materialid': 'EU01911', 'margin': 10, 'units': 'NO', 'cpurate': 2300, 'category_code': 'U019'},
    {'name': 'M.D.F. - 18 mm thick', 'specificationid': 'SP611', 'materialid': 'TL0111', 'margin': 10, 'units': 'SM', 'cpurate': 3965, 'category_code': 'L011'},
    {'name': 'Office Desk: Size 1.6 M in cherry/beech', 'specificationid': 'SP652', 'materialid': 'FY0233', 'margin': 10, 'units': 'NO', 'cpurate': 18975, 'category_code': 'Y023'},
    {'name': 'PVC Tiles - Polyflex floor tile 2mm thick', 'specificationid': 'SP900', 'materialid': 'IP0142', 'margin': 10, 'units': 'SM', 'cpurate': 1550, 'category_code': 'P014'},
    {'name': 'Shower Cubical (steam) 1400 x 1400 x 2150mm', 'specificationid': 'SP953', 'materialid': 'PV0201', 'margin': 10, 'units': 'NO', 'cpurate': 402500, 'category_code': 'V020'},
    {'name': 'Solar water heater 300 liters', 'specificationid': 'SP970', 'materialid': 'PV0206', 'margin': 10, 'units': 'NO', 'cpurate': 35600, 'category_code': 'V020'},
    {'name': 'uPVC Windows: uPVC framed windows including 6 mm thick glass', 'specificationid': 'SP1033', 'materialid': 'DA0014', 'margin': 10, 'units': 'SM', 'cpurate': 18000, 'category_code': 'J009'},
    {'name': 'Window Blinds: Wooden window blinds including supply and fix', 'specificationid': 'SP1078', 'materialid': 'DA0014', 'margin': 10, 'units': 'SM', 'cpurate': 22500, 'category_code': 'J009'},
]

MATERIAL_ID_DETAILS = {
    'DA0019': {'material_type': 'Sanitary fitting', 'applications': 'Bathroom fit-outs\nHospitality washrooms', 'features': 'Fixture supply\nEasy maintenance'},
    'PV0201': {'material_type': 'Plumbing sanitary ware', 'applications': 'Washrooms\nResidential plumbing\nCommercial sanitary installations', 'features': 'Water-efficient fittings\nCeramic and stainless options'},
    'PV0206': {'material_type': 'Hot water system component', 'applications': 'Domestic hot water\nCommercial washrooms', 'features': 'Heating element compatibility\nPressure-rated components'},
    'CD00411': {'material_type': 'Reinforcement steel', 'applications': 'Slabs\nBeams\nColumns\nFoundations', 'features': 'Reinforcement grade steel\nHigh tensile performance'},
    'IP0142': {'material_type': 'Floor finish', 'applications': 'Interior floors\nStair treads\nSkirtings', 'features': 'Architectural finish\nWear resistant'},
    'PV0203': {'material_type': 'PVC pressure pipe', 'applications': 'Water reticulation\nCold water service', 'features': 'Corrosion resistant\nLightweight handling'},
    'CD0041': {'material_type': 'Mass concrete', 'applications': 'Surface beds\nBlinding\nFoundations', 'features': 'Site mixed concrete\nGeneral structural use'},
    'PV0205': {'material_type': 'Water storage tank', 'applications': 'Cold water storage\nUtility supply', 'features': 'Covered tank\nService installation ready'},
    'GM0122': {'material_type': 'Architectural glass', 'applications': 'Glazing\nSecurity screens\nWindows', 'features': 'Light transmission control\nSafety glazing options'},
    'CD0047': {'material_type': 'Blockwork unit', 'applications': 'Walling\nPartitions\nSuspended slab infill', 'features': 'Masonry unit\nConsistent sizing'},
    'DA0013': {'material_type': 'Door system', 'applications': 'Entrances\nInternal partitions\nCommercial access control', 'features': 'Framed assemblies\nArchitectural hardware ready'},
    'FW0211': {'material_type': 'Fire alarm component', 'applications': 'Life safety systems\nCommercial fire detection', 'features': 'Alarm control integration\nStandby battery support'},
    'FY0231': {'material_type': 'Furniture joinery component', 'applications': 'Doors\nCabinets\nInterior joinery', 'features': 'Veneered finish\nMachined panel construction'},
    'IP0143': {'material_type': 'Ceiling or plaster finish', 'applications': 'Ceilings\nCornices\nInterior wall preparation', 'features': 'Architectural finish system'},
    'DA0014': {'material_type': 'Window or timber accessory', 'applications': 'Window installation\nJoinery trims\nBlinds', 'features': 'Fabrication ready\nSite-installed'},
    'EU01910': {'material_type': 'Armoured electrical cable', 'applications': 'Power distribution\nSubmains\nExternal runs', 'features': 'Protected sheath\nHeavy duty current carrying'},
    'FW0213': {'material_type': 'Pump or fire-fighting accessory', 'applications': 'Booster systems\nWater transfer\nFire-fighting services', 'features': 'Pressure system compatible'},
    'PX0221': {'material_type': 'Plant hire item', 'applications': 'Site operations\nEquipment hire\nTemporary construction support', 'features': 'Daily hire basis'},
    'EU0192': {'material_type': 'Electrical distribution board', 'applications': 'Consumer distribution\nBuilding electrical services', 'features': 'Isolator ready\nModular circuits'},
    'EU01911': {'material_type': 'Electrical accessory or fitting', 'applications': 'Lighting\nPower outlets\nFinal electrical fittings', 'features': 'Building services accessory'},
    'TL0111': {'material_type': 'Timber board product', 'applications': 'Partitions\nCeilings\nJoinery backing', 'features': 'Sheet material\nInterior fit-out ready'},
    'FY0233': {'material_type': 'Furniture item', 'applications': 'Office fit-out\nFurniture supply', 'features': 'Commercial furniture range'},
}


def log_seed_banner(title):
    logger.info("=" * 60)
    logger.info(title)
    logger.info("=" * 60)


def log_seed_result(label, identifier, created):
    action = "created" if created else "updated"
    logger.info(f"✅ {label} {action}: {identifier}")


def derive_category_tags(supplier_type):
    if supplier_type == 'material':
        return ['CONCRETE WORKS', 'INTERNAL FINISHES', 'PLUMBING AND DRAINAGE']
    if supplier_type == 'service':
        return ['ELEMENTAL COST ANALYSIS', 'EXTERNAL WORKS']
    if supplier_type == 'wholesale':
        return ['CONCRETE WORKS', 'ELECTRICAL INSTALLATIONS', 'TIMBER BOARDS AND PARTITIONS']
    return ['WALLING', 'PAINTING AND DECORATING']


def build_reference_attributes(product_seed, vendor_name):
    details = MATERIAL_ID_DETAILS.get(product_seed['materialid'], {})
    attribute_values = {
        'Material Type': details.get('material_type', 'Construction material'),
        'Dimensions': product_seed.get('dimensions') or product_seed['name'],
        'Weight': product_seed.get('weight_label') or f"{product_seed['units']} basis",
        'Cost': str(product_seed['cpurate']),
        'Supplier Information': vendor_name,
        'Regulatory Compliance': 'Seeded reference item pending field verification',
        'Installation Method': 'Install to manufacturer and project specification',
    }
    return [
        {
            'group': 'Reference',
            'name': item['name'],
            'value': attribute_values.get(item['name'], item['description']),
            'unit': '',
            'is_highlight': item['name'] in {'Material Type', 'Cost', 'Supplier Information'},
        }
        for item in ATTRIBUTE_LIBRARY
    ]


def seed_product_record(vendor, category, registry_map, product_seed):
    details = MATERIAL_ID_DETAILS.get(product_seed['materialid'], {})
    unit = product_seed.get('units') or 'NO'
    base_price = float(product_seed.get('cpurate') or 0)
    margin_multiplier = 1 + ((product_seed.get('margin') or 10) / 100)
    bulk_price = round(base_price * 0.97, 2) if base_price else None

    technical_specifications = {
        'Specification ID': product_seed['specificationid'],
        'Material ID': product_seed['materialid'],
        'Reference Unit': unit,
        'Catalog Source': 'Imported from legacy material specification export',
        'Margin (%)': product_seed.get('margin', 10),
    }
    if product_seed.get('specs'):
        technical_specifications.update(product_seed['specs'])

    product_defaults = {
        'vendor': vendor,
        'category': category,
        'description': product_seed.get('description') or product_seed['name'],
        'short_description': product_seed.get('short_description') or product_seed['name'][:500],
        'unit': unit,
        'base_price': round(base_price * margin_multiplier, 2),
        'bulk_price': bulk_price,
        'bulk_threshold': product_seed.get('bulk_threshold', 10 if unit in {'NO', 'PRS'} else 25),
        'stock_quantity': product_seed.get('stock_quantity', 20),
        'min_order_quantity': product_seed.get('min_order_quantity', 1),
        'max_order_quantity': product_seed.get('max_order_quantity'),
        'reorder_level': product_seed.get('reorder_level', 5),
        'brand': product_seed.get('brand', vendor.business_name),
        'model_number': product_seed['specificationid'],
        'weight': product_seed.get('weight'),
        'dimensions': product_seed.get('dimensions', ''),
        'color': product_seed.get('color', ''),
        'material_composition': product_seed.get('material_composition', details.get('material_type', '')),
        'country_of_origin': product_seed.get('country_of_origin', 'Kenya'),
        'packaging_details': product_seed.get('packaging_details', f"Legacy catalog unit: {unit}"),
        'quality_grade': product_seed.get('quality_grade', 'Commercial'),
        'certifications': product_seed.get('certifications_text', 'KEBS reference catalog item'),
        'delivery_regions': product_seed.get('delivery_regions', ['NAIROBI', 'MOMBASA', 'KISUMU']),
        'estimated_delivery_days': product_seed.get('estimated_delivery_days', 3),
        'requires_special_handling': product_seed.get('requires_special_handling', False),
        'handling_instructions': product_seed.get('handling_instructions', 'Confirm site measurements and installation conditions before dispatch.'),
        'features': product_seed.get('features', details.get('features', 'Catalog reference item')),
        'applications': product_seed.get('applications', details.get('applications', 'General building use')),
        'technical_specifications': technical_specifications,
        'meta_keywords': f"{product_seed['materialid']}, {product_seed['specificationid']}, {category.name.lower()}",
        'is_featured': product_seed.get('is_featured', False),
        'is_new_arrival': False,
        'is_on_sale': False,
        'status': Product.Status.ACTIVE,
    }

    product, created = Product.objects.update_or_create(
        vendor=vendor,
        model_number=product_seed['specificationid'],
        defaults={'name': product_seed['name'], **product_defaults},
    )
    log_seed_result("Product", f"{product.name} [{product_seed['specificationid']}]", created)

    cert_entries = product_seed.get('certification_entries') or [{
        'registry': 'KEBS',
        'display_name': 'KEBS Reference Registry',
        'certification_number': f"{product_seed['materialid']}-{product_seed['specificationid']}",
        'issuing_body': 'Kenya Bureau of Standards',
        'status': 'ACTIVE',
    }]
    product.certification_entries.all().delete()
    for cert_entry in cert_entries:
        registry = registry_map.get(cert_entry.pop('registry', ''), registry_map['KEBS'])
        cert, cert_created = ProductCertification.objects.update_or_create(
            product=product,
            display_name=cert_entry['display_name'],
            defaults={**cert_entry, 'registry': registry},
        )
        log_seed_result("Product certification", f"{product.name} / {cert.display_name}", cert_created)

    product.attribute_entries.all().delete()
    attribute_entries = product_seed.get('attribute_entries') or []
    reference_entries = build_reference_attributes(product_seed, vendor.business_name)
    all_attributes = attribute_entries + reference_entries
    for sort_order, entry in enumerate(all_attributes, start=1):
        attr_defaults = {**entry, 'sort_order': sort_order}
        attr, attr_created = ProductAttribute.objects.update_or_create(
            product=product,
            name=entry['name'],
            sort_order=sort_order,
            defaults=attr_defaults,
        )
        log_seed_result("Product attribute", f"{product.name} / {attr.name}", attr_created)

    product.documents.all().delete()
    documents = product_seed.get('documents') or [{
        'document_type': 'DATASHEET',
        'title': f"{product_seed['specificationid']} Technical Reference",
        'external_url': product_seed.get('document_url', f"https://example.com/catalog/{product_seed['specificationid'].lower()}.pdf"),
        'description': 'Reference sheet generated from the legacy material export.',
        'is_public': True,
    }]
    for entry in documents:
        doc, doc_created = ProductDocument.objects.update_or_create(
            product=product,
            title=entry['title'],
            defaults=entry,
        )
        log_seed_result("Product document", f"{product.name} / {doc.title}", doc_created)


def seed_taxonomy():
    """Seed taxonomy categories needed for products and services."""
    material_root, material_root_created = Category.objects.update_or_create(
        slug='building-materials',
        taxonomy_type='MATERIAL',
        region_code=None,
        defaults={
            'name': 'Building Materials',
            'active': True,
            'parent': None,
        }
    )
    log_seed_result("Category", "Building Materials (MATERIAL ROOT)", material_root_created)

    created_cats = {
        'Building Materials': material_root,
    }

    for entry in MATERIAL_CATEGORY_EXPORT:
        slug = f"{entry['cat_id'].lower()}-{slugify(entry['name'])}"
        cat, created = Category.objects.update_or_create(
            slug=slug,
            taxonomy_type='MATERIAL',
            region_code=None,
            defaults={
                'name': entry['name'],
                'active': True,
                'parent': material_root,
            }
        )
        created_cats[entry['name']] = cat
        created_cats[entry['cat_id']] = cat
        log_seed_result("Category", f"{entry['name']} ({entry['cat_id']})", created)

    services = [
        ('Masonry', 'masonry'),
        ('Plumbing', 'plumbing'),
        ('Electrical', 'electrical'),
        ('Carpentry', 'carpentry'),
    ]
    for name, slug in services:
        cat, created = Category.objects.update_or_create(
            slug=slug,
            taxonomy_type='SERVICE',
            region_code=None,
            defaults={'name': name, 'active': True}
        )
        created_cats[name] = cat
        log_seed_result("Category", f"{name} (SERVICE)", created)

    return created_cats


def seed_users():
    """Create test users for all roles using the approval-driven model."""
    users_to_create = [
        ('admin', 'admin@ujenzi.com', 'ADMIN', 'System', 'Administrator', True, []),
        ('owner', 'owner@example.com', 'PROJECT_OWNER', 'Alice', 'Owner', False, []),
        ('contractor', 'builder@example.com', 'PROJECT_OWNER', 'Bob', 'Builder', False, ['CONTRACTOR']),
        ('vendor', 'supplier@example.com', 'PROJECT_OWNER', 'Charlie', 'Supplier', False, ['VENDOR']),
        ('investor', 'capital@example.com', 'PROJECT_OWNER', 'David', 'Investor', False, ['INVESTOR']),
        ('gov', 'tender@gov.com', 'PROJECT_OWNER', 'Gov', 'Authority', False, ['GOVERNMENT']),
        ('courier', 'dispatch@ujenzi.com', 'PROJECT_OWNER', 'Cora', 'Dispatch', False, ['COURIER']),
    ]

    users = {}
    for username, email, primary_role, fname, lname, is_superuser, approved_roles in users_to_create:
        defaults = {
            'email': email,
            'role': primary_role,
            'first_name': fname,
            'last_name': lname,
        }

        if is_superuser:
            user, created = User.objects.update_or_create(
                username=username,
                defaults={**defaults, 'is_staff': True, 'is_superuser': True}
            )
        else:
            user, created = User.objects.update_or_create(
                username=username,
                defaults=defaults
            )

        if is_superuser:
            user.set_password('adminpassword123')
            user.role = User.Role.ADMIN
            user.roles = []
            user.is_staff = True
            user.is_superuser = True
            user.save(update_fields=['password', 'role', 'roles', 'is_staff', 'is_superuser'])
            log_seed_result("Superuser", f"{username}/adminpassword123", created)
            users[User.Role.ADMIN] = user
            continue

        user.set_password('password123')
        user.role = User.Role.PROJECT_OWNER
        user.roles = []
        user.is_staff = False
        user.is_superuser = False
        user.save(update_fields=['password', 'role', 'roles', 'is_staff', 'is_superuser'])
        log_seed_result("User", f"{username}/password123 ({primary_role})", created)

        for approved_role in approved_roles:
            user.grant_role(approved_role)

        users[username] = user

    users[User.Role.PROJECT_OWNER] = users['owner']
    users[User.Role.CONTRACTOR] = users['contractor']
    users[User.Role.VENDOR] = users['vendor']
    users[User.Role.INVESTOR] = users['investor']
    users[User.Role.GOVERNMENT] = users['gov']
    users[User.Role.COURIER] = users['courier']

    return users


def seed_vendors(users, categories):
    """Create vendor profiles, including supplier samples from the material export."""
    vendor_user = users.get('VENDOR')
    if not vendor_user:
        logger.warning("⚠️ No vendor user found, skipping vendor profiles")
        return []

    kenya = Country.objects.filter(iso_code='KE').first()

    primary_vendor, created = Vendor.objects.update_or_create(
        user=vendor_user,
        defaults={
            'business_name': 'Global Construction Supplies',
            'registration_number': 'REG123456',
            'verified_status': 'APPROVED',
            'country': kenya,
            'location_text': 'Westlands, Nairobi',
            'formatted_address': 'Westlands, Nairobi, Kenya',
            'location_hierarchy': {
                'country': 'Kenya',
                'county': 'Nairobi',
                'city': 'Nairobi',
                'district': 'Westlands',
                'town': 'Westlands',
            },
            'provides_delivery': True,
            'delivery_radius_km': 50,
            'categories_served': ['CONCRETE WORKS', 'PLUMBING AND DRAINAGE', 'INTERNAL FINISHES'],
        }
    )
    log_seed_result("Vendor profile", primary_vendor.business_name, created)
    if primary_vendor.verified_status == Vendor.Status.APPROVED:
        primary_vendor.user.grant_role(User.Role.VENDOR)

    vendors = [primary_vendor]
    for index, supplier in enumerate(SUPPLIER_EXPORT, start=1):
        username = f"supplier_{index}_{slugify(supplier['name'])[:18]}"
        user_defaults = {
            'email': supplier['contact_email'],
            'role': User.Role.PROJECT_OWNER,
            'first_name': supplier['name'][:75],
            'last_name': 'Supplier',
            'is_staff': False,
            'is_superuser': False,
        }
        supplier_user, user_created = User.objects.update_or_create(
            username=username,
            defaults=user_defaults,
        )
        supplier_user.set_password('password123')
        supplier_user.role = User.Role.PROJECT_OWNER
        supplier_user.save(update_fields=['password', 'role', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser'])
        log_seed_result("Supplier user", username, user_created)
        supplier_user.grant_role(User.Role.VENDOR)

        category_tags = derive_category_tags(supplier['supplier_type'])
        registration_number = f"SUP-{index:03d}"
        vendor, vendor_created = Vendor.objects.update_or_create(
            user=supplier_user,
            defaults={
                'business_name': supplier['name'],
                'registration_number': registration_number,
                'verified_status': 'APPROVED',
                'country': kenya,
                'location_text': supplier['location'],
                'formatted_address': supplier['location'],
                'location_hierarchy': {
                    'country': 'Kenya',
                    'city': supplier['location'].split(',')[0],
                },
                'provides_delivery': supplier['supplier_type'] != 'service',
                'delivery_radius_km': 120 if supplier['supplier_type'] == 'material' else 40,
                'categories_served': [tag for tag in category_tags if tag in categories],
            }
        )
        log_seed_result("Vendor profile", vendor.business_name, vendor_created)
        vendors.append(vendor)

    return vendors


def seed_vendor(users, categories=None):
    """Backward-compatible wrapper for scripts that still expect a single vendor."""
    categories = categories or seed_taxonomy()
    vendors = seed_vendors(users, categories)
    return vendors[0] if vendors else None


def seed_contractor(users):
    """Create a contractor profile with approved role grant."""
    contractor_user = users.get('CONTRACTOR')
    if not contractor_user:
        logger.warning("⚠️ No contractor user found, skipping contractor profile")
        return None

    contractor, created = ContractorProfile.objects.update_or_create(
        user=contractor_user,
        defaults={
            'company_name': 'Precision Build Partners',
            'service_categories': ['Masonry', 'Electrical'],
            'location_text': 'Nairobi, Kenya',
            'verified_status': ContractorProfile.Status.APPROVED,
        }
    )
    log_seed_result("Contractor profile", contractor.company_name, created)
    if contractor.verified_status == ContractorProfile.Status.APPROVED:
        contractor.user.grant_role(User.Role.CONTRACTOR)
    return contractor


def seed_courier(users):
    """Create a courier profile with approved role grant."""
    courier_user = users.get('COURIER')
    if not courier_user:
        logger.warning("⚠️ No courier user found, skipping courier profile")
        return None

    courier, created = CourierProfile.objects.update_or_create(
        user=courier_user,
        defaults={
            'company_name': 'SwiftSite Logistics',
            'registration_number': 'CR-998877',
            'tax_pin': 'P051234567X',
            'support_email': courier_user.email,
            'support_phone': '+254700111222',
            'location_text': 'Nairobi, Kenya',
            'status': 'APPROVED',
            'is_active': True,
            'submitted_at': timezone.now() - timedelta(days=5),
            'reviewed_at': timezone.now() - timedelta(days=2),
        }
    )
    log_seed_result("Courier profile", courier.company_name, created)
    if courier.status == 'APPROVED':
        courier.user.grant_role(User.Role.COURIER)
    return courier


def seed_countries():
    """Create a minimal operating-country registry for location-aware flows."""
    countries = [
        ('KE', 'Kenya', '🇰🇪', '+254', 'KES', True),
        ('UG', 'Uganda', '🇺🇬', '+256', 'UGX', False),
        ('TZ', 'Tanzania', '🇹🇿', '+255', 'TZS', False),
        ('RW', 'Rwanda', '🇷🇼', '+250', 'RWF', False),
        ('BI', 'Burundi', '🇧🇮', '+257', 'BIF', False),
        ('SS', 'South Sudan', '🇸🇸', '+211', 'SSP', False),
        ('ET', 'Ethiopia', '🇪🇹', '+251', 'ETB', False),
    ]

    for iso_code, name, flag, prefix, currency, is_default in countries:
        country, created = Country.objects.update_or_create(
            iso_code=iso_code,
            defaults={
                'name': name,
                'flag_emoji': flag,
                'phone_prefix': prefix,
                'default_currency': currency,
                'is_default': is_default,
                'is_active': True,
            }
        )
        log_seed_result("Country", f"{name} ({iso_code})", created)


def seed_products(vendors, categories):
    """Create sample products from a normalized slice of the material export."""
    if not vendors:
        logger.warning("⚠️ No vendor available, skipping products")
        return

    certification_registries = [
        {
            'name': 'KEBS Quality Mark',
            'code': 'KEBS',
            'issuer': 'Kenya Bureau of Standards',
            'description': 'Kenya quality and conformity mark for construction products.',
        },
        {
            'name': 'ISO 9001',
            'code': 'ISO9001',
            'issuer': 'International Organization for Standardization',
            'description': 'Quality management systems certification.',
        },
        {
            'name': 'CE Marking',
            'code': 'CE',
            'issuer': 'European Economic Area',
            'description': 'Conformity mark for products sold into EEA markets.',
        },
    ]

    registry_map = {}
    for entry in certification_registries:
        registry, created = ProductCertificationRegistry.objects.update_or_create(
            code=entry['code'],
            defaults=entry,
        )
        registry_map[entry['code']] = registry
        log_seed_result("Material certification registry", entry['name'], created)

    for index, seed in enumerate(SPECIFICATION_PRODUCT_EXPORT):
        category = categories.get(seed['category_code'])
        if not category:
            logger.warning(f"⚠️ Missing category {seed['category_code']} for {seed['name']}, skipping")
            continue

        vendor = vendors[index % len(vendors)]
        normalized_seed = {
            **seed,
            'brand': vendor.business_name,
            'country_of_origin': 'Kenya',
            'quality_grade': 'Reference export',
            'delivery_regions': ['NAIROBI', 'MOMBASA', 'KISUMU', 'NAKURU'],
            'stock_quantity': 25 + (index * 3),
            'reorder_level': 8,
            'bulk_threshold': 12 if seed.get('units') in {'NO', 'PRS'} else 30,
            'packaging_details': f"{seed.get('units') or 'NO'} catalog unit from imported legacy schedule",
            'attribute_entries': [
                {'group': 'Commercial', 'name': 'Legacy Rate', 'value': str(seed['cpurate']), 'unit': 'KES', 'is_highlight': True},
                {'group': 'Reference', 'name': 'Specification ID', 'value': seed['specificationid'], 'unit': '', 'is_highlight': True},
                {'group': 'Reference', 'name': 'Material ID', 'value': seed['materialid'], 'unit': '', 'is_highlight': False},
            ],
            'documents': [
                {
                    'document_type': 'DATASHEET',
                    'title': f"{seed['specificationid']} legacy schedule extract",
                    'external_url': f"https://example.com/legacy-materials/{seed['specificationid'].lower()}.pdf",
                    'description': 'Imported reference row from the construction materials export.',
                    'is_public': True,
                }
            ],
        }
        seed_product_record(vendor, category, registry_map, normalized_seed)


def seed_projects_and_contracts(users):
    """Create sample projects and contracts."""
    owner = users.get('PROJECT_OWNER')
    if not owner:
        logger.warning("⚠️ No project owner found, skipping projects")
        return

    # Create Project
    project, created = Project.objects.update_or_create(
        owner=owner,
        title='Skyline Apartment Wing A',
        defaults={
            'description': 'A 12-story residential development in Westlands.',
            'location_text': 'Westlands, Nairobi',
            'estimated_budget': 1500000.00,
            'status': 'FUNDING_OPEN'
        }
    )
    log_seed_result("Project", project.title, created)

    # Create Contract
    contract, created = Contract.objects.update_or_create(
        owner=owner,
        title='Masonry and Foundation Works - Wing A',
        defaults={
            'description_scope': 'Complete foundation excavation and masonry for first 3 floors.',
            'location': 'Westlands, Nairobi',
            'budget_min': 50000.00,
            'budget_max': 75000.00,
            'status': 'BIDDING'
        }
    )
    log_seed_result("Contract", contract.title, created)

    return project


def seed_government_tenders():
    """Create sample public tenders."""
    tender, created = PublicTender.objects.update_or_create(
        title='Expressway Maintenance Project - 2026',
        defaults={
            'description': 'Routine maintenance of the Nairobi-Mombasa highway segments.',
            'issuing_authority': 'Roads Authority (KENHA)',
            'bid_deadline': timezone.now() + timedelta(days=30),
            'status': 'OPEN'
        }
    )
    log_seed_result("Public tender", tender.title, created)


def seed_investor_data(users, project):
    """Create investor profile and agreement."""
    investor_user = users.get('INVESTOR')
    if not investor_user or not project:
        logger.warning("⚠️ Missing investor or project, skipping investor data")
        return

    # Create Investor Profile
    inv_profile, created = InvestorProfile.objects.update_or_create(
        user=investor_user,
        defaults={
            'kyc_status': 'VERIFIED',
            'accreditation_status': 'ACCREDITED',
            'jurisdiction': 'Kenya'
        }
    )
    log_seed_result("Investor profile", investor_user.username, created)
    if inv_profile.kyc_status == InvestorProfile.KYCStatus.VERIFIED:
        investor_user.grant_role(User.Role.INVESTOR)

    # Create Investment Agreement
    agreement, created = InvestmentAgreement.objects.update_or_create(
        project=project,
        investor=investor_user,
        amount=50000.00,
        defaults={'status': 'DRAFT'}
    )
    log_seed_result("Investment agreement", str(agreement), created)


def run_all():
    """Run all seeding functions in order."""
    log_seed_banner("🚀 Starting Ujenzi Marketplace Data Seeding")

    try:
        # 1. Seed operating countries for location-aware workflows
        seed_countries()

        # 2. Seed taxonomy first (needed for products)
        categories = seed_taxonomy()

        # 3. Seed users
        users = seed_users()

        # 4. Seed specialized approved profiles
        vendors = seed_vendors(users, categories)
        seed_contractor(users)
        seed_courier(users)

        # 5. Seed products
        seed_products(vendors, categories)

        # 6. Seed projects and contracts
        project = seed_projects_and_contracts(users)

        # 7. Seed government tenders
        seed_government_tenders()

        # 8. Seed investor data
        seed_investor_data(users, project)

        log_seed_banner("✅ Base Marketplace Seeding Complete")
        logger.info("\nDefault Credentials:")
        logger.info("  Admin: admin / adminpassword123")
        logger.info("  Others: <username> / password123")
        logger.info("    - owner (PROJECT_OWNER)")
        logger.info("    - contractor (CONTRACTOR)")
        logger.info("    - vendor (VENDOR)")
        logger.info("    - investor (INVESTOR)")
        logger.info("    - gov (GOVERNMENT)")
        logger.info("    - courier (COURIER)")

    except Exception as e:
        logger.error(f"❌ Seeding failed: {e}")
        raise


if __name__ == '__main__':
    run_all()
