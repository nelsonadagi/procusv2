from rest_framework.throttling import AnonRateThrottle, UserRateThrottle, ScopedRateThrottle
from .models import ThrottledRequest

def log_throttled_request(request, view, scope=None):
    from .models import ThrottledRequest
    ThrottledRequest.objects.create(
        ip_address=get_ident(request),
        user=request.user if request.user.is_authenticated else None,
        path=request.path,
        method=request.method,
        scope=scope
    )

def get_ident(request):
    """
    Identify the machine making the request by parsing HTTP_X_FORWARDED_FOR
    if present and falling back to REMOTE_ADDR.
    """
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    remote_addr = request.META.get('REMOTE_ADDR')
    if xff:
        return xff.split(',')[0].strip()
    return remote_addr

class MonitoredAnonThrottle(AnonRateThrottle):
    def throttle_failure(self):
        log_throttled_request(self.request, None, scope=self.scope)

class MonitoredUserThrottle(UserRateThrottle):
    def throttle_failure(self):
        log_throttled_request(self.request, None, scope=self.scope)

class MonitoredScopedThrottle(ScopedRateThrottle):
    def throttle_failure(self):
        log_throttled_request(self.request, None, scope=self.scope)

class GlobalIPRateThrottle(AnonRateThrottle):
    scope = 'global_limit'
    def get_cache_key(self, request, view):
        return self.get_ident(request)
    
    def throttle_failure(self):
        log_throttled_request(self.request, None, scope=self.scope)
