from rest_framework import viewsets, status, permissions, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Bid
from .serializers import BidSerializer
from contracts.models import Contract
from rbac.permissions import HasRequiredPermission
from notifications.models import Notification
from notifications.services import notify_user

class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticated, HasRequiredPermission]
    required_permission = 'bids:view'
    permission_map = {
        'create': 'bids:submit_bid',
        'update': 'bids:submit_bid',
        'partial_update': 'bids:submit_bid',
        'destroy': 'bids:withdraw_bid',
        'shortlist': 'bids:view',
        # Awarding a bid is part of the contract lifecycle, so reuse the contract-award permission.
        'award': 'contracts:award_contract',
    }

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'contractor_profile'):
            return Bid.objects.filter(contractor__user=user)
        # Project Owner sees bids on their contracts
        return Bid.objects.filter(contract__owner=user)

    def perform_create(self, serializer):
        user = self.request.user
        if hasattr(user, 'contractor_profile'):
            serializer.save(contractor=user.contractor_profile)
        else:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Only users with a contractor profile can submit bids.")

    @action(detail=True, methods=['post'], url_path='shortlist')
    def shortlist(self, request, pk=None):
        bid = self.get_object()
        if bid.contract.owner != request.user:
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
            
        bid.status = Bid.Status.SHORTLISTED
        bid.save()
        return Response({"status": "Bid shortlisted"})

    @action(detail=True, methods=['post'], url_path='award')
    def award(self, request, pk=None):
        bid = self.get_object()
        if bid.contract.owner != request.user:
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        contract = bid.contract

        # Auto-reject all other bids on this contract
        rejected_bids = list(contract.bids.exclude(pk=bid.pk).select_related('contractor__user'))
        contract.bids.exclude(pk=bid.pk).update(status=Bid.Status.REJECTED)

        bid.status = Bid.Status.AWARDED
        bid.save()

        contract.status = contract.Status.AWARDED
        contract.save()

        notify_user(
            bid.contractor.user,
            Notification.Type.BID,
            "Bid awarded",
            f"Your bid for {contract.title} was awarded.",
            data={"contract_id": contract.id, "bid_id": bid.id},
        )
        for rejected_bid in rejected_bids:
            notify_user(
                rejected_bid.contractor.user,
                Notification.Type.BID,
                "Bid not selected",
                f"Your bid for {contract.title} was not selected.",
                data={"contract_id": contract.id, "bid_id": rejected_bid.id},
            )

        return Response({"status": "Bid awarded", "contract_status": contract.status})
