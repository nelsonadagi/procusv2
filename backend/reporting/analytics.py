"""
Admin Analytics Module for Ujenzi Marketplace.

Provides aggregation endpoints for the admin reports dashboard.
All functions accept an optional `days` parameter for time-windowed queries.
"""

from datetime import timedelta
from django.utils import timezone
from django.db.models import (
    Count, Sum, Avg, F, Q, Value, DecimalField,
)
from django.db.models.functions import TruncDate, Coalesce
from django.contrib.auth import get_user_model

User = get_user_model()


def get_date_range(days=30):
    """Return start and end dates for time-windowed queries."""
    end = timezone.now()
    start = end - timedelta(days=days)
    return start, end


def summary_kpis(days=30):
    """High-level platform KPIs."""
    from accounts.models import User
    from orders.models import Order
    from vendors.models import Vendor
    from property.models import PropertyListing
    from disputes.models import Dispute
    from projects.models import Project
    from contracts.models import Contract
    from compliance.models import KYCVerification

    start, end = get_date_range(days)

    total_users = User.objects.count()
    new_users = User.objects.filter(date_joined__gte=start).count()

    total_orders = Order.objects.count()
    new_orders = Order.objects.filter(created_at__gte=start).count()

    total_revenue = (
        Order.objects.filter(
            status__in=[Order.Status.COMPLETED, Order.Status.DELIVERED]
        ).aggregate(total=Coalesce(Sum('total_amount'), Value(0, output_field=DecimalField())))
    )['total']

    period_revenue = (
        Order.objects.filter(
            created_at__gte=start,
            status__in=[Order.Status.COMPLETED, Order.Status.DELIVERED]
        ).aggregate(total=Coalesce(Sum('total_amount'), Value(0, output_field=DecimalField())))
    )['total']

    # Daily trends for overview
    daily_orders = (
        Order.objects.filter(created_at__gte=start)
        .annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(orders=Count('id'))
        .order_by('date')
    )
    daily_revenue = (
        Order.objects.filter(created_at__gte=start)
        .annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(revenue=Coalesce(Sum('total_amount'), Value(0, output_field=DecimalField())))
        .order_by('date')
    )

    total_vendors = Vendor.objects.count()
    approved_vendors = Vendor.objects.filter(verified_status=Vendor.Status.APPROVED).count()

    total_properties = PropertyListing.objects.count()
    active_properties = PropertyListing.objects.filter(status=PropertyListing.Status.ACTIVE).count()

    open_disputes = Dispute.objects.filter(status=Dispute.Status.OPENED).count()
    total_disputes = Dispute.objects.count()

    total_projects = Project.objects.count()
    total_contracts = Contract.objects.count()

    pending_kyc = KYCVerification.objects.filter(status=KYCVerification.Status.PENDING).count()

    return {
        'users': {
            'total': total_users,
            'new': new_users,
        },
        'orders': {
            'total': total_orders,
            'new': new_orders,
        },
        'revenue': {
            'total': float(total_revenue or 0),
            'period': float(period_revenue or 0),
        },
        'order_trend': [
            {'x': d['date'].isoformat() if d['date'] else None, 'y': d['orders']}
            for d in daily_orders
        ],
        'revenue_trend': [
            {'x': d['date'].isoformat() if d['date'] else None, 'y': float(d['revenue'] or 0)}
            for d in daily_revenue
        ],
        'vendors': {
            'total': total_vendors,
            'approved': approved_vendors,
        },
        'properties': {
            'total': total_properties,
            'active': active_properties,
        },
        'disputes': {
            'total': total_disputes,
            'open': open_disputes,
        },
        'projects': total_projects,
        'contracts': total_contracts,
        'pending_kyc': pending_kyc,
        'period_days': days,
    }


