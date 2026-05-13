#!/usr/bin/env python
"""
Seed sample payment gateway configurations.
Safe to rerun independently; writes are idempotent.
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

import logging
from platform_settings.models import PaymentGatewayConfig

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s', stream=sys.stdout)


def log_seed_banner(title):
    logger.info("=" * 60)
    logger.info(title)
    logger.info("=" * 60)


def seed_payment_gateways():
    log_seed_banner("💳 Starting Payment Gateway Seed")
    sample_gateways = [
        {
            'provider': PaymentGatewayConfig.Provider.MPESA,
            'label': 'M-Pesa Sandbox',
            'public_key': 'mpesa-sandbox-public',
            'secret_key': 'mpesa-sandbox-secret',
            'webhook_secret': 'mpesa-webhook-secret',
            'instructions': 'Simulated STK push flow. Use this for mobile money checkout in Kenya.',
            'enabled_regions': ['KE'],
            'display_order': 1,
            'is_default': True,
            'is_test_mode': True,
        },
        {
            'provider': PaymentGatewayConfig.Provider.STRIPE,
            'label': 'Stripe Test',
            'public_key': 'stripe-test-public',
            'secret_key': 'stripe-test-secret',
            'webhook_secret': 'stripe-webhook-secret',
            'instructions': 'Simulated card checkout flow for international payments.',
            'enabled_regions': ['KE', 'US', 'EU'],
            'display_order': 2,
            'is_default': False,
            'is_test_mode': True,
        },
        {
            'provider': PaymentGatewayConfig.Provider.FLUTTERWAVE,
            'label': 'Flutterwave Test',
            'public_key': 'flutterwave-test-public',
            'secret_key': 'flutterwave-test-secret',
            'webhook_secret': 'flutterwave-webhook-secret',
            'instructions': 'Simulated regional gateway for card and wallet flows.',
            'enabled_regions': ['KE', 'UG', 'TZ', 'NG'],
            'display_order': 3,
            'is_default': False,
            'is_test_mode': True,
        },
        {
            'provider': PaymentGatewayConfig.Provider.PAYPAL,
            'label': 'PayPal Sandbox',
            'public_key': 'paypal-sandbox-public',
            'secret_key': 'paypal-sandbox-secret',
            'webhook_secret': 'paypal-webhook-secret',
            'instructions': 'Simulated international checkout method.',
            'enabled_regions': ['US', 'EU', 'KE'],
            'display_order': 4,
            'is_default': False,
            'is_test_mode': True,
        },
    ]

    for payload in sample_gateways:
        secret_key = payload.pop('secret_key')
        gateway, created = PaymentGatewayConfig.objects.update_or_create(
            provider=payload['provider'],
            defaults=payload,
        )
        gateway.secret_key = secret_key
        gateway.save()
        logger.info(f"✅ {'Created' if created else 'Updated'} payment gateway: {gateway.label} ({gateway.provider})")

    log_seed_banner("✅ Payment Gateway Seed Complete")


if __name__ == '__main__':
    seed_payment_gateways()
