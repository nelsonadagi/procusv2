from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Milestone

class MilestoneViewSet(viewsets.GenericViewSet):
    queryset = Milestone.objects.all()

    @action(detail=True, methods=['post'], url_path='approve')
    def approve(self, request, pk=None):
        milestone = self.get_object()
        if milestone.contract.owner != request.user:
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
            
        milestone.status = Milestone.Status.APPROVED
        milestone.save()
        
        # Trigger Payout Placeholder?
        # In real world, this would call Payment Gateway
        
        return Response({"status": "Milestone approved", "payment_status": "PENDING_RELEASE"})
