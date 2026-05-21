from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from django.utils import timezone

from notifications.models import Notification
from notifications.services import notify_user

from .models import PropertyListing, SavedPropertySearch


def property_matches_saved_search(prop, filters):
    if not filters:
        return True

    search = filters.get('search')
    if search:
        haystack = ' '.join([
            prop.title or '',
            prop.description or '',
            prop.location_text or '',
            prop.formatted_address or '',
            getattr(prop.development_metadata, 'recommended_use', '') if hasattr(prop, 'development_metadata') else '',
        ]).lower()
        if search.lower() not in haystack:
            return False

    exact_fields = ['asset_type', 'listing_type', 'status']
    for field in exact_fields:
        if filters.get(field) and getattr(prop, field, None) != filters[field]:
            return False

    if filters.get('country') and (not prop.country or prop.country.iso_code.lower() != str(filters['country']).lower()):
        return False

    if filters.get('location'):
        location_query = str(filters['location']).lower()
        location_text = ' '.join([prop.location_text or '', prop.formatted_address or '']).lower()
        if location_query not in location_text:
            return False

    if filters.get('financing_allowed') in {True, 'true', 'True'} and not prop.financing_allowed:
        return False

    if filters.get('build_ready') in {True, 'true', 'True'}:
        if not hasattr(prop, 'development_metadata') or not prop.development_metadata.build_ready:
            return False

    effective_price = None
    if hasattr(prop, 'pricing_profile') and prop.pricing_profile.asking_price:
        effective_price = prop.pricing_profile.asking_price
    elif prop.price_estimate:
        effective_price = prop.price_estimate

    if filters.get('min_price') not in {None, ''} and effective_price is not None and effective_price < float(filters['min_price']):
        return False
    if filters.get('max_price') not in {None, ''} and effective_price is not None and effective_price > float(filters['max_price']):
        return False

    if filters.get('development_stage'):
        if not hasattr(prop, 'development_metadata') or prop.development_metadata.development_stage != filters['development_stage']:
            return False

    if filters.get('condition_rating'):
        if not hasattr(prop, 'specification') or prop.specification.condition_rating != filters['condition_rating']:
            return False

    if filters.get('occupancy_status'):
        if not hasattr(prop, 'specification') or prop.specification.occupancy_status != filters['occupancy_status']:
            return False

    return True


def dispatch_saved_search_alerts_for_property(prop):
    if prop.status != PropertyListing.Status.ACTIVE:
        return 0

    delivered = 0
    searches = SavedPropertySearch.objects.filter(is_active=True).filter(Q(email__gt='') | Q(user__isnull=False))
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@ujenzi.local')
    subject = f'New property match: {prop.title}'
    message = (
        f'{prop.title} matches your saved property search.\n\n'
        f'Location: {prop.location_text or prop.formatted_address or "Location pending"}\n'
        f'Open: /properties/{prop.id}'
    )

    for saved_search in searches:
        if not property_matches_saved_search(prop, saved_search.filters or {}):
            continue
        if saved_search.user:
            notify_user(
                saved_search.user,
                Notification.Type.SYSTEM,
                subject,
                message,
                data={
                    'property_id': prop.id,
                    'saved_search_id': saved_search.id,
                    'property_url': f'/properties/{prop.id}',
                    'action': 'open_property_match',
                },
            )
            delivered += 1
        if saved_search.email:
            send_mail(subject, message, from_email, [saved_search.email], fail_silently=True)
            delivered += 1
    return delivered


def dispatch_recent_saved_search_alerts(days=1):
    since = timezone.now() - timedelta(days=days)
    count = 0
    queryset = PropertyListing.objects.filter(status=PropertyListing.Status.ACTIVE, created_at__gte=since)
    queryset = queryset.select_related('country', 'development_metadata', 'specification', 'pricing_profile')
    for prop in queryset:
        count += dispatch_saved_search_alerts_for_property(prop)
    return count
