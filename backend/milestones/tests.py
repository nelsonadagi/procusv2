import pytest
from django.urls import reverse
from rest_framework import status
from milestones.models import Milestone
from conftest import ContractFactory, MilestoneFactory

@pytest.mark.django_db
class TestMilestonesAPI:
    def test_approve_milestone(self, api_client, project_owner):
        contract = ContractFactory(owner=project_owner)
        milestone = MilestoneFactory(contract=contract, status=Milestone.Status.PENDING)
        
        api_client.force_authenticate(user=project_owner)
        url = reverse('milestone-approve', args=[milestone.id])
        response = api_client.post(url)
        
        assert response.status_code == status.HTTP_200_OK
        milestone.refresh_from_db()
        assert milestone.status == Milestone.Status.APPROVED

    def test_approve_milestone_unauthorized(self, api_client, investor, project_owner):
        contract = ContractFactory(owner=project_owner)
        milestone = MilestoneFactory(contract=contract, status=Milestone.Status.PENDING)
        
        # This will 404 because the default queryset is everything, but let's see.
        # Wait, GenericViewSet with queryset = Milestone.objects.all()
        # So it WON'T 404, it will hit the owner check.
        api_client.force_authenticate(user=investor)
        url = reverse('milestone-approve', args=[milestone.id])
        response = api_client.post(url)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
