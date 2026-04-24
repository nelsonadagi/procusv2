from django.core.management.base import BaseCommand
from platform_settings.models import ExchangeRateConfig, CurrencyRate, PlatformSettings

class Command(BaseCommand):
    help = 'Seeds exchange rate configurations and common currencies'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding Exchange Rate Configurations...')

        # 1. ExchangeRate-API
        ExchangeRateConfig.objects.get_or_create(
            provider=ExchangeRateConfig.Provider.EXCHANGE_RATE_API,
            defaults={
                'label': 'ExchangeRate-API (Primary)',
                'base_url': 'https://v6.exchangerate-api.com/v6/KEY/latest/BASE',
                'mapping_config': {'rates_key': 'conversion_rates'},
                'active': True
            }
        )

        # 2. Exchangerate.host
        ExchangeRateConfig.objects.get_or_create(
            provider=ExchangeRateConfig.Provider.EXCHANGERATE_HOST,
            defaults={
                'label': 'Exchangerate.host (Backup)',
                'base_url': 'https://api.exchangerate.host/latest?base=BASE',
                'mapping_config': {'rates_key': 'rates'},
                'active': False
            }
        )

        # 3. Open Exchange Rates
        ExchangeRateConfig.objects.get_or_create(
            provider=ExchangeRateConfig.Provider.OPEN_EXCHANGE_RATES,
            defaults={
                'label': 'Open Exchange Rates',
                'base_url': 'https://openexchangerates.org/api/latest.json?app_id=KEY',
                'mapping_config': {'rates_key': 'rates'},
                'active': False
            }
        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded exchange rate configurations.'))

        self.stdout.write('Seeding common currencies...')
        
        currencies = [
            {'code': 'KES', 'name': 'Kenyan Shilling', 'symbol': 'KSh', 'rate': 130.00},
            {'code': 'EUR', 'name': 'Euro', 'symbol': '€', 'rate': 0.92},
            {'code': 'GBP', 'name': 'British Pound', 'symbol': '£', 'rate': 0.79},
            {'code': 'TZS', 'name': 'Tanzanian Shilling', 'symbol': 'TSh', 'rate': 2500.00},
            {'code': 'UGX', 'name': 'Ugandan Shilling', 'symbol': 'USh', 'rate': 3800.00},
            {'code': 'AED', 'name': 'UAE Dirham', 'symbol': 'DH', 'rate': 3.67},
            {'code': 'CNY', 'name': 'Chinese Yuan', 'symbol': '¥', 'rate': 7.23},
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
                default_currency="USD",
                default_region="KE",
                is_active=True
            )
            self.stdout.write(self.style.SUCCESS('Created default Platform Settings (Base: USD).'))
