from rest_framework import generics, status, views, permissions, viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer, UserSerializer, UserManagementSerializer, AddressSerializer, BuyerProfileSerializer
from .models import Address, BuyerProfile
from rbac.permissions import HasRequiredPermission

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            "token": token.key,
            "user": UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)

class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    def post(self, request):
        identity = request.data.get("email") # This could be username or email
        password = request.data.get("password")
        
        if not identity or not password:
            return Response({"error": "Please provide credentials"}, status=status.HTTP_400_BAD_REQUEST)
            
        # 1. Try authenticating as username
        user = authenticate(username=identity, password=password)
        
        # 2. If fails, try finding user by email and then authenticating by username
        if not user:
            from django.contrib.auth import get_user_model
            User_Model = get_user_model()
            try:
                user_obj = User_Model.objects.get(email=identity)
                user = authenticate(username=user_obj.username, password=password)
            except User_Model.DoesNotExist:
                pass
        
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "user": UserSerializer(user).data
            })
        
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

class UserManagementViewSet(viewsets.ModelViewSet):
    from django.contrib.auth import get_user_model
    from django.contrib.auth.models import Group
    User_Model = get_user_model()
    
    queryset = User_Model.objects.all()
    serializer_class = UserManagementSerializer
    permission_classes = [HasRequiredPermission]
    required_permission = 'users:view'
    permission_map = {
        'create': 'users:create',
        'update': 'users:update',
        'partial_update': 'users:update',
        'destroy': 'users:delete',
    }

    ROLE_GROUP_MAP = {
        'PROJECT_OWNER': 'PROJECT_OWNER',
        'CONTRACTOR': 'CONTRACTOR',
        'VENDOR': 'VENDOR',
        'INVESTOR': 'INVESTOR',
        'GOVERNMENT': 'GOVERNMENT_OWNER',
        'ADMIN': 'ADMIN'
    }

    def _sync_role_group(self, user):
        role = user.role
        group_name = self.ROLE_GROUP_MAP.get(role)
        if group_name:
            from django.contrib.auth.models import Group
            group, _ = Group.objects.get_or_create(name=group_name)
            user.groups.clear()
            user.groups.add(group)

    def perform_create(self, serializer):
        user = serializer.save()
        # Set a dummy password if not provided (should ideally be changed by user)
        if not user.password:
            user.set_password('temporary_pass_123')
            user.save()
        self._sync_role_group(user)

    def perform_update(self, serializer):
        user = serializer.save()
        if 'role' in serializer.validated_data:
            self._sync_role_group(user)

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        user_serializer = self.get_serializer(user, data=request.data, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        
        # Handle profile data
        profile_data = request.data.get('profile')
        if profile_data:
            profile = user.buyer_profile
            profile_serializer = BuyerProfileSerializer(profile, data=profile_data, partial=True)
            profile_serializer.is_valid(raise_exception=True)
            profile_serializer.save()
            
        return Response(UserSerializer(user).data)

class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # If is_default, unset others
        if serializer.validated_data.get('is_default'):
            Address.objects.filter(user=self.request.user).update(is_default=False)
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if serializer.validated_data.get('is_default'):
            Address.objects.filter(user=self.request.user).update(is_default=False)
        serializer.save()
