from django.test import TestCase

from .models import Country
from .services import ensure_default_countries


class CountryBootstrapTests(TestCase):
    def test_ensure_default_countries_populates_empty_registry(self):
        self.assertEqual(Country.objects.count(), 0)

        created = ensure_default_countries()

        self.assertTrue(created)
        self.assertGreater(Country.objects.count(), 0)
        self.assertTrue(Country.objects.filter(iso_code='KE', name='Kenya').exists())

    def test_ensure_default_countries_is_idempotent_when_registry_exists(self):
        Country.objects.create(
            iso_code='KE',
            name='Kenya',
            flag_emoji='🇰🇪',
            phone_prefix='+254',
            default_currency='KES',
            is_default=True,
        )

        created = ensure_default_countries()

        self.assertFalse(created)
        self.assertEqual(Country.objects.filter(iso_code='KE').count(), 1)
