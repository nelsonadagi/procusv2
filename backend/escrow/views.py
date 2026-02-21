from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import EscrowAccount, EscrowTransaction, EscrowRelease
from .serializers import EscrowAccountSerializer, EscrowReleaseSerializer
from contracts.models import Contract
from milestones.models import Milestone

class EscrowViewSet(viewsets.ModelViewSet):
    # This viewset might handle funding and checking status
    queryset = EscrowAccount.objects.all()
    serializer_class = EscrowAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Only owner should see their escrow? For MVP admin sees all.
    # In URL structure /contracts/{id}/escrow, so maybe we need a dedicated view method.
    
    @action(detail=False, methods=['post'], url_path='deposit')
    def deposit(self, request):
        # We expect contract_id in body or create a separate router/path
        contract_id = request.data.get('contract_id')
        amount = request.data.get('amount') # In real flow, this follows successful payment gateway webhook
        
        contract = get_object_or_404(Contract, id=contract_id)
        if contract.owner != request.user:
             return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        
        escrow, created = EscrowAccount.objects.get_or_create(
            contract=contract,
            defaults={'buyer': request.user, 'total_amount_held': 0}
        )
        
        # Simulate payment success & deposit
        escrow.total_amount_held += int(amount) # Cast for simplification
        escrow.save()
        
        EscrowTransaction.objects.create(
            escrow_account=escrow,
            type=EscrowTransaction.Type.DEPOSIT,
            amount=amount,
            payment_reference="DEP-" + str(escrow.id)
        )
        
        return Response({"status": "Deposited", "balance": escrow.total_amount_held})

class EscrowReleaseViewSet(viewsets.ModelViewSet):
    queryset = EscrowRelease.objects.all()
    serializer_class = EscrowReleaseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['post'], url_path='trigger')
    def trigger(self, request):
        # Called when milestone approved
        milestone_id = request.data.get('milestone_id')
        milestone = get_object_or_404(Milestone, id=milestone_id)
        
        # Security check: owner or admin? 
        # Usually internal call or Owner approves via /milestones/approve which calls this
        
        # Check if escrow exists
        if not hasattr(milestone.contract, 'escrow_account'):
             return Response({"error": "No escrow account found"}, status=status.HTTP_400_BAD_REQUEST)
             
        escrow = milestone.contract.escrow_account
        
        if escrow.holds.exclude(status='LIFTED').exists():
             return Response({"error": "Escrow is frozen due to dispute"}, status=status.HTTP_400_BAD_REQUEST)

        if escrow.total_amount_held < milestone.amount:
              return Response({"error": "Insufficient escrow funds"}, status=status.HTTP_400_BAD_REQUEST)
              
        # Execute Release
        escrow.total_amount_held -= milestone.amount
        escrow.save()
        
        EscrowTransaction.objects.create(
            escrow_account=escrow,
            type=EscrowTransaction.Type.RELEASE,
            amount=milestone.amount,
            milestone=milestone,
            payment_reference="REL-" + str(milestone.id)
        )
        
        # Create Release Record
        release = EscrowRelease.objects.create(
            milestone=milestone,
            approved_by=request.user,
            released_amount=milestone.amount,
            release_status=EscrowRelease.Status.COMPLETED
        )
        
        milestone.status = Milestone.Status.PAID
        milestone.save()
        
        return Response({"status": "Released", "balance": escrow.total_amount_held})
