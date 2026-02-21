import pytest
from rest_framework import status
from django.urls import reverse
from escrow.models import EscrowAccount, EscrowTransaction, EscrowHold, EscrowRelease
from disputes.models import Dispute

@pytest.mark.django_db
class TestEscrowLifecycle:
    def test_milestone_release_success(self, api_client, project_owner, contractor):
        # 1. Setup funded escrow
        from conftest import EscrowAccountFactory, MilestoneFactory, ContractFactory
        
        contract = ContractFactory(owner=project_owner)
        escrow = EscrowAccountFactory(contract=contract, total_amount_held=2000)
        milestone = MilestoneFactory(contract=contract, amount=500)
        
        # 2. Authenticate as owner
        api_client.force_authenticate(user=project_owner)
        
        # 3. Call release trigger
        url = reverse('escrow-release-trigger')
        response = api_client.post(url, {'milestone_id': milestone.id})
        
        # 4. Asserts
        assert response.status_code == status.HTTP_200_OK
        assert response.data['balance'] == 1500 # 2000 - 500
        
        # Check database side effects
        escrow.refresh_from_db()
        assert escrow.total_amount_held == 1500
        assert EscrowTransaction.objects.filter(type='RELEASE', milestone=milestone).exists()
        assert EscrowRelease.objects.filter(milestone=milestone).exists()
        
        milestone.refresh_from_db()
        assert milestone.status == 'PAID'

    def test_milestone_release_frozen_during_dispute(self, api_client, project_owner, contractor):
        # 1. Setup funded escrow
        from conftest import EscrowAccountFactory, MilestoneFactory, ContractFactory
        contract = ContractFactory(owner=project_owner)
        escrow = EscrowAccountFactory(contract=contract, total_amount_held=2000)
        milestone = MilestoneFactory(contract=contract, amount=500)
        
        # 2. Create Active Dispute & Hold
        dispute = Dispute.objects.create(
            opened_by=project_owner,
            contract=contract,
            reason="Work not as described"
        )
        EscrowHold.objects.create(
             escrow_account=escrow,
             dispute=dispute,
             reason="Dispute in progress"
        )
        
        # 3. Attempt release
        api_client.force_authenticate(user=project_owner)
        url = reverse('escrow-release-trigger')
        response = api_client.post(url, {'milestone_id': milestone.id})
        
        # 4. Asserts
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "frozen" in response.data['error']
        
        escrow.refresh_from_db()
        assert escrow.total_amount_held == 2000 # Unchanged
