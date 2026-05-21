from datetime import timedelta
import math

from django.db.models import Count
from django.db.models import DecimalField, Q, Value
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
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
    PropertyMediaAsset,
    PropertyEvent,
    PropertyInterest,
    SavedPropertySearch,
)
from .serializers import (
    PropertyListingSerializer,
    PropertyInquirySerializer,
    PropertyAvailabilityWindowSerializer,
    PropertyAppointmentSerializer,
    PropertyMediaAssetSerializer,
    PropertyEventSerializer,
    PropertyInterestSerializer,
    SavedPropertySearchSerializer,
)
from .services import dispatch_saved_search_alerts_for_property
from platform_settings.utils import resolve_request_country_code


class IsPropertyOperator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.role == 'ADMIN' or request.user.is_staff or request.user.is_superuser:
            return True
        prop = obj if isinstance(obj, PropertyListing) else getattr(obj, 'property', None)
        if not prop:
            return False
        # Direct ownership or management
        if prop.owner == request.user or prop.manager == request.user:
            return True
        # Organization-scoped access: same org as owner
        if (
            prop.owner
            and prop.owner.organization
            and request.user.organization
            and prop.owner.organization == request.user.organization
        ):
            return True
        return False


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


def notify_property_operators(prop, subject, message, action='open_property', extra_data=None):
    recipients = [prop.owner]
    if prop.manager and prop.manager != prop.owner:
        recipients.append(prop.manager)

    payload = {
        'property_id': prop.id,
        'property_title': prop.title,
        'property_url': f'/properties/{prop.id}',
        'action': action,
    }
    if extra_data:
        payload.update(extra_data)

    for recipient in recipients:
        if recipient:
            notify_user(recipient, Notification.Type.SYSTEM, subject, message, data=payload)


def property_readiness_score(prop):
    score = 0
    if prop.title:
        score += 20
    if prop.location_text or prop.formatted_address or prop.location_id:
        score += 15
    if prop.price_estimate or getattr(getattr(prop, 'pricing_profile', None), 'asking_price', None):
        score += 15
    if prop.description:
        score += 10
    if prop.media_assets.exists():
        score += 15
    if prop.inquiry_enabled:
        score += 5
    if prop.appointment_enabled:
        score += 5
    if getattr(getattr(prop, 'pricing_profile', None), 'pricing_strategy', ''):
        score += 5
    if getattr(getattr(prop, 'development_metadata', None), 'development_stage', ''):
        score += 5
    if getattr(getattr(prop, 'ownership_profile', None), 'legal_owner_name', ''):
        score += 5
    return min(score, 100)


