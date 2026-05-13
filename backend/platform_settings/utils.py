import logging

logger = logging.getLogger(__name__)


def resolve_request_country_code(request):
    """Resolve the active country from query params or the global request header.
    
    When 'country' is explicitly present in query params (even as empty string),
    it takes precedence over the header. This allows frontend pages to send
    country='' to mean "no country filter" rather than falling back to the
    global header default.
    """
    if request is None:
        return ''
    
    # Try DRF request.query_params first, then Django request.GET
    params = getattr(request, 'query_params', None) or getattr(request, 'GET', None) or {}
    
    # If 'country' key is explicitly present in query params, honor it.
    # An empty value means "show all countries — do not filter".
    country_value = params.get('country')
    if country_value is not None:
        return str(country_value or '').strip().upper()
    
    # Fallback to X-Active-Country header only when no explicit query param
    headers = getattr(request, 'headers', {}) or {}
    header_country = headers.get('X-Active-Country') or getattr(request, 'META', {}).get('HTTP_X_ACTIVE_COUNTRY')
    return str(header_country or '').strip().upper()
