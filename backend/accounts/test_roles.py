import pytest
from django.contrib.auth.models import Group
from accounts.models import User

@pytest.mark.django_db
class TestUserRoles:
    def test_user_sync_groups_on_save(self, user_factory):
        # Create a user with contractor role
        user = user_factory(role=User.Role.CONTRACTOR)
        
        # Check if the 'CONTRACTOR' group exists and user is in it
        groups = [g.name for g in user.groups.all()]
        assert 'CONTRACTOR' in groups
        assert 'ADMIN' not in groups

    def test_admin_sync_groups(self, user_factory):
        # Create an admin user
        user = user_factory(role=User.Role.ADMIN, is_superuser=True)
        
        groups = [g.name for g in user.groups.all()]
        assert 'ADMIN' in groups

    def test_role_update_syncs_groups(self, user_factory):
        user = user_factory(role=User.Role.VENDOR)
        assert 'VENDOR' in [g.name for g in user.groups.all()]
        
        # Change role to VENDOR and save
        user.role = User.Role.INVESTOR
        user.save()
        
        groups = [g.name for g in user.groups.all()]
        assert 'INVESTOR' in groups
        assert 'VENDOR' not in groups

    def test_grant_role_adds_secondary_group(self, user_factory):
        user = user_factory(role=User.Role.PROJECT_OWNER)
        user.grant_role(User.Role.VENDOR)

        user.refresh_from_db()
        groups = [g.name for g in user.groups.all()]
        assert user.role == User.Role.PROJECT_OWNER
        assert User.Role.VENDOR in user.roles
        assert 'PROJECT_OWNER' in groups
        assert 'VENDOR' in groups

    def test_grant_role_admin_clears_secondary_roles(self, user_factory):
        user = user_factory(role=User.Role.PROJECT_OWNER, roles=[User.Role.VENDOR])
        user.grant_role(User.Role.ADMIN)

        user.refresh_from_db()
        groups = [g.name for g in user.groups.all()]
        assert user.role == User.Role.ADMIN
        assert user.roles == []
        assert user.is_staff is True
        assert 'ADMIN' in groups

    def test_government_role_syncs_to_government_group(self, user_factory):
        user = user_factory(role=User.Role.GOVERNMENT)

        groups = [g.name for g in user.groups.all()]
        assert 'GOVERNMENT' in groups
        assert 'GOVERNMENT_OWNER' not in groups
