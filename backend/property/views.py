from datetime import timedelta
import math

from django.db.models import DecimalField, Q, Value
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from chat.models import ChatRoom
from notifications.models import Notification
from notifications.services import notify_user
from projects.models import Project
from rbac.permissions import HasRequiredPermission

from .models import (
    PropertyListing,
    PropertyProjectLink,
    PropertyInquiry,
    PropertyAvailabilityWindow,
    PropertyAppointment,
)
from .serializers import (
    PropertyListingSerializer,
    PropertyInquirySerializer,
    PropertyAvailabilityWindowSerializer,
    PropertyAppointmentSerializer,
)


class IsPropertyOperator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.role == 'ADMIN' or request.user.is_staff or request.user.is_superuser:
            return True
        prop = obj if isinstance(obj, PropertyListing) else getattr(obj, 'property', None)
        if not prop:
            return False
        return prop.owner == request.user or prop.manager == request.user


class IsPropertyOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        prop = obj if isinstance(obj, PropertyListing) else getattr(obj, 'property', None)
        if not prop:
            return False
        return prop.owner == request.user


def create_property_chat_room(prop, participants):
    room = ChatRoom.objects.create(name=f'Property: {prop.title}')
    for participant in participants:
        if participant and participant.is_authenticated:
            room.participants.add(participant)
    return room


