from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Organization(models.Model):
    name = models.CharField(max_length=255, verbose_name="Organization Name")
    slug = models.SlugField(unique=True, verbose_name="URL Slug")
    description = models.TextField(blank=True, verbose_name="About Organization")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")

    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

    def __str__(self):
        return self.name


class User(AbstractUser):
    class Role(models.TextChoices):
        PROJECT_OWNER = 'PROJECT_OWNER', _('Project Owner / Client')
        VENDOR = 'VENDOR', _('Material Supplier')
        CONTRACTOR = 'CONTRACTOR', _('Construction Professional')
        INVESTOR = 'INVESTOR', _('Project Investor')
        PROPERTY_MANAGER = 'PROPERTY_MANAGER', _('Property Manager')
        GOVERNMENT = 'GOVERNMENT', _('Government Agency')
        COURIER = 'COURIER', _('Logistics Partner')
        ADMIN = 'ADMIN', _('System Administrator')

    organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='members',
        verbose_name="Organization"
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.PROJECT_OWNER,
        verbose_name="Account Type"
    )
    roles = models.JSONField(
        default=list,
        blank=True,
        help_text=_("Additional roles assigned to the user"),
        verbose_name="Additional Roles"
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name="Phone Number")
    bio = models.TextField(blank=True, verbose_name="About Me")
    location = models.ForeignKey(
        'platform_settings.Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
        verbose_name="Primary Location"
    )

    class Meta:
        verbose_name = "User Account"
        verbose_name_plural = "User Accounts"

    @property
    def buyer_profile(self):
        profile, created = BuyerProfile.objects.get_or_create(user=self)
        return profile

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    def has_role(self, role):
        if self.role == self.Role.ADMIN:
            return True
        if self.role == role:
            return True
        return role in (self.roles or [])

    def grant_role(self, role, make_primary=False):
        if role == self.Role.ADMIN:
            self.role = self.Role.ADMIN
            self.roles = []
            self.is_staff = True
            self.save(update_fields=['role', 'roles', 'is_staff'])
            return

        if self.role == self.Role.ADMIN:
            return

        if make_primary:
            if self.role and self.role != role and self.role != self.Role.ADMIN:
                secondary_roles = list(self.roles or [])
                if self.role not in secondary_roles:
                    secondary_roles.append(self.role)
                self.roles = [r for r in secondary_roles if r != role]
            self.role = role
        else:
            secondary_roles = list(self.roles or [])
            if role != self.role and role not in secondary_roles:
                secondary_roles.append(role)
            self.roles = secondary_roles

        self.is_staff = False
        self.save(update_fields=['role', 'roles', 'is_staff'])

    def revoke_role(self, role):
        if role == self.Role.ADMIN:
            return
        if self.role == role:
            fallback_roles = [r for r in (self.roles or []) if r != role]
            if fallback_roles:
                self.role = fallback_roles[0]
                self.roles = fallback_roles[1:]
            else:
                self.role = self.Role.PROJECT_OWNER
                self.roles = []
            self.save(update_fields=['role', 'roles'])
            return

        secondary_roles = [r for r in (self.roles or []) if r != role]
        self.roles = secondary_roles
        self.save(update_fields=['roles'])

    def sync_groups(self):
        """Syncs Django Groups with the roles assigned to the user."""
        from django.contrib.auth.models import Group

        # Primary role mapping
        role_map = {
            'PROJECT_OWNER': 'PROJECT_OWNER',
            'CONTRACTOR': 'CONTRACTOR',
            'VENDOR': 'VENDOR',
            'INVESTOR': 'INVESTOR',
            'PROPERTY_MANAGER': 'PROPERTY_MANAGER',
            'GOVERNMENT': 'GOVERNMENT',
            'COURIER': 'COURIER',
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
    class HubType(models.TextChoices):
        CONSTRUCTION_SITE = 'SITE', _('🏗️ Construction Site')
        WAREHOUSE = 'WAREHOUSE', _('📦 Warehouse / Depot')
        OPERATIONAL_OFFICE = 'OFFICE', _('🏢 Office / Worksite')
        RETAIL_POINT = 'RETAIL', _('🛒 Retail Store')
        RESIDENTIAL = 'RESIDENTIAL', _('🏠 Home / Residential')

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='addresses',
        verbose_name="Belongs To"
    )
    name = models.CharField(
        max_length=100,
        help_text=_("Give this address a name, e.g. 'Site Alpha', 'Home Office'"),
        verbose_name="Address Name"
    )
    hub_type = models.CharField(
        max_length=20,
        choices=HubType.choices,
        default=HubType.CONSTRUCTION_SITE,
        verbose_name="Location Type"
    )

    address_line_1 = models.CharField(max_length=255, verbose_name="Street Address")
    address_line_2 = models.CharField(max_length=255, blank=True, verbose_name="Apartment, Suite, Floor")
    city = models.CharField(max_length=100, verbose_name="City / Town")
    state_province = models.CharField(max_length=100, blank=True, verbose_name="State / Province / County")
    postal_code = models.CharField(max_length=20, blank=True, verbose_name="Postal / ZIP Code")
    country = models.CharField(max_length=100, default='Kenya', verbose_name="Country")

    # Geospatial data for Interspacial Lock
    latitude = models.DecimalField(
        max_digits=12,
        decimal_places=9,
        null=True,
        blank=True,
        verbose_name="GPS Latitude"
    )
    longitude = models.DecimalField(
        max_digits=12,
        decimal_places=9,
        null=True,
        blank=True,
        verbose_name="GPS Longitude"
    )

    is_default = models.BooleanField(default=False, verbose_name="Set as Default Address")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Added On")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    class Meta:
        verbose_name = "Delivery Address"
        verbose_name_plural = "Delivery Addresses"

    def __str__(self):
        return f"{self.name}: {self.address_line_1}, {self.city}"


class BuyerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name="User"
    )
    preferred_region = models.CharField(max_length=100, blank=True, verbose_name="Preferred Delivery Region")
    delivery_instructions = models.TextField(
        blank=True,
        verbose_name="Special Delivery Instructions",
        help_text="Any notes for delivery drivers, e.g. 'Gate code: 1234'"
    )

    class Meta:
        verbose_name = "Buyer Preferences"
        verbose_name_plural = "Buyer Preferences"

    def __str__(self):
        return f"Profile - {self.user.username}"
