import pytest
from django.urls import reverse
from rest_framework import status
from vendors.models import Vendor

@pytest.mark.django_db
class TestVendorAPI:
    def test_list_vendors(self, api_client, vendor):
        url = reverse('vendors-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_create_vendor(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        url = reverse('vendors-list')
        data = {
            'user': admin_user.id,
            'business_name': 'New Vendor Corp',
            'registration_number': 'REG123',
            'location': 'Downtown'
        }
        response = api_client.post(url, data)
        # Note: In some setups, the user might be automatically set to the authenticated user
        assert response.status_code == status.HTTP_201_CREATED
        assert Vendor.objects.filter(business_name='New Vendor Corp').exists()

    def test_vendor_verification(self, api_client, admin_user, vendor):
        # Create a vendor profile for the vendor user
        v_profile = Vendor.objects.create(
            user=vendor,
            business_name="Test Vendor",
            registration_number="REG456",
            location="Uptown"
        )
        
        api_client.force_authenticate(user=admin_user)
        url = reverse('vendors-detail', args=[v_profile.id])
        
        # Patch verification status
        response = api_client.patch(url, {'verified_status': 'APPROVED'})
        assert response.status_code == status.HTTP_200_OK
        v_profile.refresh_from_db()
        assert v_profile.verified_status == 'APPROVED'

    def test_vendor_me(self, api_client, vendor):
        Vendor.objects.create(
            user=vendor,
            business_name="Me Vendor",
            registration_number="REG789",
            location="Nairobi",
            verified_status='APPROVED'
        )
        api_client.force_authenticate(user=vendor)
        url = reverse('vendors-me')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['business_name'] == "Me Vendor"
