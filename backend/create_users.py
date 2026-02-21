import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_users():
    users_to_create = [
        ('owner_jane', 'owner_jane@ujenzi.com', 'PROJECT_OWNER', 'Jane', 'Owner'),
        ('vendor_mall', 'vendor_mall@ujenzi.com', 'VENDOR', 'Mall', 'Supplier'),
        ('contractor_expert', 'contractor_expert@ujenzi.com', 'CONTRACTOR', 'Expert', 'Builder'),
        ('investor_wealth', 'investor_wealth@ujenzi.com', 'INVESTOR', 'Wealth', 'Capital'),
        ('gov_authority', 'gov_authority@ujenzi.com', 'GOVERNMENT', 'Gov', 'Official'),
        ('admin_plus', 'admin_plus@ujenzi.com', 'ADMIN', 'Plus', 'Admin'),
    ]

    password = 'Starten1@'

    print("--- Creating/Updating Users ---")
    for username, email, role, first_name, last_name in users_to_create:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'role': role,
                'first_name': first_name,
                'last_name': last_name,
            }
        )
        user.set_password(password)
        user.save()
        status = "Created" if created else "Updated password for"
        print(f"✅ {status} {username} (Role: {role})")

    print("\nAll users are set with password: " + password)

if __name__ == '__main__':
    create_users()
