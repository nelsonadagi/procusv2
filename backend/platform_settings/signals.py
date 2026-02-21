from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import PlatformSettings, PaymentGatewayConfig, MessagingGatewayConfig, FeatureFlag
from rbac.utils import log_action
import json

def get_current_user():
    # This is a bit tricky without middleware, but for admin actions, 
    # we can try to get it if available or log as SYSTEM.
    # In a real app, use a thread-local or middleware to capture the actor.
    return None # Placeholder

@receiver(post_save, sender=PlatformSettings)
@receiver(post_save, sender=PaymentGatewayConfig)
@receiver(post_save, sender=MessagingGatewayConfig)
@receiver(post_save, sender=FeatureFlag)
def log_config_change(sender, instance, created, **kwargs):
    action = f"{'CREATE' if created else 'UPDATE'}_{sender.__name__.upper()}"
    resource_type = sender.__name__.lower()
    
    # We don't want to log secret keys in cleartext in the metadata
    metadata = {
        "id": instance.id,
    }
    
    # In a more complete implementation, we'd diff the values
    log_action(None, action, resource_type, instance.id, metadata=metadata)
