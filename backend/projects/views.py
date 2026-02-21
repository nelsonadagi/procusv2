from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Project, ProjectRequirement, InvestmentCommitment, ProjectUpdate, ProjectContractLink
from .serializers import (
    ProjectSerializer, ProjectRequirementSerializer, 
    InvestmentCommitmentSerializer, ProjectUpdateSerializer
)
from contracts.models import Contract

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    def get_queryset(self):
         qs = super().get_queryset()
         loc = self.request.query_params.get('location')
         status_param = self.request.query_params.get('status')
         if loc: qs = qs.filter(location__icontains=loc)
         if status_param: qs = qs.filter(status=status_param)
         return qs

    @action(detail=True, methods=['post'], url_path='requirements')
    def add_requirement(self, request, pk=None):
        project = self.get_object()
        if project.owner != request.user:
             return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ProjectRequirementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='commit')
    def pledge_commitment(self, request, pk=None):
        project = self.get_object()
        # Investors can be any user for this MVP or check role
        amount = request.data.get('amount_committed')
        if not amount:
             return Response({"error": "Amount required"}, status=status.HTTP_400_BAD_REQUEST)
        
        commitment = InvestmentCommitment.objects.create(
            project=project,
            investor=request.user,
            amount_committed=amount
        )
        return Response(InvestmentCommitmentSerializer(commitment).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path='commitments')
    def list_commitments(self, request, pk=None):
        project = self.get_object()
        if project.owner != request.user:
             return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = InvestmentCommitmentSerializer(project.commitments.all(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='link-contract')
    def link_contract(self, request, pk=None):
        project = self.get_object()
        if project.owner != request.user:
             return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
             
        contract_id = request.data.get('contract_id')
        contract = get_object_or_404(Contract, id=contract_id)
        
        link, _ = ProjectContractLink.objects.get_or_create(project=project, contract=contract)
        return Response({"status": "Linked", "link_id": link.id})

    @action(detail=True, methods=['post'], url_path='updates')
    def post_update(self, request, pk=None):
        project = self.get_object()
        if project.owner != request.user:
             return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
             
        serializer = ProjectUpdateSerializer(data=request.data)
        if serializer.is_valid():
             serializer.save(project=project, posted_by=request.user)
             return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