def record_property_event(prop, event_type, title, message='', actor=None, data=None):
    return PropertyEvent.objects.create(
        property=prop,
        actor=actor if actor and actor.is_authenticated else None,
        event_type=event_type,
        title=title,
        message=message,
        data=data or {},
    )


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = PropertyListing.objects.all().order_by('-created_at')
    serializer_class = PropertyListingSerializer
    permission_classes = [HasRequiredPermission]
    required_permission = 'property:view'
    permission_map = {
        'create': 'property:list_property',
        'update': 'property:update_property',
        'partial_update': 'property:update_property',
        'destroy': 'property:delete_property',
        'link_project': 'property:update_property',
        'upload_media': 'property:update_property',
        'moderate': 'property:update_property',
    }

    def get_permissions(self):
        if self.action in {'list', 'retrieve', 'availability'}:
            return [permissions.AllowAny()]
        if self.action in {'similar', 'notify_me', 'saved_searches'}:
            return [permissions.AllowAny()]
        if self.action == 'mine':
            return [permissions.IsAuthenticated(), HasRequiredPermission()]
        if self.action == 'create':
            return [permissions.IsAuthenticated(), HasRequiredPermission()]
        if self.action in {'update', 'partial_update', 'destroy', 'link_project'}:
            return [permissions.IsAuthenticated(), HasRequiredPermission(), IsPropertyOwner()]
        if self.action == 'upload_media':
            return [permissions.IsAuthenticated(), HasRequiredPermission(), IsPropertyOperator()]
        if self.action in {'analytics', 'manager_recommendations'}:
            return [permissions.IsAuthenticated(), HasRequiredPermission()]
        if self.action == 'moderate':
            return [permissions.IsAdminUser()]
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
        country = resolve_request_country_code(self.request)
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
            country_filter = Q(country__iso_code__iexact=country)
            if str(country).isdigit():
                country_filter |= Q(country_id=country)
            qs = qs.filter(country_filter)
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

    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser], url_path='upload-media')
    def upload_media(self, request, pk=None):
        prop = self.get_object()
        files = request.FILES.getlist('files')
        if not files:
            return Response({'error': 'No files provided'}, status=status.HTTP_400_BAD_REQUEST)

        requested_type = request.data.get('media_type', PropertyMediaAsset.MediaType.IMAGE)
        if requested_type not in PropertyMediaAsset.MediaType.values:
            return Response({'error': f'Unsupported media type: {requested_type}'}, status=status.HTTP_400_BAD_REQUEST)

        existing_primary = prop.media_assets.filter(is_primary=True).exists()
        created_assets = []
        for idx, upload in enumerate(files):
            created_assets.append(
                PropertyMediaAsset.objects.create(
                    property=prop,
                    media_type=request.data.get(f'media_type_{idx}', requested_type) or requested_type,
                    document_category=request.data.get(f'document_category_{idx}', request.data.get('document_category', '')),
                    file=upload,
                    title=request.data.get(f'title_{idx}', '') or upload.name,
                    caption=request.data.get(f'caption_{idx}', ''),
                    alt_text=request.data.get(f'alt_text_{idx}', upload.name),
                    sort_order=prop.media_assets.count() + idx,
                    is_primary=(
                        requested_type == PropertyMediaAsset.MediaType.IMAGE
                        and idx == 0
                        and not existing_primary
                    ),
                    is_public=str(request.data.get(f'is_public_{idx}', request.data.get('is_public', 'true'))).lower() not in {'false', '0', 'no'},
                )
            )

        serializer = PropertyMediaAssetSerializer(created_assets, many=True, context={'request': request})
        record_property_event(
            prop,
            PropertyEvent.EventType.PUBLISHED,
            'Property media updated',
            f'{len(created_assets)} media file(s) were added.',
            actor=request.user,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        user = self.request.user
        manager = serializer.validated_data.get('manager')
        if manager and not (user.role == 'ADMIN' or user.has_role('PROPERTY_MANAGER') or manager == user):
            raise permissions.PermissionDenied('Only property operators can assign a property manager.')
        prop = serializer.save(owner=user)
        record_property_event(
            prop,
            PropertyEvent.EventType.PROPERTY_CREATED,
            'Property created',
            f'{prop.title} was created.',
            actor=user,
        )
        dispatch_saved_search_alerts_for_property(prop)

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
        record_property_event(
            prop,
            PropertyEvent.EventType.PROJECT_LINKED,
            'Property linked to project',
            f'{prop.title} was linked to {project.title}.',
            actor=request.user,
            data={'project_id': project.id},
        )
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

    @action(detail=True, methods=['get'], permission_classes=[permissions.AllowAny])
    def similar(self, request, pk=None):
        prop = self.get_object()
        base_price = prop.pricing_profile.asking_price if hasattr(prop, 'pricing_profile') and prop.pricing_profile.asking_price else prop.price_estimate
        queryset = self.get_queryset().filter(status=PropertyListing.Status.ACTIVE).exclude(pk=prop.pk)
        queryset = queryset.filter(Q(asset_type=prop.asset_type) | Q(location_text__icontains=prop.location_text or ''))
        if base_price:
            queryset = queryset.filter(effective_price__gte=float(base_price) * 0.75, effective_price__lte=float(base_price) * 1.25)
        serializer = self.get_serializer(queryset[:3], many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[permissions.AllowAny])
    def events(self, request, pk=None):
        prop = self.get_object()
        events = prop.events.all()[:50]
        serializer = PropertyEventSerializer(events, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.AllowAny], url_path='notify-me')
    def notify_me(self, request, pk=None):
        prop = self.get_object()
        serializer = PropertyInterestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        interest, _ = PropertyInterest.objects.update_or_create(
            property=prop,
            email=serializer.validated_data['email'],
            reason=serializer.validated_data.get('reason') or 'availability',
            defaults={'full_name': serializer.validated_data.get('full_name', '')},
        )
        notify_property_operators(
            prop,
            'New property interest',
            f'{interest.email} asked to be notified when {prop.title} is available.',
            action='review_interest',
            extra_data={'interest_id': interest.id},
        )
        return Response(PropertyInterestSerializer(interest).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny], url_path='saved-searches')
    def saved_searches(self, request):
        serializer = SavedPropertySearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        saved = serializer.save(user=request.user if request.user.is_authenticated else None)
        return Response(SavedPropertySearchSerializer(saved).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='analytics')
    def analytics(self, request):
        queryset = self.get_queryset().filter(Q(owner=request.user) | Q(manager=request.user)).distinct()
        total = queryset.count()
        active = queryset.filter(status=PropertyListing.Status.ACTIVE).count()
        inquiry_count = PropertyInquiry.objects.filter(property__in=queryset).count()
        appointment_count = PropertyAppointment.objects.filter(property__in=queryset).count()
        conversion_rate = round((appointment_count / inquiry_count) * 100, 1) if inquiry_count else 0
        per_property = queryset.annotate(
            inquiry_total=Count('inquiries', distinct=True),
            appointment_total=Count('appointments', distinct=True),
        ).values('id', 'title', 'status', 'inquiry_total', 'appointment_total')[:50]
        return Response({
            'total_properties': total,
            'active_properties': active,
            'total_views': 0,
            'inquiries_this_month': inquiry_count,
            'appointments_booked': appointment_count,
            'conversion_rate': conversion_rate,
            'properties': list(per_property),
        })

    @action(detail=False, methods=['get'], url_path='manager/recommendations')
    def manager_recommendations(self, request):
        queryset = self.get_queryset().filter(Q(owner=request.user) | Q(manager=request.user)).distinct()
        recommendations = []
        for prop in queryset[:100]:
            score = property_readiness_score(prop)
            if score < 80:
                recommendations.append({
                    'type': 'INCOMPLETE_LISTING',
                    'property_id': prop.id,
                    'priority': 'HIGH' if score < 50 else 'MEDIUM',
                    'cta': f'/properties/{prop.id}/edit',
                    'reason': f'{prop.title} is {score}% ready. Add the missing listing details before pushing it harder.',
                })
            if prop.appointment_enabled and not prop.availability_windows.filter(is_active=True).exists():
                recommendations.append({
                    'type': 'MISSING_VISIT_SLOTS',
                    'property_id': prop.id,
                    'priority': 'HIGH',
                    'cta': '/property-manager/dashboard',
                    'reason': f'Add visit slots to {prop.title} so interested buyers can book immediately.',
                })
        stale_cutoff = timezone.now() - timedelta(hours=48)
        stale_inquiries = PropertyInquiry.objects.filter(property__in=queryset, status=PropertyInquiry.Status.NEW, created_at__lt=stale_cutoff)[:20]
        for inquiry in stale_inquiries:
            recommendations.append({
                'type': 'STALE_INQUIRY',
                'property_id': inquiry.property_id,
                'priority': 'HIGH',
                'cta': '/property-manager/dashboard',
                'reason': f'Respond to {inquiry.full_name}; this inquiry has waited more than 48 hours.',
            })
        return Response(recommendations[:20])

    @action(detail=True, methods=['post'], url_path='moderate')
    def moderate(self, request, pk=None):
        prop = self.get_object()
        decision = request.data.get('decision')
        notes = request.data.get('notes', '')
        if decision == 'approve':
            prop.status = PropertyListing.Status.ACTIVE
            subject = 'Property approved'
            message = f'{prop.title} has been approved and is now active.'
        elif decision == 'reject':
            prop.status = PropertyListing.Status.INACTIVE
            subject = 'Property rejected'
            message = f'{prop.title} was rejected. {notes}'.strip()
        elif decision == 'request_changes':
            prop.status = PropertyListing.Status.DRAFT
            subject = 'Property changes requested'
            message = f'Changes were requested for {prop.title}. {notes}'.strip()
        else:
            return Response({'detail': 'Use decision approve, reject, or request_changes.'}, status=status.HTTP_400_BAD_REQUEST)
        prop.save(update_fields=['status', 'updated_at'])
        if decision == 'approve':
            dispatch_saved_search_alerts_for_property(prop)
        record_property_event(
            prop,
            PropertyEvent.EventType.MODERATION_UPDATED,
            subject,
            message,
            actor=request.user,
            data={'decision': decision, 'notes': notes},
        )
        notify_property_operators(prop, subject, message, action='moderation_update', extra_data={'notes': notes})
        return Response({'status': prop.status, 'notes': notes})


