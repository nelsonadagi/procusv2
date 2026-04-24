import pytest
from django.urls import reverse
from rest_framework import status
from taxonomy.models import Category

@pytest.mark.django_db
class TestTaxonomyAPI:
    def test_list_categories(self, api_client):
        Category.objects.create(name="Material", slug="material", taxonomy_type="MATERIAL", active=True)
        url = reverse('category-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        # Check if paginated or not
        data = response.data['results'] if 'results' in response.data else response.data
        assert len(data) >= 1

    def test_filter_categories(self, api_client):
        Category.objects.create(name="Concrete", slug="concrete", taxonomy_type="MATERIAL", active=True)
        Category.objects.create(name="Residential", slug="residential", taxonomy_type="PROJECT", active=True)
        
        url = reverse('category-list')
        response = api_client.get(url, {'taxonomy_type': 'MATERIAL'})
        assert response.status_code == status.HTTP_200_OK
        data = response.data['results'] if 'results' in response.data else response.data
        assert all(c['taxonomy_type'] == 'MATERIAL' for c in data)
        assert len(data) >= 1

    def test_list_categories_admin(self, api_client, admin_user):
        Category.objects.create(name="Inactive", slug="inactive", taxonomy_type="MATERIAL", active=False)
        api_client.force_authenticate(user=admin_user)
        url = reverse('category-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.data['results'] if 'results' in response.data else response.data
        assert any(c['name'] == 'Inactive' for c in data)

    def test_create_category_admin(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        url = reverse('category-list')
        data = {
            'name': 'New Category',
            'slug': 'new-cat',
            'taxonomy_type': 'MATERIAL',
            'active': True
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Category.objects.filter(name='New Category').exists()

    def test_tree_categories(self, api_client):
        parent = Category.objects.create(name="Parent", slug="parent", taxonomy_type="MATERIAL", active=True)
        Category.objects.create(name="Child", slug="child", taxonomy_type="MATERIAL", active=True, parent=parent)
        
        url = reverse('category-list')
        response = api_client.get(url, {'tree': 'true'})
        assert response.status_code == status.HTTP_200_OK
        data = response.data['results'] if 'results' in response.data else response.data
        assert len(data) == 1
        assert data[0]['name'] == 'Parent'
