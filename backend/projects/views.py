from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db.models import Q, Sum
from decimal import Decimal, InvalidOperation

from .models import Project, ProjectRequirement, InvestmentCommitment, ProjectUpdate, ProjectContractLink
from .serializers import (
    ProjectSerializer, ProjectRequirementSerializer,
    InvestmentCommitmentSerializer, ProjectUpdateSerializer
)
from contracts.models import Contract
from rbac.permissions import HasRequiredPermission
from .permissions import IsProjectOwnerOrAdmin
from platform_settings.utils import resolve_request_country_code
from catalog.models import Product
from catalog.serializers import ProductListSerializer


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
        'remove_requirement': 'projects:update_project',
        'pledge_commitment': 'investments:pledge',
        'list_commitments': 'projects:view',
        'link_contract': 'projects:update_project',
        'unlink_contract': 'projects:update_project',
        'post_update': 'projects:update_project',
        'remove_update': 'projects:update_project',
        'suggest_products': 'projects:view',
    }

    def get_permissions(self):
        if self.action in {'list', 'retrieve'}:
            return [permissions.AllowAny()]
        if self.action == 'pledge_commitment':
            return [permissions.IsAuthenticated(), HasRequiredPermission()]
        return [permissions.IsAuthenticated(), HasRequiredPermission(), IsProjectOwnerOrAdmin()]

    def get_queryset(self):
        qs = Project.objects.prefetch_related(
            'requirements',
            'updates',
            'commitments',
            'linked_contracts',
            'linked_contracts__contract',
            'owner',
            'category',
            'country',
            'location',
        ).order_by('-created_at')

        # Owner filter
        owner_param = self.request.query_params.get('owner')
        if owner_param == 'me':
            if not self.request.user.is_authenticated:
                return qs.none()
            qs = qs.filter(owner=self.request.user)

        country_code = resolve_request_country_code(self.request)
        if country_code:
            country_filter = Q(country__iso_code__iexact=country_code)
            if str(country_code).isdigit():
                country_filter |= Q(country_id=country_code)
            qs = qs.filter(country_filter)

        # Text search across title, description, location
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(location_text__icontains=search) |
                Q(formatted_address__icontains=search)
            )

        # Location text filter
        loc = self.request.query_params.get('location')
        if loc:
            qs = qs.filter(location_text__icontains=loc)

        # Status filter
        status_param = self.request.query_params.get('status')
        if status_param:
            qs = qs.filter(status=status_param)

        # Budget filters
        budget_min = self.request.query_params.get('budget_min')
        budget_max = self.request.query_params.get('budget_max')
        if budget_min:
            try:
                qs = qs.filter(estimated_budget__gte=Decimal(budget_min))
            except (ValueError, TypeError, InvalidOperation):
                pass
        if budget_max:
            try:
                qs = qs.filter(estimated_budget__lte=Decimal(budget_max))
            except (ValueError, TypeError, InvalidOperation):
                pass

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

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], url_path='requirements')
    def add_requirement(self, request, pk=None):
        project = self.get_object()
        serializer = ProjectRequirementSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(project=project)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='remove-requirement')
    def remove_requirement(self, request, pk=None):
        project = self.get_object()
        req_id = request.data.get('requirement_id')
        if not req_id:
            return Response({"error": "requirement_id required"}, status=status.HTTP_400_BAD_REQUEST)
        deleted, _ = project.requirements.filter(id=req_id).delete()
        if deleted:
            return Response({"status": "Removed"})
        return Response({"error": "Requirement not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], url_path='commit')
    def pledge_commitment(self, request, pk=None):
        project = self.get_object()
        if not project.funding_required:
            return Response({"error": "Project is not open for funding"}, status=status.HTTP_400_BAD_REQUEST)

        amount = request.data.get('amount_committed')
        try:
            amount = Decimal(str(amount))
            if amount <= 0:
                raise ValueError
        except (ValueError, TypeError, InvalidOperation):
            return Response({"error": "Invalid amount. Must be a positive number."}, status=status.HTTP_400_BAD_REQUEST)

        # Check total committed + new amount against budget
        total_committed = project.commitments.filter(
            status__in=[InvestmentCommitment.Status.PLEDGED, InvestmentCommitment.Status.CONFIRMED]
        ).aggregate(total=Sum('amount_committed'))['total'] or Decimal('0')

        if total_committed + amount > project.estimated_budget:
            return Response({
                "error": "Pledge exceeds project budget",
                "budget": str(project.estimated_budget),
                "already_committed": str(total_committed),
                "remaining": str(project.estimated_budget - total_committed)
            }, status=status.HTTP_400_BAD_REQUEST)

        commitment = InvestmentCommitment.objects.create(
            project=project,
            investor=request.user,
            amount_committed=amount
        )
        return Response(InvestmentCommitmentSerializer(commitment).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path='commitments')
    def list_commitments(self, request, pk=None):
        project = self.get_object()
        serializer = InvestmentCommitmentSerializer(project.commitments.all(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='link-contract')
    def link_contract(self, request, pk=None):
        project = self.get_object()
        contract_id = request.data.get('contract_id')
        contract = get_object_or_404(Contract, id=contract_id)
        link, _ = ProjectContractLink.objects.get_or_create(project=project, contract=contract)
        return Response({"status": "Linked", "link_id": link.id})

    @action(detail=True, methods=['post'], url_path='unlink-contract')
    def unlink_contract(self, request, pk=None):
        project = self.get_object()
        link_id = request.data.get('link_id')
        if not link_id:
            return Response({"error": "link_id required"}, status=status.HTTP_400_BAD_REQUEST)
        deleted, _ = project.linked_contracts.filter(id=link_id).delete()
        if deleted:
            return Response({"status": "Unlinked"})
        return Response({"error": "Link not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], url_path='updates')
    def post_update(self, request, pk=None):
        project = self.get_object()
        serializer = ProjectUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(project=project, posted_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='remove-update')
    def remove_update(self, request, pk=None):
        project = self.get_object()
        update_id = request.data.get('update_id')
        if not update_id:
            return Response({"error": "update_id required"}, status=status.HTTP_400_BAD_REQUEST)
        deleted, _ = project.updates.filter(id=update_id).delete()
        if deleted:
            return Response({"status": "Removed"})
        return Response({"error": "Update not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'], url_path='suggest-products')
    def suggest_products(self, request, pk=None):
        """
        Suggest catalog products that match a project's material requirements.
        Query param: requirement_id (optional) — if omitted, suggests for all MATERIAL requirements.
        """
        project = self.get_object()
        requirement_id = request.query_params.get('requirement_id')

        reqs = project.requirements.filter(type=ProjectRequirement.Type.MATERIAL)
        if requirement_id:
            reqs = reqs.filter(id=requirement_id)

        if not reqs.exists():
            return Response({"matches": []})

        # Build a broad search from all requirement descriptions
        search_terms = []
        for req in reqs:
            desc = (req.description or '').strip()
            if desc:
                search_terms.append(desc)

        if not search_terms:
            return Response({"matches": []})

        # Find products that match any keyword from any requirement
        qs = Product.objects.filter(status=Product.Status.ACTIVE)
        q_objects = Q()
        for term in search_terms:
            for word in term.split():
                if len(word) > 2:
                    q_objects |= Q(name__icontains=word) | Q(description__icontains=word) | Q(category__name__icontains=word)
        if q_objects:
            qs = qs.filter(q_objects)

        # Exclude out-of-stock from suggestions
        qs = qs.exclude(stock_quantity__lte=0)

        # Prefer verified vendors, then featured
        qs = qs.order_by('-vendor__verified_status', '-is_featured', '-created_at')

        # Limit to top 8 suggestions
        qs = qs.select_related('vendor', 'category').prefetch_related('images')[:8]

        serializer = ProductListSerializer(qs, many=True, context={'request': request})
        return Response({
            "matches": serializer.data,
            "requirement_count": reqs.count(),
            "total_available": Product.objects.filter(status=Product.Status.ACTIVE).exclude(stock_quantity__lte=0).count(),
        })