def notify_property_operators(prop, subject, message):
    recipients = [prop.owner]
    if prop.manager and prop.manager != prop.owner:
        recipients.append(prop.manager)

    for recipient in recipients:
        if recipient:
            notify_user(recipient, Notification.Type.CHAT, subject, message)


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = PropertyListing.objects.all().order_by('-created_at')
    serializer_class = PropertyListingSerializer
    permission_classes = [HasRequiredPermission]
    required_permission = 'property:view'
    permission_map = {
        'create': 'property:list_property',
        'update': 'property:update_property',
        'partial_update': 'property:update_property',
        'destroy': 'property:update_property',
        'link_project': 'property:update_property',
    }

    def get_permissions(self):
        if self.action in {'list', 'retrieve', 'availability'}:
            return [permissions.AllowAny()]
        if self.action == 'mine':
            return [permissions.IsAuthenticated(), HasRequiredPermission()]
        if self.action == 'create':
            return [permissions.IsAuthenticated(), HasRequiredPermission()]
        if self.action in {'update', 'partial_update', 'destroy', 'link_project'}:
            return [permissions.IsAuthenticated(), HasRequiredPermission(), IsPropertyOwner()]
        return super().get_permissions()

    def get_queryset(self):
        qs = (
            super()
            .get_queryset()
            .select_related(
                'owner',
                'manager',
                'country',
                'location',
                'purpose',
                'development_metadata',
                'specification',
                'ownership_profile',
                'pricing_profile',
            )
            .prefetch_related(
                'linked_projects__project',
                'availability_windows',
                'features',
                'media_assets',
                'showings',
            )
        )
        qs = qs.annotate(
            effective_price=Coalesce(
                'pricing_profile__asking_price',
                'price_estimate',
                Value(0),
                output_field=DecimalField(max_digits=12, decimal_places=2),
            )
        )
        owner_param = self.request.query_params.get('owner')
        managed_param = self.request.query_params.get('managed')
        if owner_param == 'me':
            if not self.request.user.is_authenticated:
                return qs.none()
            qs = qs.filter(owner=self.request.user)
        if managed_param == 'me':
            if not self.request.user.is_authenticated:
                return qs.none()
            qs = qs.filter(Q(manager=self.request.user) | Q(owner=self.request.user))

        search = self.request.query_params.get('search')
        asset_type = self.request.query_params.get('asset_type')
        listing_type = self.request.query_params.get('listing_type')
        purpose = self.request.query_params.get('purpose')
        country = self.request.query_params.get('country')
        city = self.request.query_params.get('city')
        state = self.request.query_params.get('state')
        location_query = self.request.query_params.get('location')
        status_param = self.request.query_params.get('status')
        financing_allowed = self.request.query_params.get('financing_allowed')
        build_ready = self.request.query_params.get('build_ready')
        development_stage = self.request.query_params.get('development_stage')
        pricing_strategy = self.request.query_params.get('pricing_strategy')
        verification_status = self.request.query_params.get('verification_status')
        occupancy_status = self.request.query_params.get('occupancy_status')
        condition_rating = self.request.query_params.get('condition_rating')
        furnishing_state = self.request.query_params.get('furnishing_state')
        min_bedrooms = self.request.query_params.get('min_bedrooms')
        min_bathrooms = self.request.query_params.get('min_bathrooms')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        feature = self.request.query_params.get('feature')
        sort_by = self.request.query_params.get('sort_by')

        if search:
            qs = qs.filter(
                Q(title__icontains=search)
                | Q(description__icontains=search)
                | Q(location_text__icontains=search)
                | Q(formatted_address__icontains=search)
                | Q(features__name__icontains=search)
                | Q(features__description__icontains=search)
                | Q(development_metadata__recommended_use__icontains=search)
                | Q(development_metadata__zoning_info__icontains=search)
            )
        if asset_type:
            qs = qs.filter(asset_type=asset_type)
        if listing_type:
            qs = qs.filter(listing_type=listing_type)
        if purpose:
            if purpose.isdigit():
                qs = qs.filter(purpose_id=purpose)
            else:
                qs = qs.filter(Q(purpose__slug=purpose) | Q(purpose__name__iexact=purpose))
        if country:
            qs = qs.filter(country_id=country)
        if city:
            qs = qs.filter(Q(location__city__icontains=city) | Q(location_text__icontains=city) | Q(formatted_address__icontains=city))
        if state:
            qs = qs.filter(Q(location__state__icontains=state) | Q(formatted_address__icontains=state))
        if location_query:
            qs = qs.filter(
                Q(location_text__icontains=location_query)
                | Q(formatted_address__icontains=location_query)
                | Q(location__name__icontains=location_query)
                | Q(location__city__icontains=location_query)
                | Q(location__state__icontains=location_query)
            )
        if status_param:
            qs = qs.filter(status=status_param)
        if financing_allowed in {'true', 'false'}:
            qs = qs.filter(financing_allowed=(financing_allowed == 'true'))
        if build_ready in {'true', 'false'}:
            qs = qs.filter(development_metadata__build_ready=(build_ready == 'true'))
        if development_stage:
            qs = qs.filter(development_metadata__development_stage=development_stage)
        if pricing_strategy:
            qs = qs.filter(pricing_profile__pricing_strategy=pricing_strategy)
        if verification_status:
            qs = qs.filter(ownership_profile__verification_status=verification_status)
        if occupancy_status:
            qs = qs.filter(specification__occupancy_status=occupancy_status)
        if condition_rating:
            qs = qs.filter(specification__condition_rating=condition_rating)
        if furnishing_state:
            qs = qs.filter(specification__furnishing_state=furnishing_state)
        if feature:
            qs = qs.filter(Q(features__name__icontains=feature) | Q(features__category__icontains=feature))

        numeric_filters = [
            (min_bedrooms, 'specification__bedrooms__gte'),
            (min_bathrooms, 'specification__bathrooms__gte'),
            (min_price, 'effective_price__gte'),
            (max_price, 'effective_price__lte'),
        ]
        for raw_value, lookup in numeric_filters:
            if raw_value in {None, ''}:
                continue
            try:
                qs = qs.filter(**{lookup: raw_value})
            except (TypeError, ValueError):
                pass

        sort_map = {
            'price': 'effective_price',
            '-price': '-effective_price',
            'created_at': 'created_at',
            '-created_at': '-created_at',
            'bedrooms': 'specification__bedrooms',
            '-bedrooms': '-specification__bedrooms',
        }
        if sort_by in sort_map:
            qs = qs.order_by(sort_map[sort_by])

        lat = self.request.query_params.get('latitude')
        lng = self.request.query_params.get('longitude')
        radius = self.request.query_params.get('radius_km')

        if lat and lng:
            try:
                lat_value = float(lat)
                lng_value = float(lng)
                if radius:
                    radius_value = float(radius)
                    lat_delta = radius_value / 111.0
                    lng_divisor = 111.0 * max(math.cos(math.radians(lat_value)), 0.1)
                    lng_delta = radius_value / lng_divisor
                    qs = qs.filter(
                        latitude__isnull=False,
                        longitude__isnull=False,
                        latitude__gte=lat_value - lat_delta,
                        latitude__lte=lat_value + lat_delta,
                        longitude__gte=lng_value - lng_delta,
                        longitude__lte=lng_value + lng_delta,
                    )
            except (ValueError, TypeError):
                pass

        return qs.distinct()

    def perform_create(self, serializer):
        user = self.request.user
        manager = serializer.validated_data.get('manager')
        if manager and not (user.role == 'ADMIN' or user.has_role('PROPERTY_MANAGER') or manager == user):
            raise permissions.PermissionDenied('Only property operators can assign a property manager.')
        serializer.save(owner=user)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def mine(self, request):
        queryset = self.get_queryset().filter(Q(owner=request.user) | Q(manager=request.user)).distinct()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsPropertyOwner], url_path='link-project')
    def link_project(self, request, pk=None):
        prop = self.get_object()
        project_id = request.data.get('project_id')
        project = get_object_or_404(Project, id=project_id)
        link, _ = PropertyProjectLink.objects.get_or_create(property=prop, project=project)
        return Response({"status": "Linked", "link_id": link.id})

    @action(detail=True, methods=['get'], permission_classes=[permissions.AllowAny])
    def availability(self, request, pk=None):
        prop = self.get_object()
        windows = prop.availability_windows.filter(is_active=True).order_by('start_at')
        booked = list(
            prop.appointments.exclude(status=PropertyAppointment.Status.CANCELLED)
            .values_list('scheduled_start', 'scheduled_end')
        )

        slots = []
        for window in windows:
            cursor = window.start_at
            while cursor < window.end_at:
                slot_end = min(cursor + timedelta(minutes=window.slot_duration_minutes), window.end_at)
                overlapping = any(start < slot_end and end > cursor for start, end in booked)
                if not overlapping:
                    slots.append({
                        'window_id': window.id,
                        'start_at': cursor,
                        'end_at': slot_end,
                    })
                cursor = slot_end
        return Response(slots)


