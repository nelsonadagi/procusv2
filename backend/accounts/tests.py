import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from accounts.models import Address

User = get_user_model()

@pytest.mark.django_db
class TestAccountsAPI:
    def test_register(self, api_client):
        url = reverse('register')
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'password123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'token' in response.data
        assert User.objects.filter(username='newuser').exists()
        assert response.data['user']['role'] == 'PROJECT_OWNER'

    def test_register_ignores_role_override(self, api_client):
        url = reverse('register')
        data = {
            'username': 'forcedrole',
            'email': 'forced@example.com',
            'password': 'password123',
            'first_name': 'Forced',
            'last_name': 'Role',
            'role': 'ADMIN'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['user']['role'] == 'PROJECT_OWNER'

    def test_login(self, api_client):
        user = User.objects.create_user(username='testlogin', password='password123', email='test@example.com')
        url = reverse('login')
        
        # Test by email
        response = api_client.post(url, {'email': 'test@example.com', 'password': 'password123'})
        assert response.status_code == status.HTTP_200_OK
        assert 'token' in response.data
        
        # Test by username
        response = api_client.post(url, {'email': 'testlogin', 'password': 'password123'})
        assert response.status_code == status.HTTP_200_OK

    def test_profile_update(self, api_client, project_owner):
        api_client.force_authenticate(user=project_owner)
        url = reverse('profile')
        data = {'first_name': 'UpdatedName'}
        response = api_client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        project_owner.refresh_from_db()
        assert project_owner.first_name == 'UpdatedName'

    def test_address_management(self, api_client, project_owner):
        api_client.force_authenticate(user=project_owner)
        url = reverse('addresses-list')
        data = {
            'name': 'Home',
            'address_line_1': '123 Street',
            'city': 'Nairobi',
            'state_province': 'Nairobi',
            'postal_code': '00100',
            'country': 'Kenya',
            'is_default': True
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED, f"Error: {response.data}"
        assert project_owner.addresses.filter(name='Home').exists()
        
    def test_login_invalid(self, api_client):
        url = reverse('login')
        response = api_client.post(url, {'email': 'wrong@ex.com', 'password': 'pass'})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_management_list_admin(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        url = reverse('user-management-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_profile_update_buyer_data(self, api_client, project_owner):
        api_client.force_authenticate(user=project_owner)
        url = reverse('profile')
        data = {
            'first_name': 'Buyer',
            'profile': {
                'preferred_region': 'Nairobi',
                'delivery_instructions': 'Leave at gate'
            }
        }
        response = api_client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        project_owner.refresh_from_db()
        assert project_owner.profile.preferred_region == 'Nairobi'

    def test_management_create_user(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        url = reverse('user-management-list')
        data = {
            'email': 'managed@ex.com',
            'username': 'managed',
            'role': 'VENDOR',
            'first_name': 'Managed',
            'last_name': 'Vendor'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        user = User.objects.get(email='managed@ex.com')
        assert user.groups.filter(name='VENDOR').exists()
        assert user.check_password('temporary_pass_123')
