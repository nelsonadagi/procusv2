from celery import shared_task
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@shared_task
def notify_vendor_new_order(order_id):
    logger.info(f"NOTIFY: Vendor notified of new Order #{order_id}")
    # Integration with MessagingGatewayConfig will go here in Phase 2
    pass

@shared_task
def notify_buyer_order_confirmed(order_id):
    logger.info(f"NOTIFY: Buyer notified of Order #{order_id} confirmation")
    pass

@shared_task
def notify_delivery_update(order_id, status):
    logger.info(f"NOTIFY: Delivery update for Order #{order_id}: {status}")
    pass

@shared_task
def update_vendor_performance_metrics(vendor_id):
    from vendors.models import Vendor
    from orders.models import Order
    from django.db.models import Count, Q
    
    vendor = Vendor.objects.get(id=vendor_id)
    orders = Order.objects.filter(vendor=vendor)
    total_orders = orders.count()
    
    if total_orders > 0:
        completed_orders = orders.filter(status='COMPLETED').count()
        cancelled_orders = orders.filter(status='CANCELLED').count()
        
        vendor.fulfillment_rate = (completed_orders / total_orders) * 100
        vendor.cancellation_rate = (cancelled_orders / total_orders) * 100
        # Simplistic timeliness: percentage of orders completed (placeholder logic)
        vendor.delivery_timeliness = (completed_orders / total_orders) * 100
        
        # Ratings
        from reviews.models import Rating
        from django.db.models import Avg
        rating_stats = Rating.objects.filter(vendor=vendor).aggregate(Avg('score'), Count('id'))
        vendor.average_rating = rating_stats['score__avg'] or 0.0
        vendor.total_reviews = rating_stats['id__count']
        
        vendor.save()
        logger.info(f"METRICS: Updated performance for Vendor {vendor.business_name}: FR={vendor.fulfillment_rate}%, Rating={vendor.average_rating}")
