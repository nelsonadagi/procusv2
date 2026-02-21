from rest_framework import viewsets, status, permissions
from accounts.permissions import IsProjectOwnerOrReadOnly, IsContractor
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Contract
from .serializers import ContractSerializer
from bids.models import Bid
from bids.serializers import BidSerializer
from milestones.models import Milestone
from milestones.serializers import MilestoneSerializer
from reviews.models import ContractorReview
from reviews.serializers import ContractorReviewSerializer
from contractors.models import ContractorProfile

from rbac.permissions import HasRequiredPermission
from rbac.utils import log_action

class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all().order_by('-created_at')
    serializer_class = ContractSerializer
    permission_classes = [HasRequiredPermission]
    required_permission = 'contracts:view'
    permission_map = {
        'create': 'contracts:post_contract',
        'update': 'contracts:post_contract',
        'partial_update': 'contracts:post_contract',
        'destroy': 'contracts:post_contract',
        'bids': 'bids:view', # Post bid handled inside
        'milestones': 'contracts:manage_milestones',
    }

    def perform_create(self, serializer):
        contract = serializer.save(owner=self.request.user)
        log_action(self.request.user, 'POST_CONTRACT', 'contract', contract.id)

    def get_queryset(self):
        try:
            qs = super().get_queryset()
            
            # If user is not admin and didn't specify a status, default to POSTED (Public Tenders)
            # This ensures regular users don't see 'PENDING' moderation queue contracts.
            status_param = self.request.query_params.get('status')
            user = self.request.user
            
            # Check if user is authenticated and has admin privileges
            is_admin = user.is_authenticated and (user.is_staff or user.role == 'ADMIN')
            
            if not is_admin and not status_param:
                # Regular users see POSTED contracts OR their own contracts (regardless of status)
                if user.is_authenticated:
                    from django.db.models import Q
                    qs = qs.filter(Q(status='POSTED') | Q(owner=user))
                else:
                    qs = qs.filter(status='POSTED')
            elif status_param:
                qs = qs.filter(status=status_param)
                
            location = self.request.query_params.get('location')
            if location:
                qs = qs.filter(location__icontains=location)
                
            search = self.request.query_params.get('search')
            if search:
                from django.db.models import Q
                qs = qs.filter(Q(title__icontains=search) | Q(description_scope__icontains=search))
                
            return qs
        except Exception as e:
            import traceback
            print("ERROR IN GET_QUERYSET:")
            traceback.print_exc()
            raise e

    @action(detail=True, methods=['post', 'get'], url_path='bids')
    def bids(self, request, pk=None):
        contract = self.get_object()
        
        if request.method == 'POST':
            # Check if user is contractor
            if not hasattr(request.user, 'contractor_profile'):
                 return Response({"error": "Only contractors can bid"}, status=status.HTTP_403_FORBIDDEN)
            
            serializer = BidSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(contract=contract, contractor=request.user.contractor_profile)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        else: # GET
            # Only owner or specific contractor? Spec says "Owner views submitted bids". 
            # In a public marketplace, maybe bids are visible? Or sealed? 
            # Assuming sealed, only Owner sees all. Contractor sees theirs.
            if contract.owner == request.user:
                bids = contract.bids.all()
            elif hasattr(request.user, 'contractor_profile'):
                bids = contract.bids.filter(contractor=request.user.contractor_profile)
            else:
                 return Response({"error": "Not authorized to view bids"}, status=status.HTTP_403_FORBIDDEN)
            
            serializer = BidSerializer(bids, many=True)
            return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='milestones')
    def milestones(self, request, pk=None):
        contract = self.get_object()
        if contract.owner != request.user:
            return Response({"error": "Only owner can define milestones"}, status=status.HTTP_403_FORBIDDEN)
            
        serializer = MilestoneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(contract=contract)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='review')
    def review(self, request, pk=None):
        contract = self.get_object()
        if contract.owner != request.user:
             return Response({"error": "Only owner can review"}, status=status.HTTP_403_FORBIDDEN)
        
        # Need to identify contractor to review. 
        # Usually review is post-completion, and we review the awarded contractor.
        # Check if contract is awarded/completed
        try:
             awarded_bid = contract.bids.get(status='AWARDED')
             contractor = awarded_bid.contractor
        except Bid.DoesNotExist:
             return Response({"error": "No awarded contractor to review"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ContractorReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(contract=contract, owner=request.user, contractor=contractor)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