def financial_trends(days=30):
    """Daily revenue and order trends."""
    from orders.models import Order
    from payments.models import Payment

    start, end = get_date_range(days)

    # Daily order/revenue aggregation
    daily_orders = (
        Order.objects.filter(created_at__gte=start)
        .annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(
            orders=Count('id'),
            revenue=Coalesce(Sum('total_amount'), Value(0, output_field=DecimalField())),
        )
        .order_by('date')
    )

    order_trend = []
    revenue_trend = []
    for row in daily_orders:
        d = row['date'].isoformat() if row['date'] else None
        order_trend.append({'x': d, 'y': row['orders']})
        revenue_trend.append({'x': d, 'y': float(row['revenue'] or 0)})

    # Payment status breakdown
    payment_status = (
        Payment.objects.values('status')
        .annotate(count=Count('id'), total=Coalesce(Sum('amount'), Value(0, output_field=DecimalField())))
        .order_by('-count')
    )

    # AOV
    aov_data = Order.objects.filter(
        created_at__gte=start
    ).aggregate(aov=Avg('total_amount'))

    # Calculate period revenue for financial card
    period_revenue = (
        Order.objects.filter(
            created_at__gte=start,
            status__in=[Order.Status.COMPLETED, Order.Status.DELIVERED]
        ).aggregate(total=Coalesce(Sum('total_amount'), Value(0, output_field=DecimalField())))
    )['total']

    return {
        'order_trend': order_trend,
        'revenue_trend': revenue_trend,
        'payment_status': [
            {'status': p['status'], 'count': p['count'], 'total': float(p['total'] or 0)}
            for p in payment_status
        ],
        'aov': float(aov_data['aov'] or 0),
        'period_revenue': float(period_revenue or 0),
        'period_days': days,
    }


