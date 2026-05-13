import pytest
from django.urls import reverse
from rest_framework import status
from contracts.models import Contract
from bids.models import Bid
from contractors.models import ContractorProfile
from taxonomy.models import Category

@pytest.mark.django_db
class TestContractsAPI:
    def test_list_contracts_public(self, api_client):
        from conftest import ContractFactory
        ContractFactory(status='POSTED')
        
        url = reverse('contract-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1

    def test_list_contracts_filter(self, api_client):
        from conftest import ContractFactory
        ContractFactory(status='POSTED', location='Nairobi', title='Nairobi Project')
        ContractFactory(status='POSTED', location='Mombasa', title='Mombasa Project')
        
        url = reverse('contract-list')
        
        # Filter by status
        response = api_client.get(url, {'status': 'POSTED'})
        assert response.status_code == status.HTTP_200_OK
        assert all(c['status'] == 'POSTED' for c in response.data['results'])
        
        # Filter by location
        response = api_client.get(url, {'location': 'Nairobi'})
        assert response.status_code == status.HTTP_200_OK
        assert any('Nairobi' in c['location'] for c in response.data['results'])
        
        # Search
        response = api_client.get(url, {'search': 'Mombasa'})
        assert response.status_code == status.HTTP_200_OK
        assert any('Mombasa' in c['title'] for c in response.data['results'])

    def test_create_contract_owner(self, api_client, project_owner):
        api_client.force_authenticate(user=project_owner)
        url = reverse('contract-list')
        category = Category.objects.create(
            name='Electrical Works',
            slug='electrical-works',
            taxonomy_type='SERVICE',
            active=True,
        )
        data = {
            'title': 'Build a shed',
            'description_scope': 'Small wooden shed',
            'location': 'Backyard',
            'budget_min': 500,
            'budget_max': 1000,
            'currency': 'KES',
            'category_uuid': str(category.uuid),
            'bid_deadline': '2026-12-01T10:00:00Z',
            'project_start_date': '2026-12-10',
            'project_end_date': '2027-01-10',
            'payment_terms': '30% advance, 40% midpoint, 30% on completion',
            'eligibility_criteria': 'Registered contractor with similar experience',
        }
        response = api_client.post(url, data, format='multipart')
        assert response.status_code == status.HTTP_201_CREATED
        contract = Contract.objects.get(title='Build a shed')
        assert contract.category == category
        assert contract.currency == 'KES'
        assert contract.bid_deadline is not None

    def test_submit_bid_via_contract(self, api_client, contractor, project_owner):
        from conftest import ContractFactory
        contract = ContractFactory(owner=project_owner, status='POSTED')
        
        cp, _ = ContractorProfile.objects.get_or_create(
            user=contractor,
            defaults={
                'company_name':"Builder Co",
                'service_categories':[],
                'operating_region':"Region"
            }
        )
        
        api_client.force_authenticate(user=contractor)
        url = reverse('contract-bids', args=[contract.id])
        data = {
            'contract': contract.id,
            'proposed_cost': 750,
            'proposed_timeline_days': 10,
            'message': 'Can do'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Bid.objects.filter(contract=contract, contractor=cp).exists()

    def test_get_bids_as_owner(self, api_client, project_owner, contractor):
        from conftest import ContractFactory
        contract = ContractFactory(owner=project_owner, status='POSTED')
        cp, _ = ContractorProfile.objects.get_or_create(user=contractor, defaults={'company_name':"B", 'operating_region':"R", 'service_categories':[]})
        Bid.objects.create(contract=contract, contractor=cp, proposed_cost=1000, proposed_timeline_days=5)
        
        api_client.force_authenticate(user=project_owner)
        url = reverse('contract-bids', args=[contract.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_add_milestone_via_contract(self, api_client, project_owner):
        from conftest import ContractFactory
        contract = ContractFactory(owner=project_owner)
        
        api_client.force_authenticate(user=project_owner)
        url = reverse('contract-milestones', args=[contract.id])
        data = {
            'contract': contract.id,
            'title': 'Foundation',
            'amount': 200,
            'due_date': '2026-12-31'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert contract.milestones.count() == 1

    def test_review_contractor(self, api_client, project_owner, contractor):
        from conftest import ContractFactory
        contract = ContractFactory(owner=project_owner, status='POSTED')
        cp, _ = ContractorProfile.objects.get_or_create(user=contractor, defaults={'company_name':"B", 'operating_region':"R", 'service_categories':[]})
        bid = Bid.objects.create(contract=contract, contractor=cp, proposed_cost=1000, proposed_timeline_days=5, status='AWARDED')
        
        api_client.force_authenticate(user=project_owner)
        url = reverse('contract-review', args=[contract.id])
        data = {
            'contract': contract.id,
            'contractor': cp.id,
            'score': 5,
            'comment': 'Great work'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED, f"Failed: {response.data}"
        from reviews.models import ContractorReview
        assert ContractorReview.objects.filter(contract=contract).exists()
