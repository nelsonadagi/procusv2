from .models import AuditLog

def log_action(user, action, resource_type, resource_id=None, metadata=None):
    AuditLog.objects.create(
        actor=user,
        action=action,
        resource_type=resource_type,
        resource_id=str(resource_id) if resource_id else None,
        metadata=metadata
    )
