from rest_framework import serializers

from taxonomy.models import Category
from taxonomy.serializers import CategorySerializer

from milestones.serializers import MilestoneSerializer

from .models import Contract, ContractAttachment


class ContractAttachmentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    attachment_type_label = serializers.CharField(source='get_attachment_type_display', read_only=True)

    class Meta:
        model = ContractAttachment
        fields = [
            'id',
            'contract',
            'file',
            'file_url',
            'attachment_type',
            'attachment_type_label',
            'title',
            'uploaded_at',
        ]
        read_only_fields = ['contract', 'file_url', 'attachment_type_label', 'uploaded_at']

    def get_file_url(self, obj):
        if not obj.file:
            return ''
        try:
            return obj.file.url
        except ValueError:
            return ''


class ContractSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    milestones = MilestoneSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    category_uuid = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    country_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    featured_image_url = serializers.SerializerMethodField()
    attachments = ContractAttachmentSerializer(many=True, read_only=True)
    linked_project = serializers.SerializerMethodField()

    class Meta:
        model = Contract
        fields = [
            'id',
            'owner',
            'owner_username',
            'title',
            'description_scope',
            'location',
            'country',
            'country_id',
            'budget_min',
            'budget_max',
            'currency',
            'status',
            'bid_deadline',
            'project_start_date',
            'project_end_date',
            'category',
            'category_uuid',
            'featured_image',
            'featured_image_url',
            'payment_terms',
            'eligibility_criteria',
            'linked_project',
            'created_at',
            'milestones',
            'attachments',
        ]
        read_only_fields = [
            'owner',
            'status',
            'created_at',
            'owner_username',
            'featured_image_url',
            'category',
            'linked_project',
            'milestones',
            'attachments',
        ]

    def get_featured_image_url(self, obj):
        if not obj.featured_image:
            return ''
        try:
            return obj.featured_image.url
        except ValueError:
            return ''

    def get_linked_project(self, obj):
        link = obj.linked_project.select_related('project', 'project__owner').first()
        if not link:
          return None
        project = link.project
        return {
            'id': project.id,
            'title': project.title,
            'owner': project.owner_id,
            'owner_username': project.owner.username,
        }

    def _resolve_category(self, validated_data):
        category_uuid = validated_data.pop('category_uuid', None)
        if category_uuid is None:
            if 'category_uuid' in self.initial_data and self.initial_data.get('category_uuid') in {'', None}:
                validated_data['category'] = None
            return validated_data

        try:
            validated_data['category'] = Category.objects.get(uuid=category_uuid)
        except Category.DoesNotExist as exc:
            raise serializers.ValidationError({'category_uuid': 'Selected category does not exist.'}) from exc
        return validated_data

    def create(self, validated_data):
        validated_data = self._resolve_category(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data = self._resolve_category(validated_data)
        return super().update(instance, validated_data)
