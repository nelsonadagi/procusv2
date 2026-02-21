from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'role', 'first_name', 'last_name')
        extra_kwargs = {
            'username': {'required': False}, # We'll set it to email if missing
            'role': {'required': False}  # Optional, defaults to PROJECT_OWNER
        }

    def create(self, validated_data):
        if 'username' not in validated_data:
            validated_data['username'] = validated_data['email']
            
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'PROJECT_OWNER'),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

from accounts.models import Address, BuyerProfile

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'name', 'address_line_1', 'address_line_2', 'city', 'state_province', 'postal_code', 'country', 'is_default')

class BuyerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerProfile
        fields = ('preferred_region', 'delivery_instructions')

class UserSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()
    groups = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    profile = BuyerProfileSerializer(read_only=True)
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'role', 'roles', 'first_name', 'last_name', 'permissions', 'groups', 'profile', 'addresses', 'phone', 'bio')
        read_only_fields = ('email', 'username', 'permissions', 'groups')  # role and roles are editable

    def get_permissions(self, obj):
        try:
            # Return logical permissions 'ns:action'
            perms = obj.get_all_permissions()
            # Filter only logical ones we created under 'rbac' app
            logical_perms = []
            for p in perms:
                if p.startswith('rbac.'):
                    # rbac.contracts_post_contract -> contracts:post_contract
                    raw = p.split('.')[1]
                    logical_perms.append(raw.replace('_', ':', 1))
            return logical_perms
        except Exception as e:
            import traceback
            print("ERROR IN GET_PERMISSIONS:")
            traceback.print_exc()
            return []

class UserManagementSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'role', 'first_name', 'last_name', 'is_active', 'password')
        extra_kwargs = {
            'username': {'required': False},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', 'temporary_pass_123')
        if 'username' not in validated_data:
            validated_data['username'] = validated_data['email']
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
