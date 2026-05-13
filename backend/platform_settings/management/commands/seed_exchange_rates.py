from django.core.management.base import BaseCommand
from platform_settings.models import ExchangeRateConfig, CurrencyRate, PlatformSettings

class Command(BaseCommand):
    help = 'Seeds exchange rate configurations and common currencies'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding Exchange Rate Configurations...')

        # 1. ExchangeRate-API
        ExchangeRateConfig.objects.get_or_create(
            provider=ExchangeRateConfig.Provider.FRANKFURTER,
            defaults={
                'label': 'Frankfurter (Primary)',
                'base_url': 'https://api.frankfurter.dev/v1/latest?base=BASE',
                'mapping_config': {'rates_key': 'rates'},
                'active': True,
                'is_default': True,
            }
        )

        # 2. ExchangeRate-API
        ExchangeRateConfig.objects.get_or_create(
            provider=ExchangeRateConfig.Provider.EXCHANGE_RATE_API,
            defaults={
                'label': 'ExchangeRate-API (Backup)',
                'base_url': 'https://v6.exchangerate-api.com/v6/KEY/latest/BASE',
                'mapping_config': {'rates_key': 'conversion_rates'},
                'active': False
            }
        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded exchange rate configurations.'))

        self.stdout.write('Seeding common currencies...')
        
        currencies = [
            {'code': 'KES', 'name': 'Kenyan Shilling', 'symbol': 'KSh', 'rate': 1.00},
            {'code': 'RWF', 'name': 'Rwandan Franc', 'symbol': 'RF', 'rate': 0.0071},
            {'code': 'BIF', 'name': 'Burundian Franc', 'symbol': 'FBu', 'rate': 0.0034},
            {'code': 'SSP', 'name': 'South Sudanese Pound', 'symbol': 'SSP', 'rate': 1.00},
            {'code': 'ETB', 'name': 'Ethiopian Birr', 'symbol': 'Br', 'rate': 0.43},
            {'code': 'EUR', 'name': 'Euro', 'symbol': '€', 'rate': 138.50},
            {'code': 'GBP', 'name': 'British Pound', 'symbol': '£', 'rate': 160.00},
            {'code': 'TZS', 'name': 'Tanzanian Shilling', 'symbol': 'TSh', 'rate': 0.051},
            {'code': 'UGX', 'name': 'Ugandan Shilling', 'symbol': 'USh', 'rate': 0.035},
            {'code': 'AED', 'name': 'UAE Dirham', 'symbol': 'DH', 'rate': 35.30},
            {'code': 'CNY', 'name': 'Chinese Yuan', 'symbol': '¥', 'rate': 18.20},
        ]

        for cur in currencies:
            CurrencyRate.objects.get_or_create(
                currency_code=cur['code'],
                defaults={
                    'currency_name': cur['name'],
                    'symbol': cur['symbol'],
                    'rate_to_default': cur['rate'],
                    'is_active': True
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded common currencies.'))
        
        # Ensure a default platform setting exists if not already there
        if not PlatformSettings.objects.exists():
            PlatformSettings.objects.create(
                platform_name="Ujenzi Marketplace",
                default_currency="KES",
                default_region="KE",
                is_active=True
            )
            self.stdout.write(self.style.SUCCESS('Created default Platform Settings (Base: KES).'))

        ExchangeRateConfig.objects.filter(provider=ExchangeRateConfig.Provider.FRANKFURTER).update(is_default=True, active=True)
        ExchangeRateConfig.objects.filter(provider=ExchangeRateConfig.Provider.EXCHANGE_RATE_API).update(is_default=False)
