from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Carrier, PricingZone, Shipment, TrackingEvent, CourierProfile, PricingRule
from .serializers import CarrierSerializer, PricingZoneSerializer, PricingRuleSerializer, ShipmentSerializer, TrackingEventSerializer, CourierProfileSerializer
from .services import LogisticsService
from rbac.permissions import HasRequiredPermission, IsCourierOwner

class CourierProfileViewSet(viewsets.ModelViewSet):
    queryset = CourierProfile.objects.all()
    serializer_class = CourierProfileSerializer
    permission_classes = [permissions.IsAuthenticated, HasRequiredPermission]
    required_permission = 'logistics:view'
    permission_map = {
        'create': 'logistics:onboard',
        'update': 'logistics:manage_profile',
        'partial_update': 'logistics:manage_profile',
        'destroy': 'logistics:manage_profile',
    }

    def get_queryset(self):
        if self.request.user.role == 'ADMIN':
            return CourierProfile.objects.all()
        # Couriers see only their own profile
        return CourierProfile.objects.filter(user=self.request.user)


    @action(detail=False, methods=['get'])
    def me(self, request):
        if not hasattr(request.user, 'courier_profile'):
            return Response({"error": "User is not a registered courier"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(request.user.courier_profile)
        return Response(serializer.data)

class CarrierViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Carrier.objects.filter(is_active=True)
    serializer_class = CarrierSerializer

class PricingZoneViewSet(viewsets.ModelViewSet):
    queryset = PricingZone.objects.all()
    serializer_class = PricingZoneSerializer
    permission_classes = [permissions.IsAuthenticated, HasRequiredPermission, IsCourierOwner]
    required_permission = 'logistics:view'
    permission_map = {
        'create': 'logistics:manage_pricing',
        'update': 'logistics:manage_pricing',
        'partial_update': 'logistics:manage_pricing',
        'destroy': 'logistics:manage_pricing',
    }

    def get_queryset(self):
        if self.request.user.role == 'ADMIN':
            return PricingZone.objects.all()
        # Couriers see only their zones
        if hasattr(self.request.user, 'courier_profile'):
            return PricingZone.objects.filter(courier=self.request.user.courier_profile)
        return PricingZone.objects.none()

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'courier_profile'):
            serializer.save(courier=self.request.user.courier_profile)
        else:
            # Fallback or error if admin tries to create without explicit courier?
            # For now, assume admin passes courier or handles it.
            serializer.save()

    @action(detail=False, methods=['get'])
    def calculate(self, request):
        # Publicly accessible for now (authenticated users)
        zone_id = request.query_params.get('zone_id')
        weight = float(request.query_params.get('weight', 0))
        volume = float(request.query_params.get('volume', 0))

        result = LogisticsService.calculate_cost(zone_id, weight, volume)
        return Response(result)

class PricingRuleViewSet(viewsets.ModelViewSet):
    queryset = PricingRule.objects.all()
    serializer_class = PricingRuleSerializer
    permission_classes = [permissions.IsAuthenticated, HasRequiredPermission]
    required_permission = 'logistics:view'
    permission_map = {
        'create': 'logistics:manage_pricing',
        'update': 'logistics:manage_pricing',
        'partial_update': 'logistics:manage_pricing',
        'destroy': 'logistics:manage_pricing',
    }

    def get_queryset(self):
        if self.request.user.role == 'ADMIN':
            return PricingRule.objects.all()
        if hasattr(self.request.user, 'courier_profile'):
            return PricingRule.objects.filter(courier=self.request.user.courier_profile)
        return PricingRule.objects.none()

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'courier_profile'):
            serializer.save(courier=self.request.user.courier_profile)
        else:
            serializer.save()

class ShipmentViewSet(viewsets.ModelViewSet):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    permission_classes = [permissions.IsAuthenticated, HasRequiredPermission]
    required_permission = 'logistics:view'
    permission_map = {
        'create': 'logistics:manage_shipments',
        'update': 'logistics:manage_shipments',
        'partial_update': 'logistics:manage_shipments',
        'destroy': 'logistics:manage_shipments',
    }

    def get_queryset(self):
        if self.request.user.role == 'ADMIN':
            return Shipment.objects.all()
        # Vendors see shipments for their orders
        if hasattr(self.request.user, 'vendor_profile'):
            return Shipment.objects.filter(order__vendor=self.request.user.vendor_profile)
        # Couriers see their assigned shipments
        if hasattr(self.request.user, 'courier_profile'):
            return Shipment.objects.filter(courier=self.request.user.courier_profile)
        # Buyers see their own shipments
        return Shipment.objects.filter(order__buyer=self.request.user)

    @action(detail=True, methods=['get'])
    def track(self, request, pk=None):
        shipment = self.get_object()

        # Determine tracking provider
        carrier_code = "G4S" # Default
        if shipment.carrier:
            carrier_code = shipment.carrier.code
        elif shipment.courier and hasattr(shipment.courier, 'api_config'):
             # If using new courier system, logic would be dynamic here
             pass

        strategy = LogisticsService.get_strategy(carrier_code)
        live_status = strategy.get_tracking_status(shipment.tracking_number)

        return Response({
            "current_status": shipment.status,
            "live_update": live_status,
            "history": TrackingEventSerializer(shipment.events.all(), many=True).data
        })

class CarrierWebhookView(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny] # Usually secured via secret

    @action(detail=False, methods=['post'], url_path='update/(?P<carrier_code>[^/.]+)')
    def status_update(self, request, carrier_code=None):
        data = request.data
        tracking_number = data.get('tracking_number')
        new_status = data.get('status')
        location = data.get('location', 'Unknown')

        try:
            shipment = Shipment.objects.get(tracking_number=tracking_number)
            shipment.status = new_status
            shipment.save()

            TrackingEvent.objects.create(
                shipment=shipment,
                status=new_status,
                location=location,
                description=data.get('description', f"Status updated to {new_status}")
            )
            return Response({"status": "received"})
        except Shipment.DoesNotExist:
            return Response({"error": "Shipment not found"}, status=status.HTTP_404_NOT_FOUND)
