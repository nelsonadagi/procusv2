import pytest
from django.urls import reverse
from rest_framework import status
from orders.models import Order, QuoteRequest, QuoteResponse, QuoteItem
from vendors.models import Vendor
from catalog.models import Product, ProductInventoryMovement
from logistics.models import Carrier, Shipment
from payments.models import Payment
from taxonomy.models import Category
from django.utils import timezone
from datetime import timedelta

@pytest.mark.django_db
class TestOrdersAPI:
    def setup_vendor(self, user):
        return Vendor.objects.create(
            user=user,
            business_name="Vendor Co",
            registration_number="123",
            location_text="City",
            verified_status='APPROVED'
        )

    def setup_product(self, vendor):
        cat = Category.objects.create(name="Mat", slug="mat", taxonomy_type="MATERIAL")
        return Product.objects.create(
            vendor=vendor,
            category=cat,
            name="Cement",
            unit="bag",
            base_price=500,
            stock_quantity=100
        )

    def test_list_orders_buyer(self, api_client, project_owner, vendor):
        v_profile = self.setup_vendor(vendor)
        Order.objects.create(buyer=project_owner, vendor=v_profile, total_amount=1000)
        
        api_client.force_authenticate(user=project_owner)
        url = reverse('orders-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1

    def test_update_fulfillment_vendor(self, api_client, vendor, project_owner):
        v_profile = self.setup_vendor(vendor)
        order = Order.objects.create(buyer=project_owner, vendor=v_profile, total_amount=1000)
        
        api_client.force_authenticate(user=vendor)
        url = reverse('orders-update-fulfillment', args=[order.id])
        data = {'status': 'CONFIRMED', 'estimated_delivery_at': (timezone.now() + timedelta(days=2)).isoformat()}
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        order.refresh_from_db()
        assert order.status == 'CONFIRMED'

    def test_checkout_quote(self, api_client, project_owner, vendor):
        v_profile = self.setup_vendor(vendor)
        prod = self.setup_product(v_profile)
        
        qr = QuoteRequest.objects.create(buyer=project_owner)
        QuoteItem.objects.create(quote_request=qr, product=prod, quantity=10)
        
        qres = QuoteResponse.objects.create(
            quote_request=qr,
            vendor=v_profile,
            confirmed_price=4500,
            delivery_fee=200,
            expires_at=timezone.now() + timedelta(days=7)
        )
        
        api_client.force_authenticate(user=project_owner)
        url = reverse('quote-requests-checkout', args=[qr.id])
        data = {'response_id': qres.id}
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Order.objects.filter(quote_response=qres).exists()
        prod.refresh_from_db()
        assert prod.stock_quantity == 90 # 100 - 10
        movement = ProductInventoryMovement.objects.get(product=prod, movement_type=ProductInventoryMovement.MovementType.ORDER_COMMIT)
        assert movement.quantity_delta == -10
        order = Order.objects.get(quote_response=qres)
        assert order.items.first().product == prod

    def test_cancel_order(self, api_client, project_owner, vendor):
        v_profile = self.setup_vendor(vendor)
        prod = self.setup_product(v_profile)
        prod.stock_quantity = 75
        prod.save()
        order = Order.objects.create(buyer=project_owner, vendor=v_profile, total_amount=1000, status='PLACED')
        order.items.create(
            product=prod,
            product_name_snapshot=prod.name,
            unit_price_snapshot=prod.base_price,
            quantity=5,
        )
        
        api_client.force_authenticate(user=project_owner)
        url = reverse('orders-cancel-order', args=[order.id])
        response = api_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        order.refresh_from_db()
        prod.refresh_from_db()
        assert order.status == 'CANCELLED'
        assert prod.stock_quantity == 80
        movement = ProductInventoryMovement.objects.get(product=prod, movement_type=ProductInventoryMovement.MovementType.ORDER_RESTOCK)
        assert movement.quantity_delta == 5

    def test_simulate_payment_initiates_delivery(self, api_client, project_owner, vendor):
        v_profile = self.setup_vendor(vendor)
        Carrier.objects.create(name="G4S", code="G4S", is_active=True)
        order = Order.objects.create(buyer=project_owner, vendor=v_profile, total_amount=1000, status='PLACED')
        Payment.objects.create(order=order, provider='SIMULATED', amount=1000, status='PENDING')

        api_client.force_authenticate(user=project_owner)
        url = reverse('orders-simulate-payment', args=[order.id])
        response = api_client.post(url, {}, format='json')

        assert response.status_code == status.HTTP_200_OK
        order.refresh_from_db()
        assert order.payment_status == 'PAID'
        assert order.status == 'CONFIRMED'
        shipment = Shipment.objects.get(order=order)
        assert shipment.tracking_number
        assert order.tracking_number == shipment.tracking_number
        assert shipment.events.filter(status='PENDING').exists()

    def test_confirm_delivery(self, api_client, project_owner, vendor):
        v_profile = self.setup_vendor(vendor)
        order = Order.objects.create(buyer=project_owner, vendor=v_profile, total_amount=1000, status='SHIPPED')
        
        api_client.force_authenticate(user=project_owner)
        url = reverse('orders-confirm-delivery', args=[order.id])
        response = api_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        order.refresh_from_db()
        assert order.status == 'COMPLETED'
        assert order.buyer_confirmed_delivery == True

    def test_initiate_dispute(self, api_client, project_owner, vendor):
        v_profile = self.setup_vendor(vendor)
        order = Order.objects.create(buyer=project_owner, vendor=v_profile, total_amount=1000)
        
        api_client.force_authenticate(user=project_owner)
        url = reverse('orders-initiate-dispute', args=[order.id])
        data = {'reason': 'Item damaged'}
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        from disputes.models import Dispute
        assert Dispute.objects.filter(order=order, opened_by=project_owner).exists()

    def test_respond_to_quote(self, api_client, vendor, project_owner):
        v_profile = self.setup_vendor(vendor)
        prod = self.setup_product(v_profile)
        qr = QuoteRequest.objects.create(buyer=project_owner)
        QuoteItem.objects.create(quote_request=qr, product=prod, quantity=5)
        
        api_client.force_authenticate(user=vendor)
        url = reverse('quote-requests-respond', args=[qr.id])
        data = {
            'delivery_fee': 50,
            'valid_until': (timezone.now() + timedelta(days=1)).isoformat(),
            'items': [
                {
                    'id': qr.items.first().id,
                    'unit_price': '500',
                    'availability_notes': 'Ready for dispatch',
                }
            ],
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert qr.responses.filter(vendor=v_profile).exists()
