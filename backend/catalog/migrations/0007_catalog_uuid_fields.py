import uuid

from django.db import migrations, models


def populate_catalog_uuids(apps, schema_editor):
    model_names = [
        'Product',
        'ProductImage',
        'ProductCertificationRegistry',
        'ProductCertification',
        'ProductAttribute',
        'ProductDocument',
    ]

    for model_name in model_names:
        Model = apps.get_model('catalog', model_name)
        for row in Model.objects.filter(uuid__isnull=True):
            row.uuid = uuid.uuid4()
            row.save(update_fields=['uuid'])


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_productcertificationregistry_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='uuid',
            field=models.UUIDField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='productimage',
            name='uuid',
            field=models.UUIDField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='productcertificationregistry',
            name='uuid',
            field=models.UUIDField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='productcertification',
            name='uuid',
            field=models.UUIDField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='productattribute',
            name='uuid',
            field=models.UUIDField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='productdocument',
            name='uuid',
            field=models.UUIDField(blank=True, editable=False, null=True),
        ),
        migrations.RunPython(populate_catalog_uuids, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='product',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='productcertificationregistry',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='productcertification',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='productattribute',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='productdocument',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
