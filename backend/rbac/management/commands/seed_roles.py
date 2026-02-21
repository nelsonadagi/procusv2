from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Seed initial roles and permissions across all phases'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding comprehensive RBAC system...")

        # Definition of permission namespaces and their associated logical names
        # Format: (namespace, [actions])
        namespaces = {
            'catalog': ['view', 'create', 'update', 'delete', 'manage_stock'],
            'orders': ['view', 'create', 'update', 'cancel', 'process'],
            'contracts': ['view', 'post_contract', 'award_contract', 'manage_milestones'],
            'bids': ['view', 'submit_bid', 'withdraw_bid', 'award_bid'],
            'escrow': ['view', 'release_funds', 'refund_funds', 'dispute_funds'],
            'finance': ['view', 'apply', 'approve_loan', 'disburse'],
            'disputes': ['view', 'raise_dispute', 'arbitrate_dispute', 'close_dispute'],
            'projects': ['view', 'create_project', 'update_project', 'delete_project'],
            'property': ['view', 'list_property', 'update_property'],
            'investments': ['view', 'pledge', 'sign_agreement', 'transfer_stake'],
            'enterprise': ['view', 'request_approval', 'approve_request', 'manage_org'],
            'government': ['view', 'publish_tender', 'audit_tender'],
            'milestones': ['view', 'manage_milestones'],
            'compliance': ['view', 'verify_kyc', 'report_aml'],
            'risk': ['view', 'manage_ai_rules', 'view_anomaly'],
            'banking': ['view', 'reconcile', 'settle'],
            'integrations': ['view', 'manage_api_keys', 'sync_erp'],
            'users': ['view', 'create', 'update', 'delete', 'manage_roles'],
        }

        # Roles (Groups) and their permission bundles
        role_matrix = {
            'GUEST': ['catalog:view', 'contracts:view', 'projects:view', 'government:view'],
            
            'BUYER': [
                'catalog:view', 'orders:create', 'orders:view', 
                'contracts:view', 'projects:view'
            ],
            
            'VENDOR': [
                'catalog:create', 'catalog:update', 'catalog:view', 'catalog:manage_stock',
                'orders:view', 'orders:process'
            ],
            
            'CONTRACTOR': [
                'contracts:view', 'contracts:post_contract', 'bids:submit_bid', 'bids:view', 
                'milestones:view', 'disputes:raise_dispute'
            ],
            
            'PROJECT_OWNER': [
                'contracts:post_contract', 'contracts:award_contract', 'contracts:view',
                'projects:create_project', 'projects:update_project', 'projects:view',
                'bids:view', 'escrow:release_funds', 'milestones:manage_milestones'
            ],
            
            'INVESTOR': [
                'projects:view', 'investments:view', 'investments:pledge', 
                'investments:sign_agreement', 'compliance:view'
            ],
            
            'VERIFIED_INVESTOR': [
                'projects:view', 'investments:view', 'investments:pledge', 
                'investments:sign_agreement', 'investments:transfer_stake', 
                'compliance:view'
            ],
            
            'GOVERNMENT_OWNER': [
                'government:publish_tender', 'government:view', 'government:audit_tender'
            ],
            
            'GOVERNMENT_AUDITOR': [
                'government:view', 'government:audit_tender', 'compliance:view'
            ],
            
            'ADMIN': [f"{ns}:{action}" for ns, actions in namespaces.items() for action in actions],
        }

        # Create Permissions
        # Since we use logical namespaces, we'll create them under a dummy ContentType if real ones aren't available,
        # but for production quality, we should map them to actual models where possible.
        # For simplicity in this logical enforcement, we'll use a unified ContentType "rbac"
        content_type, _ = ContentType.objects.get_or_create(app_label='rbac', model='permission_logical')

        permissions_lookup = {}
        for ns, actions in namespaces.items():
            for action in actions:
                codename = f"{ns}_{action}"
                name = f"Can {action} in {ns}"
                perm, created = Permission.objects.get_or_create(
                    codename=codename,
                    name=name,
                    content_type=content_type,
                )
                permissions_lookup[f"{ns}:{action}"] = perm
                if created:
                    self.stdout.write(f"Created permission: {codename}")

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

        self.stdout.write(self.style.SUCCESS("RBAC Seeding complete."))
