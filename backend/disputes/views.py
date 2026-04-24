from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Dispute, EvidenceSubmission
from .serializers import DisputeSerializer, EvidenceSubmissionSerializer
from escrow.models import EscrowHold, EscrowAccount, EscrowTransaction
from rbac.permissions import HasRequiredPermission

class DisputeViewSet(viewsets.ModelViewSet):
    queryset = Dispute.objects.all()
    serializer_class = DisputeSerializer
    permission_classes = [permissions.IsAuthenticated, HasRequiredPermission]
    required_permission = 'disputes:view'
    permission_map = {
        'create': 'disputes:raise_dispute',
        'update': 'disputes:raise_dispute',
        'partial_update': 'disputes:raise_dispute',
        'submit_evidence': 'disputes:raise_dispute',
        'resolve': 'disputes:arbitrate_dispute',
        'destroy': 'disputes:close_dispute',
    }

    def _is_admin(self):
        user = self.request.user
        return user.is_staff or user.is_superuser or getattr(user, 'role', '') == 'ADMIN'

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created_at')
        if self._is_admin():
            return queryset
        return queryset.filter(opened_by=self.request.user)

    def perform_create(self, serializer):
        dispute = serializer.save(opened_by=self.request.user)
        # Freeze Escrow If exists
        if dispute.contract and hasattr(dispute.contract, 'escrow_account'):
            escrow = dispute.contract.escrow_account
            EscrowHold.objects.create(
                escrow_account=escrow,
                dispute=dispute,
                reason="Dispute Opened",
                status='ACTIVE'
            )

    @action(detail=True, methods=['post'], url_path='evidence')
    def submit_evidence(self, request, pk=None):
        dispute = self.get_object()
        serializer = EvidenceSubmissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(dispute=dispute, submitted_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='resolve')
    def resolve(self, request, pk=None):
        # Admin only
        if not self._is_admin():
             return Response({"error": "Admin only"}, status=status.HTTP_403_FORBIDDEN)
             
        dispute = self.get_object()
        outcome = request.data.get('outcome') # RELEASE or REFUND
        
        if not dispute.contract or not hasattr(dispute.contract, 'escrow_account'):
             # Just close dispute if no escrow
             dispute.status = 'CLOSED'
             dispute.save()
             return Response({"status": "Closed (No Escrow)"})

        escrow = dispute.contract.escrow_account
        
        # Lift Hold
        escrow.holds.filter(dispute=dispute, status='ACTIVE').update(status='LIFTED')
        
        if outcome == 'RELEASE':
            # Release total held? Or specific amount? 
            # Simplified: Release all to Vendor/Contractor? 
            # Or just unfreeze? 
            # Spec says "Resolve -> Release Funds". Let's assume release all held.
            amount = escrow.total_amount_held
            escrow.total_amount_held = 0
            escrow.status = 'RELEASED'
            escrow.save()
            
            EscrowTransaction.objects.create(
                escrow_account=escrow,
                type=EscrowTransaction.Type.RELEASE,
                amount=amount,
                payment_reference="DISPUTE-RES-REL"
            )
            dispute.status = 'RESOLVED_RELEASE'
            
        elif outcome == 'REFUND':
             amount = escrow.total_amount_held
             escrow.total_amount_held = 0
             escrow.status = 'CLOSED' # Refunded implies returned to buyer
             escrow.save()
             
             EscrowTransaction.objects.create(
                escrow_account=escrow,
                type=EscrowTransaction.Type.REFUND,
                amount=amount,
                payment_reference="DISPUTE-RES-REF"
             )
             dispute.status = 'RESOLVED_REFUND'

        dispute.save()
        return Response({"status": f"Resolved: {outcome}"})
