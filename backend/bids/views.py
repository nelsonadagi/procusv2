from rest_framework import viewsets, status, permissions, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Bid
from .serializers import BidSerializer
from contracts.models import Contract

class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticated]

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
            # Fallback or error if not contractor
            pass

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
            
        # Reject others? 
        # Update Contract status
        bid.status = Bid.Status.AWARDED
        bid.save()
        
        contract = bid.contract
        contract.status = 'AWARDED' # Or Contract.Status.AWARDED
        contract.save()
        
        return Response({"status": "Bid awarded", "contract_status": "AWARDED"})
