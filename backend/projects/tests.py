import pytest
from django.urls import reverse
from rest_framework import status
from projects.models import Project, InvestmentCommitment

@pytest.mark.django_db
class TestProjectsAPI:
    def test_create_project(self, api_client, project_owner):
        api_client.force_authenticate(user=project_owner)
        url = reverse('project-list')
        data = {
            'title': 'New Residential Complex',
            'description': 'Building 50 floors',
            'location': 'Westlands',
            'estimated_budget': 5000000,
            'funding_required': True
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Project.objects.filter(title='New Residential Complex').exists()

    def test_add_requirement(self, api_client, project_owner):
        api_client.force_authenticate(user=project_owner)
        project = Project.objects.create(
            owner=project_owner,
            title="Test Project",
            description="Desc",
            location="Loc",
            estimated_budget=1000
        )
        url = reverse('project-add-requirement', args=[project.id])
        data = {
            'type': 'MATERIAL',
            'description': 'Cement',
            'quantity': '100 bags'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert project.requirements.count() == 1

    def test_pledge_commitment(self, api_client, investor, project_owner):
        project = Project.objects.create(
            owner=project_owner,
            title="Fundable Project",
            description="Desc",
            location="Loc",
            estimated_budget=10000,
            funding_required=True
        )
        api_client.force_authenticate(user=investor)
        url = reverse('project-pledge-commitment', args=[project.id])
        data = {'amount_committed': 500}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert InvestmentCommitment.objects.filter(project=project, investor=investor).exists()

    def test_list_commitments(self, api_client, project_owner, investor):
        project = Project.objects.create(owner=project_owner, title="P1", estimated_budget=100)
        InvestmentCommitment.objects.create(project=project, investor=investor, amount_committed=50)
        
        api_client.force_authenticate(user=project_owner)
        url = reverse('project-list-commitments', args=[project.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_link_contract(self, api_client, project_owner):
        project = Project.objects.create(owner=project_owner, title="P1", estimated_budget=100)
        from contracts.models import Contract
        contract = Contract.objects.create(
            owner=project_owner, 
            title="C1", 
            budget_min=50, 
            budget_max=100,
            location="Nairobi"
        )
        
        api_client.force_authenticate(user=project_owner)
        url = reverse('project-link-contract', args=[project.id])
        data = {'contract_id': contract.id}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert project.linked_contracts.count() == 1

    def test_post_update(self, api_client, project_owner):
        project = Project.objects.create(owner=project_owner, title="P1", estimated_budget=100)
        
        api_client.force_authenticate(user=project_owner)
        url = reverse('project-post-update', args=[project.id])
        data = {
            'update_text': 'Laying foundation'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert project.updates.count() == 1
