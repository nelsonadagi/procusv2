from django.db.models.signals import post_save
from django.dispatch import receiver
from bids.models import Bid
from milestones.models import Milestone
from payments.models import Payment
from escrow.models import EscrowHold
from .services import notify_user
from .models import Notification

@receiver(post_save, sender=Bid)
def notify_on_new_bid(sender, instance, created, **kwargs):
    if created:
        owner = instance.contract.owner
        notify_user(
            user=owner,
            notification_type=Notification.Type.BID,
            subject=f"New Bid for {instance.contract.title}",
            message=f"Contractor {instance.contractor.company_name} has submitted a bid for {instance.proposed_cost}."
        )

@receiver(post_save, sender=Milestone)
def notify_on_milestone_update(sender, instance, created, **kwargs):
    if not created:
        if instance.status == 'COMPLETED':
             notify_user(
                user=instance.contract.owner,
                notification_type=Notification.Type.MILESTONE,
                subject=f"Milestone COMPLETED: {instance.title}",
                message=f"Please review and approve the milestone for project {instance.contract.title}."
            )
        elif instance.status == 'APPROVED':
             awarded_bid = instance.contract.bids.filter(status='AWARDED').select_related('contractor__user').first()
             if awarded_bid:
                notify_user(
                    user=awarded_bid.contractor.user,
                    notification_type=Notification.Type.MILESTONE,
                    subject=f"Milestone approved: {instance.title}",
                    message=f"The owner approved {instance.title}. Payment is pending release."
                )

@receiver(post_save, sender=Payment)
def notify_on_payment_status(sender, instance, created, **kwargs):
    if not created:
        user = instance.order.buyer
        if instance.status == 'PAID':
            order = instance.order
            update_fields = []
            if order.payment_status != 'PAID':
                order.payment_status = 'PAID'
                update_fields.append('payment_status')
            if order.status == 'PLACED':
                order.status = 'CONFIRMED'
                update_fields.append('status')
            if update_fields:
                order.save(update_fields=[*update_fields, 'updated_at'])

            from orders.services import initiate_delivery_for_paid_order
            shipment = initiate_delivery_for_paid_order(order)

            notify_user(
                user=user,
                notification_type=Notification.Type.PAYMENT,
                subject="Payment Successful",
                message=f"Your payment of {instance.amount} for order {order.id} has been confirmed.",
                data={"order_id": order.id, "shipment_id": shipment.id, "tracking_number": shipment.tracking_number},
            )
            notify_user(
                user=order.vendor.user,
                notification_type=Notification.Type.SYSTEM,
                subject="Payment confirmed",
                message=f"Order #{order.id} has been paid. Start fulfillment and delivery preparation.",
                data={"order_id": order.id, "shipment_id": shipment.id, "tracking_number": shipment.tracking_number},
            )
        elif instance.status == 'FAILED':
            notify_user(
                user=user,
                notification_type=Notification.Type.PAYMENT,
                subject="Payment Failed",
                message=f"Your payment of {instance.amount} for order {instance.order.id} has failed. Please try again."
            )

@receiver(post_save, sender=EscrowHold)
def notify_on_escrow_freeze(sender, instance, created, **kwargs):
    if created:
        awarded_bid = instance.escrow_account.contract.bids.filter(status='AWARDED').select_related('contractor__user').first()
        users = [instance.escrow_account.buyer]
        if awarded_bid:
            users.append(awarded_bid.contractor.user)
        for user in users:
            notify_user(
                user=user,
                notification_type=Notification.Type.ESCROW,
                subject="Escrow Account Frozen",
                message=f"An escrow hold has been placed on {instance.escrow_account.contract.title} due to a dispute."
            )
