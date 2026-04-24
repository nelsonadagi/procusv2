from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='uuid', read_only=True)
    parent = serializers.UUIDField(source='parent.uuid', read_only=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "taxonomy_type", "parent", "children"]

    def get_children(self, obj):
        # Only return children if this is a parent category (or recursivly)
        if obj.children.exists():
            return CategorySerializer(obj.children.all(), many=True).data
        return []
