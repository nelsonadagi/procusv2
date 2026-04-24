import uuid

from django.db import migrations, models


def populate_category_uuids(apps, schema_editor):
    Category = apps.get_model('taxonomy', 'Category')
    for category in Category.objects.filter(uuid__isnull=True):
        category.uuid = uuid.uuid4()
        category.save(update_fields=['uuid'])


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0002_alter_category_options_alter_category_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='uuid',
            field=models.UUIDField(blank=True, editable=False, null=True),
        ),
        migrations.RunPython(populate_category_uuids, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='category',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
