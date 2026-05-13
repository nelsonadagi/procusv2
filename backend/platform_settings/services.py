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
    platform_settings = PlatformSettings.objects.filter(is_active=True).first()
    if not platform_settings:
        print("No active PlatformSettings found.")
        return False

    base_currency = platform_settings.default_currency

    configs = list(ExchangeRateConfig.objects.filter(active=True).order_by('-is_default', 'display_order', 'label'))
    if not configs:
        print("No active ExchangeRateConfig found.")
        return False

    for config in configs:
        if _sync_currency_rates_from_config(config, base_currency):
            return True

    return False


def _build_exchange_rate_url(config, base_currency):
    if config.provider == ExchangeRateConfig.Provider.FRANKFURTER:
        default_url = "https://api.frankfurter.dev/v1/latest?base=BASE"
    elif config.provider == ExchangeRateConfig.Provider.EXCHANGE_RATE_API:
        default_url = "https://v6.exchangerate-api.com/v6/KEY/latest/BASE"
    else:
        default_url = config.base_url

    url = config.base_url or default_url
    if config.api_key:
        url = url.replace('{KEY}', config.api_key).replace('KEY', config.api_key)
    return url.replace('{BASE}', base_currency).replace('BASE', base_currency)


def _extract_rates(config, data):
    mapping = config.mapping_config or {}
    if config.provider == ExchangeRateConfig.Provider.FRANKFURTER:
        return data.get('rates') if isinstance(data, dict) else None
    if config.provider == ExchangeRateConfig.Provider.EXCHANGE_RATE_API:
        if isinstance(data, dict):
            return data.get('conversion_rates') or data.get('rates')
        return None

    rates_key = mapping.get('rates_key', 'rates')
    rates = data
    for key in rates_key.split('.'):
        if not isinstance(rates, dict):
            return None
        rates = rates.get(key)
    return rates if isinstance(rates, dict) else None


def _sync_currency_rates_from_config(config, base_currency):
    url = _build_exchange_rate_url(config, base_currency)
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error fetching exchange rates from {config.label} ({config.provider}): {e}")
        return False

    rates = _extract_rates(config, data)
    if not rates or not isinstance(rates, dict):
        print(f"Could not find rates dictionary for {config.label} using provider {config.provider}")
        return False

    available_currencies = CurrencyRate.objects.filter(is_active=True)
    updated_codes = set()
    for currency in available_currencies:
        if currency.currency_code == base_currency:
            currency.rate_to_default = Decimal('1')
            currency.save(update_fields=['rate_to_default', 'updated_at'])
            updated_codes.add(currency.currency_code)
            continue

        rate = rates.get(currency.currency_code)
        if rate is None:
            continue
        try:
            currency.rate_to_default = Decimal(str(rate))
            currency.save(update_fields=['rate_to_default', 'updated_at'])
            updated_codes.add(currency.currency_code)
        except Exception as e:
            print(f"Error updating rate for {currency.currency_code}: {e}")

    config.last_sync = timezone.now()
    config.save(update_fields=['last_sync'])
    return bool(updated_codes or rates)
