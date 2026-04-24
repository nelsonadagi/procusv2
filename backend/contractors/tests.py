import pytest
from django.urls import reverse
from rest_framework import status
from contractors.models import ContractorProfile

@pytest.mark.django_db
class TestContractorsAPI:
    def test_list_contractors(self, api_client, contractor):
        api_client.force_authenticate(user=contractor)
        url = reverse('contractor-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_register_contractor(self, api_client, contractor):
        # Ensure user doesn't have a profile yet
        ContractorProfile.objects.filter(user=contractor).delete()
        
        api_client.force_authenticate(user=contractor)
        url = reverse('contractor-register')
        data = {
            'company_name': 'My Construction Co',
            'service_categories': ['Roofing'],
            'operating_region': 'Nairobi',
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED, f"Failed: {response.data}"
        assert ContractorProfile.objects.filter(company_name='My Construction Co').exists()

    def test_register_contractor_exists(self, api_client, contractor):
        # Create profile first
        ContractorProfile.objects.get_or_create(
            user=contractor,
            defaults={
                'company_name': 'Existing', 
                'operating_region': 'Nairobi',
                'service_categories': ['General']
            }
        )
        api_client.force_authenticate(user=contractor)
        url = reverse('contractor-register')
        response = api_client.post(url, {'company_name': 'New'}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