class PropertyInquiryViewSet(viewsets.ModelViewSet):
    queryset = PropertyInquiry.objects.all().order_by('-created_at')
    serializer_class = PropertyInquirySerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), HasRequiredPermission(), IsPropertyOperator()]

    required_permission = 'property:view'

    def get_queryset(self):
        user = self.request.user
        property_id = self.request.query_params.get('property')
        if not user.is_authenticated:
            return self.queryset.none()
        if user.role == 'ADMIN' or user.is_staff or user.is_superuser:
            queryset = self.queryset
        else:
            queryset = self.queryset.filter(Q(property__owner=user) | Q(property__manager=user) | Q(inquirer_user=user)).distinct()
        if property_id:
            queryset = queryset.filter(property_id=property_id)
        return queryset

    def perform_create(self, serializer):
        property_id = self.request.data.get('property')
        prop = get_object_or_404(PropertyListing, id=property_id)
        if not prop.inquiry_enabled:
            raise permissions.PermissionDenied('Inquiries are disabled for this property.')

        participants = [prop.owner]
        if prop.manager and prop.manager != prop.owner:
            participants.append(prop.manager)
        if self.request.user.is_authenticated:
            participants.append(self.request.user)
        chat_room = create_property_chat_room(prop, participants)
        serializer.save(
            property=prop,
            inquirer_user=self.request.user if self.request.user.is_authenticated else None,
            chat_room=chat_room,
        )
        notify_property_operators(
            prop,
            'New property inquiry',
            f'A new inquiry was submitted for {prop.title}.',
        )


class PropertyAvailabilityWindowViewSet(viewsets.ModelViewSet):
    queryset = PropertyAvailabilityWindow.objects.all().order_by('start_at')
    serializer_class = PropertyAvailabilityWindowSerializer
    permission_classes = [permissions.IsAuthenticated, HasRequiredPermission, IsPropertyOperator]
    required_permission = 'property:update_property'

    def get_queryset(self):
        user = self.request.user
        property_id = self.request.query_params.get('property')
        if user.role == 'ADMIN' or user.is_staff or user.is_superuser:
            queryset = self.queryset
        else:
            queryset = self.queryset.filter(Q(property__owner=user) | Q(property__manager=user)).distinct()
        if property_id:
            queryset = queryset.filter(property_id=property_id)
        return queryset

    def perform_create(self, serializer):
        property_id = self.request.data.get('property')
        prop = get_object_or_404(PropertyListing, id=property_id)
        if not (prop.owner == self.request.user or prop.manager == self.request.user or self.request.user.role == 'ADMIN'):
            raise permissions.PermissionDenied('Only the property owner or manager can set availability.')
        serializer.save(managed_by=self.request.user, property=prop)


class PropertyAppointmentViewSet(viewsets.ModelViewSet):
    queryset = PropertyAppointment.objects.all().order_by('scheduled_start')
    serializer_class = PropertyAppointmentSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), HasRequiredPermission(), IsPropertyOperator()]

    required_permission = 'property:view'

    def get_queryset(self):
        user = self.request.user
        property_id = self.request.query_params.get('property')
        if not user.is_authenticated:
            return self.queryset.none()
        if user.role == 'ADMIN' or user.is_staff or user.is_superuser:
            queryset = self.queryset
        else:
            queryset = self.queryset.filter(Q(property__owner=user) | Q(property__manager=user) | Q(visitor_user=user)).distinct()
        if property_id:
            queryset = queryset.filter(property_id=property_id)
        return queryset

    def perform_create(self, serializer):
        property_id = self.request.data.get('property')
        prop = get_object_or_404(PropertyListing, id=property_id)
        if not prop.appointment_enabled:
            raise permissions.PermissionDenied('Appointments are disabled for this property.')

        availability_window = None
        if self.request.data.get('availability_window'):
            availability_window = get_object_or_404(PropertyAvailabilityWindow, id=self.request.data.get('availability_window'), property=prop)

        participants = [prop.owner]
        if prop.manager and prop.manager != prop.owner:
            participants.append(prop.manager)
        if self.request.user.is_authenticated:
            participants.append(self.request.user)
        chat_room = create_property_chat_room(prop, participants)

        serializer.save(
            property=prop,
            availability_window=availability_window,
            visitor_user=self.request.user if self.request.user.is_authenticated else None,
            created_by=self.request.user if self.request.user.is_authenticated else None,
            chat_room=chat_room,
        )
        notify_property_operators(
            prop,
            'New property appointment',
            f'A viewing request was scheduled for {prop.title}.',
        )
