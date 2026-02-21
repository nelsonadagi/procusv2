import pytest
from django.urls import reverse
from notifications.models import Notification, NotificationPreference
from bids.models import Bid

@pytest.mark.django_db
def test_notification_created_on_new_bid(api_client, project_owner, contractor):
    # Setup
    from conftest import ContractFactory
    from contractors.models import ContractorProfile
    
    contract = ContractFactory(owner=project_owner)
    contractor_profile = ContractorProfile.objects.create(
        user=contractor,
        company_name="Test Contractor",
        service_categories=[],
        operating_region="Region"
    )
    
    # Create a bid
    Bid.objects.create(
        contract=contract,
        contractor=contractor_profile,
        proposed_cost=1000,
        proposed_timeline_days=30,
        status='SUBMITTED'
    )
    
    # Check notification for project owner
    notifications = Notification.objects.filter(user=project_owner)
    assert notifications.count() == 1
    assert notifications.first().type == Notification.Type.BID
    assert "New Bid" in notifications.first().subject

@pytest.mark.django_db
def test_notification_preferences_api(api_client, project_owner):
    api_client.force_authenticate(user=project_owner)
    url = reverse('notification-preferences')
    
    # GET
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['email_enabled'] is True
    
    # PATCH
    response = api_client.patch(url, {'email_enabled': False, 'sms_enabled': True})
    assert response.status_code == 200
    assert response.data['email_enabled'] is False
    assert response.data['sms_enabled'] is True
    
    prefs = NotificationPreference.objects.get(user=project_owner)
    assert prefs.email_enabled is False
    assert prefs.sms_enabled is True
