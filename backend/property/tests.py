import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status

from platform_settings.models import Country
from property.models import (
    PropertyListing,
    PropertyInquiry,
    PropertyAvailabilityWindow,
    PropertyAppointment,
    PropertySpecification,
    PropertyPricingProfile,
    PropertyFeature,
    PropertyMediaAsset,
)
from taxonomy.models import Category, TaxonomyType


@pytest.mark.django_db
class TestPropertyAPI:
    def test_property_operator_can_create_rich_listing(self, api_client, project_owner):
        api_client.force_authenticate(user=project_owner)

        response = api_client.post(
            reverse('propertylisting-list'),
            {
                'title': 'Modern Residential Block',
                'description': 'A rich property profile for sale.',
                'asset_type': PropertyListing.Type.RESIDENTIAL,
                'listing_type': PropertyListing.ListingType.SALE,
                'price_estimate': '18000000.00',
                'location_text': 'Westlands, Nairobi',
                'development_metadata': {
                    'zoning_info': 'Residential',
                    'build_ready': True,
                    'utilities_available': ['Water', 'Power'],
                    'development_stage': 'COMPLETED',
                },
                'specification': {
                    'bedrooms': 4,
                    'bathrooms': 3,
                    'internal_area': '220.00',
                    'internal_area_unit': 'SQM',
                },
                'pricing_profile': {
                    'currency': 'KES',
                    'asking_price': '18000000.00',
                    'pricing_strategy': 'NEGOTIABLE',
                },
                'features': [
                    {'name': 'Backup Generator', 'category': 'Utilities', 'is_highlighted': True},
                    {'name': 'Rooftop Terrace', 'category': 'Lifestyle'},
                ],
            },
            format='json',
        )

        assert response.status_code == status.HTTP_201_CREATED
        prop = PropertyListing.objects.get(title='Modern Residential Block')
        assert PropertySpecification.objects.filter(property=prop, bedrooms=4).exists()
        assert PropertyPricingProfile.objects.filter(property=prop, currency='KES').exists()
        assert PropertyFeature.objects.filter(property=prop, name='Backup Generator').exists()

    def test_anonymous_property_inquiry_creates_lead(self, api_client, project_owner):
        prop = PropertyListing.objects.create(
            owner=project_owner,
            title='Riverside Asset',
            description='Standalone asset',
            asset_type=PropertyListing.Type.RESIDENTIAL,
            price_estimate=100000,
        )

        response = api_client.post(
            reverse('property-inquiry-list'),
            {
                'property': prop.id,
                'full_name': 'Anonymous Visitor',
                'email': 'visitor@example.com',
                'message': 'I would like more details.',
            },
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert PropertyInquiry.objects.filter(property=prop, email='visitor@example.com').exists()

    def test_property_list_supports_rich_filters(self, api_client, project_owner):
        country = Country.objects.create(iso_code='KE', name='Kenya', is_active=True)
        purpose = Category.objects.create(
            name='Apartments',
            slug='apartments',
            taxonomy_type=TaxonomyType.PROPERTY,
            active=True,
        )
        matching = PropertyListing.objects.create(
            owner=project_owner,
            title='Modern Finance Ready Apartments',
            description='High quality residential inventory',
            asset_type=PropertyListing.Type.RESIDENTIAL,
            listing_type=PropertyListing.ListingType.SALE,
            price_estimate=150000,
            financing_allowed=True,
            country=country,
            purpose=purpose,
            location_text='Westlands, Nairobi',
            latitude='-1.267000000',
            longitude='36.810000000',
        )
        other = PropertyListing.objects.create(
            owner=project_owner,
            title='Industrial Shell Site',
            description='Raw industrial yard',
            asset_type=PropertyListing.Type.INDUSTRIAL,
            listing_type=PropertyListing.ListingType.SALE,
            price_estimate=90000,
            financing_allowed=False,
            location_text='Athi River',
        )

        PropertySpecification.objects.create(
            property=matching,
            bedrooms=3,
            bathrooms=2,
            occupancy_status='VACANT',
            condition_rating='EXCELLENT',
        )
        PropertyPricingProfile.objects.create(
            property=matching,
            currency='KES',
            asking_price='145000.00',
            pricing_strategy='NEGOTIABLE',
        )
        PropertyFeature.objects.create(
            property=matching,
            name='Rooftop Terrace',
            category='Lifestyle',
            is_highlighted=True,
        )
        PropertySpecification.objects.create(
            property=other,
            bedrooms=0,
            bathrooms=1,
            occupancy_status='UNDER_CONSTRUCTION',
            condition_rating='SHELL',
        )

        response = api_client.get(
            reverse('propertylisting-list'),
            {
                'asset_type': 'RESIDENTIAL',
                'financing_allowed': 'true',
                'min_bedrooms': 2,
                'pricing_strategy': 'NEGOTIABLE',
                'feature': 'Rooftop',
                'purpose': 'apartments',
                'country': country.id,
                'location': 'Nairobi',
            },
        )

        assert response.status_code == status.HTTP_200_OK
        results = response.data.get('results', response.data)
        ids = {item['id'] for item in results}
        assert str(matching.id) in ids
        assert str(other.id) not in ids

    def test_owner_can_create_availability_window(self, api_client, project_owner):
        api_client.force_authenticate(user=project_owner)
        prop = PropertyListing.objects.create(
            owner=project_owner,
            title='Industrial Site',
            description='Managed asset',
            asset_type=PropertyListing.Type.INDUSTRIAL,
            price_estimate=250000,
        )

        response = api_client.post(
            reverse('property-availability-window-list'),
            {
                'property': prop.id,
                'start_at': '2026-05-01T09:00:00Z',
                'end_at': '2026-05-01T12:00:00Z',
                'slot_duration_minutes': 60,
            },
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert PropertyAvailabilityWindow.objects.filter(property=prop).count() == 1

    def test_anonymous_appointment_booking_creates_record(self, api_client, project_owner):
        prop = PropertyListing.objects.create(
            owner=project_owner,
            title='Appointment Asset',
            description='Bookable site',
            asset_type=PropertyListing.Type.COMMERCIAL,
            price_estimate=400000,
        )
        window = PropertyAvailabilityWindow.objects.create(
            property=prop,
            managed_by=project_owner,
            start_at='2026-05-02T10:00:00Z',
            end_at='2026-05-02T12:00:00Z',
            slot_duration_minutes=60,
        )

        response = api_client.post(
            reverse('property-appointment-list'),
            {
                'property': prop.id,
                'availability_window': window.id,
                'full_name': 'Prospective Buyer',
                'phone_number': '+254700000000',
                'scheduled_start': '2026-05-02T10:00:00Z',
                'scheduled_end': '2026-05-02T11:00:00Z',
            },
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert PropertyAppointment.objects.filter(property=prop, full_name='Prospective Buyer').exists()

    def test_owner_can_upload_multiple_property_media_files(self, api_client, project_owner):
        api_client.force_authenticate(user=project_owner)
        prop = PropertyListing.objects.create(
            owner=project_owner,
            title='Media Ready Asset',
            description='Managed asset',
            asset_type=PropertyListing.Type.RESIDENTIAL,
            price_estimate=250000,
        )

        url = reverse('propertylisting-upload-media', args=[prop.id])
        image_one = SimpleUploadedFile("front.jpg", b"front_image", content_type="image/jpeg")
        image_two = SimpleUploadedFile("rear.jpg", b"rear_image", content_type="image/jpeg")

        response = api_client.post(
            url,
            {'files': [image_one, image_two], 'media_type': PropertyMediaAsset.MediaType.IMAGE},
            format='multipart',
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert prop.media_assets.count() == 2
