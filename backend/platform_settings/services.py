import requests
from django.utils import timezone
from decimal import Decimal
from .models import PlatformSettings, CurrencyRate, ExchangeRateConfig, Country


DEFAULT_COUNTRIES = [
    {
        "iso_code": "KE",
        "name": "Kenya",
        "flag_emoji": "🇰🇪",
        "phone_prefix": "+254",
        "default_currency": "KES",
        "is_default": True,
    },
    {
        "iso_code": "UG",
        "name": "Uganda",
        "flag_emoji": "🇺🇬",
        "phone_prefix": "+256",
        "default_currency": "UGX",
        "is_default": False,
    },
    {
        "iso_code": "TZ",
        "name": "Tanzania",
        "flag_emoji": "🇹🇿",
        "phone_prefix": "+255",
        "default_currency": "TZS",
        "is_default": False,
    },
    {
        "iso_code": "RW",
        "name": "Rwanda",
        "flag_emoji": "🇷🇼",
        "phone_prefix": "+250",
        "default_currency": "RWF",
        "is_default": False,
    },
    {
        "iso_code": "BI",
        "name": "Burundi",
        "flag_emoji": "🇧🇮",
        "phone_prefix": "+257",
        "default_currency": "BIF",
        "is_default": False,
    },
    {
        "iso_code": "SS",
        "name": "South Sudan",
        "flag_emoji": "🇸🇸",
        "phone_prefix": "+211",
        "default_currency": "SSP",
        "is_default": False,
    },
    {
        "iso_code": "ET",
        "name": "Ethiopia",
        "flag_emoji": "🇪🇹",
        "phone_prefix": "+251",
        "default_currency": "ETB",
        "is_default": False,
    },
]


def ensure_default_countries():
    """
    Ensure the platform has a minimal country registry.

    This keeps location-aware onboarding usable in fresh environments where
    Country rows have not been seeded yet.
    """
    if Country.objects.exists():
        return False

    for country_data in DEFAULT_COUNTRIES:
        Country.objects.create(**country_data)

    return True

def update_currency_rates():
    """
    Fetch latest exchange rates from the configured API and update CurrencyRate model.
    """
    config = ExchangeRateConfig.objects.filter(active=True).first()
    if not config:
        print("No active ExchangeRateConfig found.")
        return False

    platform_settings = PlatformSettings.objects.filter(is_active=True).first()
    if not platform_settings:
        print("No active PlatformSettings found.")
        return False

    base_currency = platform_settings.default_currency
    
    # Dynamic URL construction
    # Supports placeholders: {KEY} and {BASE}
    url = config.base_url
    if config.api_key:
        url = url.replace('{KEY}', config.api_key).replace('KEY', config.api_key)
    url = url.replace('{BASE}', base_currency).replace('BASE', base_currency)

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error fetching exchange rates: {e}")
        return False

    # Get mapping config
    mapping = config.mapping_config or {}
    
    # Handle different providers default behaviors if mapping is empty
    if not mapping and config.provider == ExchangeRateConfig.Provider.EXCHANGE_RATE_API:
        rates_key = 'conversion_rates'
    elif not mapping and config.provider == ExchangeRateConfig.Provider.OPEN_EXCHANGE_RATES:
        rates_key = 'rates'
    else:
        rates_key = mapping.get('rates_key', 'rates')

    # Nested key resolution (e.g. 'data.rates')
    rates = data
    try:
        for key in rates_key.split('.'):
            if rates:
                rates = rates.get(key)
    except Exception:
        rates = None

    if not rates or not isinstance(rates, dict):
        print(f"Could not find rates dictionary in response using key '{rates_key}'")
        return False

    # Update active CurrencyRate objects
    count = 0
    available_currencies = CurrencyRate.objects.filter(is_active=True)
    for currency in available_currencies:
        rate = rates.get(currency.currency_code)
        if rate:
            try:
                currency.rate_to_default = Decimal(str(rate))
                currency.save()
                count += 1
            except Exception as e:
                print(f"Error updating rate for {currency.currency_code}: {e}")
    
    config.last_sync = timezone.now()
    config.save()
    
    return True
