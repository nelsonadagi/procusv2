import pytest
from django.urls import reverse
from rest_framework import status
from bids.models import Bid
from contractors.models import ContractorProfile

@pytest.mark.django_db
class TestBidsAPI:
    def test_list_bids(self, api_client, project_owner):
        api_client.force_authenticate(user=project_owner)
        url = reverse('bid-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_submit_bid(self, api_client, contractor, project_owner):
        # Setup contractor profile
        cp = ContractorProfile.objects.create(
            user=contractor,
            company_name="Contr Inc",
            service_categories=[],
            operating_region="City"
        )
        
        # Setup contract
        from conftest import ContractFactory
        contract = ContractFactory(owner=project_owner)
        
        api_client.force_authenticate(user=contractor)
        url = reverse('bid-list')
        data = {
            'contract': contract.id,
            'contractor': cp.id,
            'proposed_cost': 2500,
            'proposed_timeline_days': 45,
            'message': 'Work'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Bid.objects.filter(proposed_cost=2500).exists()

    def test_award_bid(self, api_client, project_owner, contractor):
        # Setup contractor profile
        cp, _ = ContractorProfile.objects.get_or_create(
            user=contractor,
            defaults={'company_name':"B", 'operating_region':"R", 'service_categories':[]}
        )
        
        # Setup contract
        from conftest import ContractFactory
        contract = ContractFactory(owner=project_owner, status='POSTED')
        bid = Bid.objects.create(contract=contract, contractor=cp, proposed_cost=1000, proposed_timeline_days=5)
        
        api_client.force_authenticate(user=project_owner)
        url = reverse('bid-award', args=[bid.id])
        response = api_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        bid.refresh_from_db()
        assert bid.status == 'AWARDED'
        contract.refresh_from_db()
        assert contract.status == 'AWARDED'

    def test_list_bids_contractor(self, api_client, contractor, project_owner):
        cp, _ = ContractorProfile.objects.get_or_create(
            user=contractor,
            defaults={'company_name':"C", 'operating_region':"R", 'service_categories':[]}
        )
        from conftest import ContractFactory
        contract = ContractFactory(owner=project_owner)
        Bid.objects.create(contract=contract, contractor=cp, proposed_cost=500, proposed_timeline_days=10)
        
        api_client.force_authenticate(user=contractor)
        url = reverse('bid-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

    def test_shortlist_bid(self, api_client, project_owner, contractor):
        cp, _ = ContractorProfile.objects.get_or_create(
            user=contractor,
            defaults={'company_name':"C", 'operating_region':"R", 'service_categories':[]}
        )
        from conftest import ContractFactory
        contract = ContractFactory(owner=project_owner)
        bid = Bid.objects.create(contract=contract, contractor=cp, proposed_cost=500, proposed_timeline_days=10)
        
        api_client.force_authenticate(user=project_owner)
        url = reverse('bid-shortlist', args=[bid.id])
        response = api_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        bid.refresh_from_db()
        assert bid.status == Bid.Status.SHORTLISTED

    def test_shortlist_bid_unauthorized(self, api_client, project_owner, contractor):
        cp, _ = ContractorProfile.objects.get_or_create(
            user=contractor,
            defaults={'company_name':"C", 'operating_region':"R", 'service_categories':[]}
        )
        from conftest import ContractFactory
        contract = ContractFactory(owner=project_owner)
        bid = Bid.objects.create(contract=contract, contractor=cp, proposed_cost=500, proposed_timeline_days=10)
        
        # A contractor can "see" their own bid, so get_object won't 404, but they can't shortlist it.
        api_client.force_authenticate(user=contractor)
        url = reverse('bid-shortlist', args=[bid.id])
        response = api_client.post(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_award_bid_unauthorized(self, api_client, project_owner, contractor):
        cp, _ = ContractorProfile.objects.get_or_create(
            user=contractor,
            defaults={'company_name':"C", 'operating_region':"R", 'service_categories':[]}
        )
        from conftest import ContractFactory
        contract = ContractFactory(owner=project_owner)
        bid = Bid.objects.create(contract=contract, contractor=cp, proposed_cost=500, proposed_timeline_days=10)
        
        # A contractor can "see" their own bid, so get_object won't 404, but they can't award it.
        api_client.force_authenticate(user=contractor)
        url = reverse('bid-award', args=[bid.id])
        response = api_client.post(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_submit_bid_non_contractor(self, api_client, project_owner):
        from conftest import ContractFactory
        contract = ContractFactory(owner=project_owner)
        
        api_client.force_authenticate(user=project_owner)
        url = reverse('bid-list')
        data = {
            'contract': contract.id,
            'proposed_cost': 2500,
            'proposed_timeline_days': 45
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
