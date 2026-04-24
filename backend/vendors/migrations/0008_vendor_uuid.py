import uuid

from django.db import migrations, models


def populate_vendor_uuids(apps, schema_editor):
    Vendor = apps.get_model('vendors', 'Vendor')
    for vendor in Vendor.objects.filter(uuid__isnull=True):
        vendor.uuid = uuid.uuid4()
        vendor.save(update_fields=['uuid'])


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0007_alter_vendor_options_alter_vendor_average_rating_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='uuid',
            field=models.UUIDField(blank=True, editable=False, null=True),
        ),
        migrations.RunPython(populate_vendor_uuids, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='vendor',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
