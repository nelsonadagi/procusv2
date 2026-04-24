from django.db import migrations
from django.contrib.gis.geos import Point

def populate_locations(apps, schema_editor):
    Location = apps.get_model('platform_settings', 'Location')
    Vendor = apps.get_model('vendors', 'Vendor')
    Project = apps.get_model('projects', 'Project')
    PropertyListing = apps.get_model('property', 'PropertyListing')
    ContractorProfile = apps.get_model('contractors', 'ContractorProfile')
    
    # Simple migration: Create Location record from location_text
    
    for vendor in Vendor.objects.all():
        if vendor.location_text and not vendor.location:
            try:
                point = None
                if vendor.latitude and vendor.longitude:
                    point = Point(float(vendor.longitude), float(vendor.latitude))
                
                loc = Location.objects.create(
                    address=vendor.formatted_address or vendor.location_text,
                    point=point,
                    metadata=vendor.location_hierarchy or {}
                )
                vendor.location = loc
                vendor.save()
            except Exception as e:
                print(f"Error migrating vendor {vendor.id}: {e}")
            
    for project in Project.objects.all():
        if project.location_text and not project.location:
            loc = Location.objects.create(address=project.location_text)
            project.location = loc
            project.save()
            
    for prop in PropertyListing.objects.all():
        if prop.location_text and not prop.location:
            loc = Location.objects.create(address=prop.location_text)
            prop.location = loc
            prop.save()
            
    for contractor in ContractorProfile.objects.all():
        if contractor.operating_region and not contractor.location:
            loc = Location.objects.create(address=contractor.operating_region)
            contractor.location = loc
            contractor.save()

class Migration(migrations.Migration):
    dependencies = [
        ('platform_settings', '0005_location'),
        ('vendors', '0006_vendor_location_text_alter_vendor_location'),
        ('projects', '0003_project_location_text_alter_project_location'),
        ('property', '0002_propertylisting_location_text_and_more'),
        ('contractors', '0003_contractorprofile_location'),
    ]

    operations = [
        migrations.RunPython(populate_locations, reverse_code=migrations.RunPython.noop),
    ]
