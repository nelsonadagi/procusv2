import pytest
from django.urls import reverse
from rest_framework import status
from reviews.models import Rating
from orders.models import Order
from vendors.models import Vendor

@pytest.mark.django_db
class TestReviewsAPI:
    def test_create_rating(self, api_client, project_owner, vendor):
        v_profile = Vendor.objects.create(
            user=vendor,
            business_name="Vendor Co",
            registration_number="123",
            location="City",
            verified_status='APPROVED'
        )
        order = Order.objects.create(buyer=project_owner, vendor=v_profile, total_amount=1000, status='COMPLETED')
        
        api_client.force_authenticate(user=project_owner)
        url = reverse('ratings-list')
        data = {
            'order': order.id,
            'score': 5,
            'comment': 'Great!'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Rating.objects.filter(order=order, score=5).exists()
