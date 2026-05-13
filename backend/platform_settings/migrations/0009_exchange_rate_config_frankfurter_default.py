from django.db import migrations, models


def seed_exchange_rate_configs(apps, schema_editor):
    ExchangeRateConfig = apps.get_model('platform_settings', 'ExchangeRateConfig')

    ExchangeRateConfig.objects.filter(provider__in=['EXCHANGERATE_HOST', 'OPEN_EXCHANGE_RATES']).update(
        provider='EXCHANGE_RATE_API'
    )

    ExchangeRateConfig.objects.update_or_create(
        provider='FRANKFURTER',
        defaults={
            'label': 'Frankfurter (Primary)',
            'base_url': 'https://api.frankfurter.dev/v1/latest?base=BASE',
            'active': True,
            'is_default': True,
            'mapping_config': {'rates_key': 'rates'},
        },
    )

    ExchangeRateConfig.objects.filter(provider='FRANKFURTER').update(active=True, is_default=True)


class Migration(migrations.Migration):

    dependencies = [
        ('platform_settings', '0008_paymentgatewayconfig_display_order_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchangerateconfig',
            name='provider',
            field=models.CharField(choices=[('FRANKFURTER', 'Frankfurter'), ('EXCHANGE_RATE_API', 'ExchangeRate-API'), ('CUSTOM', 'Custom API')], default='FRANKFURTER', max_length=32),
        ),
        migrations.AddField(
            model_name='exchangerateconfig',
            name='is_default',
            field=models.BooleanField(default=False, help_text='Use this provider as the default sync source'),
        ),
        migrations.RunPython(seed_exchange_rate_configs, migrations.RunPython.noop),
    ]
