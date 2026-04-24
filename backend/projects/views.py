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
from rbac.permissions import HasRequiredPermission

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer
    permission_classes = [HasRequiredPermission]
    required_permission = 'projects:view'
    permission_map = {
        'create': 'projects:create_project',
        'update': 'projects:update_project',
        'partial_update': 'projects:update_project',
        'destroy': 'projects:delete_project',
        'add_requirement': 'projects:update_project',
        'pledge_commitment': 'investments:pledge',
        'list_commitments': 'projects:view',
        'link_contract': 'projects:update_project',
        'post_update': 'projects:update_project',
    }

    def get_permissions(self):
        if self.action in {'list', 'retrieve'}:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), HasRequiredPermission()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
         qs = super().get_queryset()
         owner_param = self.request.query_params.get('owner')
         if owner_param == 'me':
             if not self.request.user.is_authenticated:
                 return qs.none()
             qs = qs.filter(owner=self.request.user)
         loc = self.request.query_params.get('location')
         status_param = self.request.query_params.get('status')
         if loc: qs = qs.filter(location_text__icontains=loc)
         if status_param: qs = qs.filter(status=status_param)

         # Proximity Search
         lat = self.request.query_params.get('latitude')
         lng = self.request.query_params.get('longitude')
         radius = self.request.query_params.get('radius_km')

         if lat and lng:
             from django.contrib.gis.db.models.functions import Distance
             from django.contrib.gis.geos import Point
             from django.contrib.gis.measure import D
             try:
                 user_location = Point(float(lng), float(lat), srid=4326)
                 if radius:
                     qs = qs.filter(location__point__distance_lte=(user_location, D(km=float(radius))))

                 qs = qs.annotate(distance=Distance('location__point', user_location)).order_by('distance')
             except (ValueError, TypeError):
                 pass

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
