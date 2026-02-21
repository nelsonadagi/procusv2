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
             # Notify awarded contractor if possible
             # For now we'll notify the owner as well or log it
             pass

@receiver(post_save, sender=Payment)
def notify_on_payment_status(sender, instance, created, **kwargs):
    if not created:
        user = instance.order.user
        if instance.status == 'PAID':
            notify_user(
                user=user,
                notification_type=Notification.Type.PAYMENT,
                subject="Payment Successful",
                message=f"Your payment of {instance.amount} for order {instance.order.id} has been confirmed."
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
        # Notify both parties
        users = [instance.escrow_account.buyer]
        # Contractor should also be notified if we can reach them
        for user in users:
            notify_user(
                user=user,
                notification_type=Notification.Type.ESCROW,
                subject="Escrow Account Frozen",
                message=f"An escrow hold has been placed on {instance.escrow_account.contract.title} due to a dispute."
            )
