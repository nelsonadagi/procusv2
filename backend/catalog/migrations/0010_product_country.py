from django.db import migrations, models
import django.db.models.deletion


def backfill_product_country(apps, schema_editor):
    Product = apps.get_model('catalog', 'Product')
    Country = apps.get_model('platform_settings', 'Country')

    default_country = Country.objects.filter(is_default=True, is_active=True).first() or Country.objects.filter(is_active=True).order_by('name').first()

    for product in Product.objects.select_related('vendor__country').all():
        if product.country_id:
            continue
        vendor_country_id = getattr(getattr(product.vendor, 'country', None), 'id', None)
        if vendor_country_id:
            product.country_id = vendor_country_id
        elif default_country:
            product.country_id = default_country.id
        product.save(update_fields=['country'])


class Migration(migrations.Migration):

    dependencies = [
        ('platform_settings', '0011_alter_currencyrate_rate_to_default'),
        ('catalog', '0009_product_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='platform_settings.country', verbose_name='Product Country'),
        ),
        migrations.RunPython(backfill_product_country, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='product',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='platform_settings.country', verbose_name='Product Country'),
        ),
    ]
