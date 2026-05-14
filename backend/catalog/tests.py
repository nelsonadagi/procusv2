import pytest
from django.urls import reverse
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from catalog.models import (
    Product,
    ProductImage,
    ProductDocument,
    ProductCertificationRegistry,
    ProductCertification,
    ProductAttribute,
    ProductInventoryMovement,
)
from vendors.models import Vendor
from taxonomy.models import Category
import io
import csv

@pytest.mark.django_db
class TestCatalogAPI:
    def setup_vendor(self, user):
        return Vendor.objects.create(
            user=user,
            business_name="Hardware Store",
            registration_number="REG001",
            location_text="Nairobi",
            verified_status='APPROVED'
        )

    def setup_category(self):
        return Category.objects.get_or_create(
            name="Cement",
            slug="cement",
            taxonomy_type='MATERIAL',
            active=True
        )[0]

    def test_list_products_public(self, api_client, vendor):
        v_profile = self.setup_vendor(vendor)
        cat = self.setup_category()
        Product.objects.create(
            vendor=v_profile,
            category=cat,
            name="Simba Cement",
            base_price=650,
            unit="bag",
            stock_quantity=25,
            status='ACTIVE'
        )

        url = reverse('product-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1

    def test_create_product_vendor(self, api_client, vendor):
        v_profile = self.setup_vendor(vendor)
        cat = self.setup_category()
        api_client.force_authenticate(user=vendor)

        url = reverse('product-list')
        data = {
            'category': str(cat.uuid),
            'name': 'Bamburi Cement',
            'description': 'High quality',
            'base_price': 700,
            'unit': 'bag',
            'stock_quantity': 50
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Product.objects.filter(name='Bamburi Cement').exists()

    def test_create_product_with_structured_material_data(self, api_client, vendor):
        self.setup_vendor(vendor)
        cat = self.setup_category()
        registry = ProductCertificationRegistry.objects.create(
            name='KEBS',
            code='KEBS',
            issuer='Kenya Bureau of Standards',
        )
        api_client.force_authenticate(user=vendor)

        url = reverse('product-list')
        data = {
            'category': str(cat.uuid),
            'name': 'Premium Ready Mix',
            'description': 'Engineered concrete mix for slab casting.',
            'short_description': 'High-strength ready mix concrete.',
            'base_price': 14500,
            'unit': 'm3',
            'stock_quantity': 18,
            'reorder_level': 5,
            'country_of_origin': 'Kenya',
            'packaging_details': 'Delivered by mixer truck',
            'certification_entries': [
                {
                    'registry': str(registry.uuid),
                    'display_name': 'KEBS Quality Mark',
                    'certification_number': 'Q-553200',
                    'issuing_body': 'KEBS',
                    'status': 'ACTIVE',
                }
            ],
            'attribute_entries': [
                {
                    'group': 'Performance',
                    'name': 'Compressive Strength',
                    'value': '30',
                    'unit': 'MPa',
                    'is_highlight': True,
                    'sort_order': 1,
                }
            ],
            'documents': [
                {
                    'document_type': 'DATASHEET',
                    'title': 'Product Datasheet',
                    'external_url': 'https://example.com/datasheet.pdf',
                    'description': 'Technical product sheet',
                    'is_public': True,
                }
            ],
        }
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        product = Product.objects.get(name='Premium Ready Mix')
        assert product.reorder_level == 5
        assert product.certification_entries.count() == 1
        assert product.attribute_entries.count() == 1
        assert product.documents.count() == 1

    def test_filter_products_by_certification_and_inventory_signal(self, api_client, vendor):
        vendor_profile = self.setup_vendor(vendor)
        cat = self.setup_category()
        registry = ProductCertificationRegistry.objects.create(name='ISO 9001', code='ISO9001')
        certified = Product.objects.create(
            vendor=vendor_profile,
            category=cat,
            name='Certified Cement',
            base_price=800,
            unit='bag',
            stock_quantity=3,
            reorder_level=5,
            status='ACTIVE',
        )
        ProductCertification.objects.create(
            product=certified,
            registry=registry,
            display_name='ISO 9001',
        )
        ProductAttribute.objects.create(
            product=certified,
            name='Strength',
            value='42.5',
            unit='grade',
            is_highlight=True,
        )
        Product.objects.create(
            vendor=vendor_profile,
            category=cat,
            name='Bulk Cement',
            base_price=780,
            unit='bag',
            stock_quantity=100,
            reorder_level=10,
            status='ACTIVE',
        )

        url = reverse('product-list')
        response = api_client.get(url, {'certification': 'ISO 9001', 'inventory_signal': 'LOW_STOCK'})

        assert response.status_code == status.HTTP_200_OK
        names = [item['name'] for item in response.data['results']]
        assert 'Certified Cement' in names
        assert 'Bulk Cement' not in names

    def test_search_products_by_name_and_category_terms(self, api_client, vendor):
        vendor_profile = self.setup_vendor(vendor)
        cement = self.setup_category()
        steel = Category.objects.get_or_create(
            name="Steel",
            slug="steel",
            taxonomy_type='MATERIAL',
            active=True
        )[0]

        Product.objects.create(
            vendor=vendor_profile,
            category=cement,
            name="Simba 32.5R PPC",
            short_description="Reliable build material",
            base_price=650,
            unit="bag",
            stock_quantity=20,
            status='ACTIVE'
        )
        Product.objects.create(
            vendor=vendor_profile,
            category=steel,
            name="TMT Bar 12mm",
            short_description="High tensile reinforcement bar",
            base_price=1200,
            unit="pcs",
            stock_quantity=30,
            status='ACTIVE'
        )

        url = reverse('product-list')

        response = api_client.get(url, {'search': 'simba'})
        assert response.status_code == status.HTTP_200_OK
        names = [item['name'] for item in response.data['results']]
        assert 'Simba 32.5R PPC' in names
        assert 'TMT Bar 12mm' not in names

    def test_adjust_inventory_creates_movement(self, api_client, vendor):
        vendor_profile = self.setup_vendor(vendor)
        cat = self.setup_category()
        product = Product.objects.create(
            vendor=vendor_profile,
            category=cat,
            name='Inventory Cement',
            base_price=700,
            unit='bag',
            stock_quantity=12,
            reorder_level=5,
            status='ACTIVE',
        )

        api_client.force_authenticate(user=vendor)
        url = reverse('product-adjust-inventory', args=[product.uuid])
        response = api_client.post(url, {
            'quantity_delta': 8,
            'note': 'Warehouse recount',
            'reference': 'cycle-count-001',
        }, format='json')

        assert response.status_code == status.HTTP_200_OK
        product.refresh_from_db()
        assert product.stock_quantity == 20
        movement = ProductInventoryMovement.objects.get(product=product)
        assert movement.movement_type == ProductInventoryMovement.MovementType.MANUAL_ADJUSTMENT
        assert movement.quantity_before == 12
        assert movement.quantity_after == 20

    def test_inventory_history_returns_movements(self, api_client, vendor):
        vendor_profile = self.setup_vendor(vendor)
        cat = self.setup_category()
        product = Product.objects.create(
            vendor=vendor_profile,
            category=cat,
            name='Ledger Cement',
            base_price=640,
            unit='bag',
            stock_quantity=10,
            status='ACTIVE',
        )
        product.record_inventory_movement(
            movement_type=ProductInventoryMovement.MovementType.INITIAL,
            quantity_delta=10,
            quantity_before=0,
            quantity_after=10,
            actor=vendor,
            note='Initial stock load',
        )

        api_client.force_authenticate(user=vendor)
        url = reverse('product-inventory-history', args=[product.uuid])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        movement = response.data['results'][0]
        assert movement['movement_type'] == ProductInventoryMovement.MovementType.INITIAL

    def test_upload_images(self, api_client, vendor):
        v_profile = self.setup_vendor(vendor)
        cat = self.setup_category()
        product = Product.objects.create(
            vendor=v_profile, category=cat, name="P1", base_price=10, unit="u"
        )

        api_client.force_authenticate(user=vendor)
        url = reverse('product-upload-images', args=[product.uuid])

        image = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        response = api_client.post(url, {'images': [image]}, format='multipart')

        assert response.status_code == status.HTTP_201_CREATED
        assert product.images.count() == 1

    def test_import_products_csv(self, api_client, vendor):
        v_profile = self.setup_vendor(vendor)
        cat = self.setup_category() # Name is "Cement"

        api_client.force_authenticate(user=vendor)
        url = reverse('product-import-products')

        csv_content = "Name,Category,Price,Unit,Stock,Brand,Description\n"
        csv_content += "Steel Bar,Cement,1200,pcs,100,Alloy,Strong\n"

        file = SimpleUploadedFile("products.csv", csv_content.encode('utf-8'), content_type="text/csv")
        response = api_client.post(url, {'file': file}, format='multipart')

        assert response.status_code == status.HTTP_201_CREATED
        assert Product.objects.filter(name='Steel Bar').exists()

    def test_import_products_csv_with_minimal_fields_only(self, api_client, vendor):
        self.setup_vendor(vendor)
        self.setup_category()

        api_client.force_authenticate(user=vendor)
        url = reverse('product-import-products')

        csv_content = "Name,Description,Price,Unit\n"
        csv_content += "Quick Lime,Fast-setting binder,850,bag\n"

        file = SimpleUploadedFile("products-minimal.csv", csv_content.encode('utf-8'), content_type="text/csv")
        response = api_client.post(url, {'file': file}, format='multipart')

        assert response.status_code == status.HTTP_201_CREATED
        product = Product.objects.get(name='Quick Lime')
        assert product.description == 'Fast-setting binder'
        assert product.unit == 'bag'

    def test_download_template(self, api_client, project_owner):
        api_client.force_authenticate(user=project_owner)
        url = reverse('product-download-template')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response['Content-Type'] == 'text/csv'

    def test_upload_documents(self, api_client, vendor):
        v_profile = self.setup_vendor(vendor)
        cat = self.setup_category()
        product = Product.objects.create(vendor=v_profile, category=cat, name="P1", base_price=10, unit="u")

        api_client.force_authenticate(user=vendor)
        url = reverse('product-upload-documents', args=[product.uuid])

        document = SimpleUploadedFile("datasheet.pdf", b"pdf_content", content_type="application/pdf")
        response = api_client.post(
            url,
            {'documents': [document], 'document_type': ProductDocument.DocumentType.DATASHEET},
            format='multipart'
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert product.documents.count() == 1

    def test_set_primary_image(self, api_client, vendor):
        v_profile = self.setup_vendor(vendor)
        cat = self.setup_category()
        product = Product.objects.create(vendor=v_profile, category=cat, name="P1", base_price=10, unit="u")
        img1 = ProductImage.objects.create(product=product, image="img1.jpg", is_primary=False)
        img2 = ProductImage.objects.create(product=product, image="img2.jpg", is_primary=True)

        api_client.force_authenticate(user=vendor)
        url = reverse('product-image-set-primary', args=[img1.uuid])
        response = api_client.post(url)

        assert response.status_code == status.HTTP_200_OK
        img1.refresh_from_db()
        img2.refresh_from_db()
        assert img1.is_primary == True
        assert img2.is_primary == False