class PropertyInquiryViewSet(viewsets.ModelViewSet):
    queryset = PropertyInquiry.objects.all().order_by('-created_at')
    serializer_class = PropertyInquirySerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), HasRequiredPermission(), IsPropertyOperator()]

    required_permission = 'property:view'
    permission_map = {
        'update': 'property:manage_inquiries',
        'partial_update': 'property:manage_inquiries',
        'destroy': 'property:manage_inquiries',
    }

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
            action='review_inquiry',
            extra_data={
                'inquiry_id': serializer.instance.id,
            },
        )
        record_property_event(
            prop,
            PropertyEvent.EventType.INQUIRY_RECEIVED,
            'Inquiry received',
            f'{serializer.instance.full_name} submitted a property inquiry.',
            actor=self.request.user,
            data={'inquiry_id': serializer.instance.id},
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
        window = serializer.save(managed_by=self.request.user, property=prop)
        record_property_event(
            prop,
            PropertyEvent.EventType.SLOT_ADDED,
            'Visit slots added',
            f'Availability was published for {prop.title}.',
            actor=self.request.user,
            data={'availability_window_id': window.id},
        )


class PropertyAppointmentViewSet(viewsets.ModelViewSet):
    queryset = PropertyAppointment.objects.all().order_by('scheduled_start')
    serializer_class = PropertyAppointmentSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        if self.action in {'confirm', 'cancel', 'complete', 'reschedule'}:
            return [permissions.IsAuthenticated(), HasRequiredPermission(), IsPropertyOperator()]
        return [permissions.IsAuthenticated(), HasRequiredPermission(), IsPropertyOperator()]

    required_permission = 'property:view'
    permission_map = {
        'update': 'property:manage_appointments',
        'partial_update': 'property:manage_appointments',
        'destroy': 'property:manage_appointments',
    }

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
            action='review_appointment',
            extra_data={
                'appointment_id': serializer.instance.id,
            },
        )
        record_property_event(
            prop,
            PropertyEvent.EventType.VISIT_BOOKED,
            'Visit booked',
            f'{serializer.instance.full_name} booked a visit.',
            actor=self.request.user,
            data={'appointment_id': serializer.instance.id},
        )

    def _update_status(self, request, status_value, title):
        appointment = self.get_object()
        appointment.status = status_value
        if request.data.get('notes'):
            appointment.notes = request.data.get('notes')
        appointment.save(update_fields=['status', 'notes'])
        record_property_event(
            appointment.property,
            PropertyEvent.EventType.VISIT_UPDATED,
            title,
            request.data.get('notes', ''),
            actor=request.user,
            data={'appointment_id': appointment.id, 'status': appointment.status},
        )
        return Response(self.get_serializer(appointment).data)

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        return self._update_status(request, PropertyAppointment.Status.CONFIRMED, 'Visit confirmed')

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        return self._update_status(request, PropertyAppointment.Status.CANCELLED, 'Visit cancelled')

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        return self._update_status(request, PropertyAppointment.Status.COMPLETED, 'Visit completed')

    @action(detail=True, methods=['post'])
    def reschedule(self, request, pk=None):
        appointment = self.get_object()
        scheduled_start = request.data.get('scheduled_start')
        scheduled_end = request.data.get('scheduled_end')
        if not scheduled_start or not scheduled_end:
            return Response({'detail': 'Provide scheduled_start and scheduled_end.'}, status=status.HTTP_400_BAD_REQUEST)
        appointment.scheduled_start = scheduled_start
        appointment.scheduled_end = scheduled_end
        appointment.status = PropertyAppointment.Status.REQUESTED
        if request.data.get('notes'):
            appointment.notes = request.data.get('notes')
        appointment.save(update_fields=['scheduled_start', 'scheduled_end', 'status', 'notes'])
        record_property_event(
            appointment.property,
            PropertyEvent.EventType.VISIT_UPDATED,
            'Visit rescheduled',
            appointment.notes,
            actor=request.user,
            data={'appointment_id': appointment.id},
        )
        return Response(self.get_serializer(appointment).data)
