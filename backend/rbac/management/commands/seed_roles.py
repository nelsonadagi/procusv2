from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from rbac.permission_catalog import get_permission_catalog, get_role_permission_matrix

class Command(BaseCommand):
    help = 'Seed initial roles and permissions across all phases'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding comprehensive RBAC system...")
        permission_catalog = get_permission_catalog()
        role_matrix = get_role_permission_matrix()

        # Create Permissions
        content_type, _ = ContentType.objects.get_or_create(app_label='rbac', model='permission_logical')

        permissions_lookup = {}
        for definition in permission_catalog:
            perm, created = Permission.objects.get_or_create(
                codename=definition["codename"],
                content_type=content_type,
                defaults={"name": definition["name"]},
            )
            if not created and perm.name != definition["name"]:
                perm.name = definition["name"]
                perm.save(update_fields=["name"])
            permissions_lookup[definition["key"]] = perm
            if created:
                self.stdout.write(f"Created permission: {definition['codename']}")

        # Create Groups and Assign Permissions
        for role_name, perm_keys in role_matrix.items():
            group, created = Group.objects.get_or_create(name=role_name)
            
            perms_to_add = []
            for key in perm_keys:
                if key in permissions_lookup:
                    perms_to_add.append(permissions_lookup[key])
                else:
                    self.stdout.write(self.style.WARNING(f"Permission key {key} not found for role {role_name}"))
            
            group.permissions.set(perms_to_add)
            self.stdout.write(self.style.SUCCESS(f"Role {role_name} synchronized with {len(perms_to_add)} permissions."))

        User = get_user_model()
        synced_users = 0
        for user in User.objects.all().iterator():
            user.sync_groups()
            synced_users += 1

        self.stdout.write(self.style.SUCCESS(f"Synchronized RBAC groups for {synced_users} existing users."))
        self.stdout.write(self.style.SUCCESS("RBAC Seeding complete."))
