from rest_framework import serializers
from .models import ThrottledRequest

class ThrottledRequestSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = ThrottledRequest
        fields = ['id', 'ip_address', 'user', 'user_email', 'path', 'method', 'scope', 'timestamp']
