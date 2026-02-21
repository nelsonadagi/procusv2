from django.contrib.auth.models import AbstractUser
from django.db import models

class Organization(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    class Role(models.TextChoices):
        PROJECT_OWNER = 'PROJECT_OWNER', 'Project Owner'
        VENDOR = 'VENDOR', 'Vendor'
        CONTRACTOR = 'CONTRACTOR', 'Contractor'
        INVESTOR = 'INVESTOR', 'Investor'
        GOVERNMENT = 'GOVERNMENT', 'Government'
        ADMIN = 'ADMIN', 'Admin'

    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.PROJECT_OWNER)
    roles = models.JSONField(default=list, blank=True, help_text="List of roles assigned to the user")
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)

    @property
    def buyer_profile(self):
        profile, created = BuyerProfile.objects.get_or_create(user=self)
        return profile

    def __str__(self):
        return f"{self.username} ({self.role})"

    def sync_groups(self):
        """Syncs Django Groups with the roles assigned to the user."""
        from django.contrib.auth.models import Group
        
        # Primary role mapping
        role_map = {
            'PROJECT_OWNER': 'PROJECT_OWNER',
            'CONTRACTOR': 'CONTRACTOR',
            'VENDOR': 'VENDOR',
            'INVESTOR': 'INVESTOR',
            'GOVERNMENT': 'GOVERNMENT_OWNER',
            'ADMIN': 'ADMIN'
        }
        
        target_groups = set()
        
        # Add primary role
        primary_group = role_map.get(self.role)
        if primary_group:
            target_groups.add(primary_group)
            
        # Add secondary roles
        if isinstance(self.roles, list):
            for r in self.roles:
                g = role_map.get(r)
                if g:
                    target_groups.add(g)
        
        # Superuser always gets ADMIN group for permissions
        if self.is_superuser:
            target_groups.add('ADMIN')

        # Get or create necessary groups and set them
        group_objs = []
        for g_name in target_groups:
            group, _ = Group.objects.get_or_create(name=g_name)
            group_objs.append(group)
            
        self.groups.set(group_objs)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        # Sync groups after save (needed for M2M)
        # Note: In some race conditions or specific transactions this might be tricky, 
        # but for Django standard save() it works well for syncing groups.
        self.sync_groups()

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    name = models.CharField(max_length=100, help_text="e.g. Home, Office, Site A")
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}: {self.address_line_1}, {self.city}"

class BuyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    preferred_region = models.CharField(max_length=100, blank=True)
    delivery_instructions = models.TextField(blank=True)
    
    def __str__(self):
        return f"Profile - {self.user.username}"