def marketplace_analytics(days=30):
    """Marketplace performance: order funnel, top products, vendor scores."""
    from orders.models import Order, OrderItem
    from catalog.models import Product
    from vendors.models import Vendor

    start, end = get_date_range(days)

    # Order funnel (all time + period)
    funnel_all = {}
    for status, label in Order.Status.choices:
        funnel_all[status] = Order.objects.filter(status=status).count()

    funnel_period = {}
    for status, label in Order.Status.choices:
        funnel_period[status] = Order.objects.filter(
            status=status, created_at__gte=start
        ).count()

    # Top products by order volume
    top_products = (
        OrderItem.objects.filter(order__created_at__gte=start)
        .values('product_name_snapshot')
        .annotate(
            quantity_sold=Sum('quantity'),
            revenue=Coalesce(Sum(F('unit_price_snapshot') * F('quantity')), Value(0, output_field=DecimalField()))
        )
        .order_by('-quantity_sold')[:10]
    )

    # Vendor performance leaderboard
    vendor_leaderboard = (
        Vendor.objects.filter(verified_status=Vendor.Status.APPROVED)
        .annotate(order_count=Count('orders'))
        .values('business_name', 'average_rating', 'fulfillment_rate',
                'cancellation_rate', 'delivery_timeliness', 'order_count')
        .order_by('-order_count')[:10]
    )

    # Product status distribution
    product_status = (
        Product.objects.values('status')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    # Low stock alerts
    low_stock = (
        Product.objects.filter(stock_quantity__lte=F('reorder_level'), reorder_level__gt=0)
        .values('name', 'stock_quantity', 'reorder_level')
        .order_by('stock_quantity')[:10]
    )

    return {
        'order_funnel_all': funnel_all,
        'order_funnel_period': funnel_period,
        'top_products': [
            {
                'name': p['product_name_snapshot'],
                'quantity_sold': p['quantity_sold'],
                'revenue': float(p['revenue'] or 0),
            }
            for p in top_products
        ],
        'vendor_leaderboard': [
            {
                'name': v['business_name'],
                'rating': float(v['average_rating'] or 0),
                'fulfillment_rate': float(v['fulfillment_rate'] or 0),
                'cancellation_rate': float(v['cancellation_rate'] or 0),
                'delivery_timeliness': float(v['delivery_timeliness'] or 0),
                'orders': v['order_count'],
            }
            for v in vendor_leaderboard
        ],
        'product_status': list(product_status),
        'low_stock_alerts': list(low_stock),
        'period_days': days,
    }


def user_analytics(days=30):
    """User growth and role distribution."""
    from accounts.models import User

    start, end = get_date_range(days)

    # Role distribution
    role_dist = (
        User.objects.values('role')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    # Daily signups
    daily_signups = (
        User.objects.filter(date_joined__gte=start)
        .annotate(date=TruncDate('date_joined'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )

    # Active vs inactive
    active_users = User.objects.filter(is_active=True).count()
    inactive_users = User.objects.filter(is_active=False).count()

    return {
        'role_distribution': [
            {'role': r['role'], 'count': r['count']} for r in role_dist
        ],
        'signup_trend': [
            {'x': s['date'].isoformat() if s['date'] else None, 'y': s['count']}
            for s in daily_signups
        ],
        'activation': {
            'active': active_users,
            'inactive': inactive_users,
        },
        'period_days': days,
    }


def operations_analytics(days=30):
    """Operational metrics: KYC, disputes, contracts, projects."""
    from compliance.models import KYCVerification
    from disputes.models import Dispute
    from contracts.models import Contract
    from projects.models import Project
    from contractors.models import ContractorProfile

    start, end = get_date_range(days)

    # KYC pipeline
    kyc_pipeline = {}
    for status, label in KYCVerification.Status.choices:
        kyc_pipeline[status] = KYCVerification.objects.filter(status=status).count()

    # Dispute status breakdown
    dispute_status = {}
    for status, label in Dispute.Status.choices:
        dispute_status[status] = Dispute.objects.filter(status=status).count()

    # Contract status
    contract_status = {}
    for status, label in Contract.Status.choices:
        contract_status[status] = Contract.objects.filter(status=status).count()

    # Project status
    project_status = {}
    for status, label in Project.Status.choices:
        project_status[status] = Project.objects.filter(status=status).count()

    # Contractor verification
    contractor_status = {}
    for status, label in ContractorProfile.Status.choices:
        contractor_status[status] = ContractorProfile.objects.filter(verified_status=status).count()

    return {
        'kyc_pipeline': kyc_pipeline,
        'dispute_status': dispute_status,
        'contract_status': contract_status,
        'project_status': project_status,
        'contractor_status': contractor_status,
        'period_days': days,
    }


def geographic_analytics():
    """Geographic distribution of marketplace entities."""
    from vendors.models import Vendor
    from projects.models import Project
    from property.models import PropertyListing
    from orders.models import Order

    # Entities with coordinates for map plotting
    vendors = (
        Vendor.objects.filter(latitude__isnull=False, longitude__isnull=False)
        .values('business_name', 'latitude', 'longitude', 'verified_status')
        .order_by('-created_at')[:500]
    )

    projects = (
        Project.objects.filter(latitude__isnull=False, longitude__isnull=False)
        .values('title', 'latitude', 'longitude', 'status')
        .order_by('-created_at')[:500]
    )

    properties = (
        PropertyListing.objects.filter(latitude__isnull=False, longitude__isnull=False)
        .values('title', 'latitude', 'longitude', 'status', 'asset_type')
        .order_by('-created_at')[:500]
    )

    # Orders with delivery location (if location has coords)
    orders = (
        Order.objects.filter(
            delivery_location__latitude__isnull=False,
            delivery_location__longitude__isnull=False,
        )
        .values(
            'delivery_location__latitude',
            'delivery_location__longitude',
            'status',
        )
        .order_by('-created_at')[:500]
    )

    return {
        'vendors': [
            {'name': v['business_name'], 'lat': float(v['latitude']), 'lng': float(v['longitude']), 'status': v['verified_status']}
            for v in vendors
        ],
        'projects': [
            {'name': p['title'], 'lat': float(p['latitude']), 'lng': float(p['longitude']), 'status': p['status']}
            for p in projects
        ],
        'properties': [
            {'name': prop['title'], 'lat': float(prop['latitude']), 'lng': float(prop['longitude']), 'status': prop['status'], 'type': prop['asset_type']}
            for prop in properties
        ],
        'orders': [
            {'lat': float(o['delivery_location__latitude']), 'lng': float(o['delivery_location__longitude']), 'status': o['status']}
            for o in orders
        ],
    }


def property_analytics(days=30):
    """Real estate analytics."""
    from property.models import PropertyListing, PropertyInquiry, PropertyAppointment

    start, end = get_date_range(days)

    # Listing status
    listing_status = {}
    for status, label in PropertyListing.Status.choices:
        listing_status[status] = PropertyListing.objects.filter(status=status).count()

    # Asset type distribution
    asset_types = (
        PropertyListing.objects.values('asset_type')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    # Inquiry funnel
    inquiry_status = {}
    for status, label in PropertyInquiry.Status.choices:
        inquiry_status[status] = PropertyInquiry.objects.filter(status=status).count()

    # Appointment status
    appointment_status = {}
    for status, label in PropertyAppointment.Status.choices:
        appointment_status[status] = PropertyAppointment.objects.filter(status=status).count()

    # Recent inquiries trend
    inquiry_trend = (
        PropertyInquiry.objects.filter(created_at__gte=start)
        .annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )

    return {
        'listing_status': listing_status,
        'asset_types': [
            {'type': a['asset_type'], 'count': a['count']} for a in asset_types
        ],
        'inquiry_status': inquiry_status,
        'appointment_status': appointment_status,
        'inquiry_trend': [
            {'x': i['date'].isoformat() if i['date'] else None, 'y': i['count']}
            for i in inquiry_trend
        ],
        'period_days': days,
    }
