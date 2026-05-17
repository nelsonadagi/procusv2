def _vendor_origin_address(order):
    vendor = order.vendor
    return (
        vendor.formatted_address
        or getattr(vendor.location, 'address', None)
        or getattr(vendor.location, 'city', None)
        or vendor.location_text
        or 'Vendor dispatch location pending'
    )


def _tracking_event_location(order):
    vendor = order.vendor
    return (
        vendor.location_text
        or getattr(vendor.location, 'city', None)
        or getattr(vendor.country, 'name', None)
        or 'Dispatch hub'
    )[:255]


def _destination_address(order):
    if order.delivery_location:
        return (
            order.delivery_location.address
            or order.delivery_location.city
            or str(order.delivery_location)
        )

    buyer_profile = getattr(order.buyer, 'buyer_profile', None)
    if buyer_profile and buyer_profile.preferred_region:
        return buyer_profile.preferred_region

    if order.buyer.addresses.exists():
        addr = order.buyer.addresses.filter(is_default=True).first() or order.buyer.addresses.first()
        return str(addr)

    return 'Buyer delivery location pending'


def initiate_delivery_for_paid_order(order):
    """
    Create the initial logistics record once payment is confirmed.
    Vendor fulfillment can still move the order through PACKING/SHIPPED later.
    """
    from logistics.models import Carrier, Shipment, TrackingEvent

    carrier = (
        Carrier.objects.filter(code='G4S', is_active=True).first()
        or Carrier.objects.filter(is_active=True).order_by('id').first()
    )

    shipment, created = Shipment.objects.get_or_create(
        order=order,
        defaults={
            'carrier': carrier,
            'origin_address': _vendor_origin_address(order),
            'destination_address': _destination_address(order),
            'recipient_name': f"{order.buyer.first_name} {order.buyer.last_name}".strip() or order.buyer.username,
            'recipient_phone': getattr(order.buyer, 'phone', '') or 'Unknown',
        },
    )

    if carrier and not shipment.carrier_id:
        shipment.carrier = carrier
        shipment.save(update_fields=['carrier'])

    if not order.tracking_number:
        order.tracking_number = shipment.tracking_number
        order.save(update_fields=['tracking_number', 'updated_at'])

    if created or not shipment.events.exists():
        TrackingEvent.objects.create(
            shipment=shipment,
            status='PENDING',
            location=_tracking_event_location(order),
            description='Payment confirmed. Delivery workflow initiated and waiting for vendor fulfillment.',
            raw_payload={'source': 'payment_confirmation'},
        )

    return shipment
