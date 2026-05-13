from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Milestone


class MilestoneViewSet(viewsets.GenericViewSet):
    queryset = Milestone.objects.all()

    def _get_awarded_contractor_user(self, contract):
        """Return the user of the contractor whose bid was awarded on this contract."""
        awarded_bid = contract.bids.filter(status='AWARDED').select_related('contractor__user').first()
        return awarded_bid.contractor.user if awarded_bid else None

    def _check_all_milestones_approved(self, contract):
        """Return True if contract has milestones and all are APPROVED."""
        milestones = contract.milestones.all()
        return milestones.exists() and all(m.status == Milestone.Status.APPROVED for m in milestones)

    @action(detail=True, methods=['post'], url_path='complete')
    def complete(self, request, pk=None):
        """Contractor marks a milestone as completed. Moves contract to IN_PROGRESS if first completion."""
        milestone = self.get_object()
        contract = milestone.contract

        awarded_contractor_user = self._get_awarded_contractor_user(contract)
        if awarded_contractor_user != request.user:
            return Response({"error": "Only the awarded contractor can mark milestones complete."}, status=status.HTTP_403_FORBIDDEN)

        if milestone.status != Milestone.Status.PENDING:
            return Response({"error": f"Milestone is already {milestone.status}."}, status=status.HTTP_400_BAD_REQUEST)

        milestone.status = Milestone.Status.COMPLETED
        milestone.save()

        # Auto-progress contract: AWARDED → IN_PROGRESS on first milestone completion
        if contract.status == contract.Status.AWARDED:
            contract.status = contract.Status.IN_PROGRESS
            contract.save()

        return Response({"status": "Milestone marked complete", "contract_status": contract.status})

    @action(detail=True, methods=['post'], url_path='approve')
    def approve(self, request, pk=None):
        """Owner approves a completed milestone. Moves contract to COMPLETED if all milestones approved."""
        milestone = self.get_object()
        contract = milestone.contract

        if contract.owner != request.user:
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        if milestone.status != Milestone.Status.COMPLETED:
            return Response({"error": "Milestone must be marked complete by the contractor before approval."}, status=status.HTTP_400_BAD_REQUEST)

        milestone.status = Milestone.Status.APPROVED
        milestone.save()

        # Auto-progress contract: IN_PROGRESS → COMPLETED when all milestones are approved
        if self._check_all_milestones_approved(contract):
            contract.status = contract.Status.COMPLETED
            contract.save()

        # Trigger Payout Placeholder
        return Response({
            "status": "Milestone approved",
            "payment_status": "PENDING_RELEASE",
            "contract_status": contract.status
        })
