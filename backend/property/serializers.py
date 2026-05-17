from rest_framework import serializers

from platform_settings.models import Country
from platform_settings.serializers import LocationSyncMixin
from platform_settings.utils import resolve_request_country_code

from .models import (
    PropertyListing,
    DevelopmentMetadata,
    PropertySpecification,
    PropertyFeature,
    PropertyMediaAsset,
    PropertyOwnershipProfile,
    PropertyPricingProfile,
    PropertyShowing,
    PropertyProjectLink,
    PropertyInquiry,
    PropertyAvailabilityWindow,
    PropertyAppointment,
)


class DevelopmentMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DevelopmentMetadata
        fields = '__all__'
        read_only_fields = ['property']


class PropertySpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertySpecification
        fields = '__all__'
        read_only_fields = ['property']


class PropertyFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyFeature
        fields = '__all__'
        read_only_fields = ['property']


class PropertyMediaAssetSerializer(serializers.ModelSerializer):
    media_url = serializers.SerializerMethodField()

    class Meta:
        model = PropertyMediaAsset
        fields = [
            'id',
            'property',
            'media_type',
            'file',
            'external_url',
            'media_url',
            'title',
            'caption',
            'alt_text',
            'sort_order',
            'is_primary',
            'is_public',
        ]
        read_only_fields = ['property']

    def get_media_url(self, obj):
        if obj.external_url:
            return obj.external_url
        if obj.file:
            try:
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(obj.file.url)
                return obj.file.url
            except ValueError:
                return ''
        return ''


class PropertyOwnershipProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyOwnershipProfile
        fields = '__all__'
        read_only_fields = ['property']


class PropertyPricingProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyPricingProfile
        fields = '__all__'
        read_only_fields = ['property']


class PropertyShowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyShowing
        fields = '__all__'
        read_only_fields = ['property']


class PropertyProjectLinkSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source='project.title', read_only=True)

    class Meta:
        model = PropertyProjectLink
        fields = ['id', 'project', 'project_title']


class PropertyInquirySerializer(serializers.ModelSerializer):
    property_title = serializers.CharField(source='property.title', read_only=True)
    chat_room_id = serializers.IntegerField(source='chat_room.id', read_only=True)

    class Meta:
        model = PropertyInquiry
        fields = '__all__'
        read_only_fields = ['property', 'inquirer_user', 'status', 'chat_room', 'created_at']

    def validate(self, attrs):
        if not attrs.get('email') and not attrs.get('phone_number'):
            raise serializers.ValidationError('Provide either an email or a phone number for follow-up.')
        return attrs


class PropertyAvailabilityWindowSerializer(serializers.ModelSerializer):
    property_title = serializers.CharField(source='property.title', read_only=True)

    class Meta:
        model = PropertyAvailabilityWindow
        fields = '__all__'
        read_only_fields = ['managed_by', 'created_at']

    def validate(self, attrs):
        if attrs['end_at'] <= attrs['start_at']:
            raise serializers.ValidationError('Availability end time must be after start time.')
        if attrs['slot_duration_minutes'] <= 0:
            raise serializers.ValidationError('Slot duration must be greater than zero.')
        return attrs


class PropertyAppointmentSerializer(serializers.ModelSerializer):
    property_title = serializers.CharField(source='property.title', read_only=True)
    chat_room_id = serializers.IntegerField(source='chat_room.id', read_only=True)

    class Meta:
        model = PropertyAppointment
        fields = '__all__'
        read_only_fields = ['visitor_user', 'created_by', 'chat_room', 'created_at']

    def validate(self, attrs):
        if not attrs.get('email') and not attrs.get('phone_number'):
            raise serializers.ValidationError('Provide either an email or a phone number for follow-up.')
        if attrs['scheduled_end'] <= attrs['scheduled_start']:
            raise serializers.ValidationError('Appointment end time must be after start time.')
        return attrs


class PropertyListingSerializer(LocationSyncMixin, serializers.ModelSerializer):
    owner_name = serializers.SerializerMethodField()
    manager_name = serializers.SerializerMethodField()
    location_display = serializers.SerializerMethodField()
    purpose_name = serializers.SerializerMethodField()
    purpose_slug = serializers.SerializerMethodField()
    development_metadata = DevelopmentMetadataSerializer(required=False)
    specification = PropertySpecificationSerializer(required=False)
    features = PropertyFeatureSerializer(many=True, required=False)
    media_assets = PropertyMediaAssetSerializer(many=True, required=False)
    ownership_profile = PropertyOwnershipProfileSerializer(required=False)
    pricing_profile = PropertyPricingProfileSerializer(required=False)
    showings = PropertyShowingSerializer(many=True, required=False)
    linked_projects = PropertyProjectLinkSerializer(many=True, read_only=True)
    open_slots = serializers.SerializerMethodField()
    primary_media = serializers.SerializerMethodField()
    highlighted_features = serializers.SerializerMethodField()

    class Meta:
        model = PropertyListing
        fields = '__all__'
        read_only_fields = ['owner', 'created_at', 'updated_at']

    def create(self, validated_data):
        development_metadata = validated_data.pop('development_metadata', None)
        specification = validated_data.pop('specification', None)
        features = validated_data.pop('features', [])
        media_assets = validated_data.pop('media_assets', [])
        ownership_profile = validated_data.pop('ownership_profile', None)
        pricing_profile = validated_data.pop('pricing_profile', None)
        showings = validated_data.pop('showings', [])
        request = self.context.get('request')
        if request and request.user and not validated_data.get('owner'):
            validated_data['owner'] = request.user
        if not validated_data.get('country'):
            country_code = resolve_request_country_code(request)
            selected_country = Country.objects.filter(iso_code__iexact=country_code, is_active=True).first()
            if selected_country is None:
                selected_country = Country.objects.filter(is_default=True, is_active=True).first()
            if selected_country:
                validated_data['country'] = selected_country
        prop = super().create(validated_data)
        self._sync_location_obj(prop, validated_data)
        self._save_nested(prop, development_metadata, specification, features, media_assets, ownership_profile, pricing_profile, showings)
        return prop

    def update(self, instance, validated_data):
        development_metadata = validated_data.pop('development_metadata', None)
        specification = validated_data.pop('specification', None)
        features = validated_data.pop('features', None)
        media_assets = validated_data.pop('media_assets', None)
        ownership_profile = validated_data.pop('ownership_profile', None)
        pricing_profile = validated_data.pop('pricing_profile', None)
        showings = validated_data.pop('showings', None)
        prop = super().update(instance, validated_data)
        self._sync_location_obj(prop, validated_data)
        self._save_nested(prop, development_metadata, specification, features, media_assets, ownership_profile, pricing_profile, showings)
        return prop

    def _save_nested(
        self,
        prop,
        development_metadata,
        specification,
        features,
        media_assets,
        ownership_profile,
        pricing_profile,
        showings,
    ):
        if development_metadata is not None:
            DevelopmentMetadata.objects.update_or_create(property=prop, defaults=development_metadata)
        if specification is not None:
            PropertySpecification.objects.update_or_create(property=prop, defaults=specification)
        if ownership_profile is not None:
            PropertyOwnershipProfile.objects.update_or_create(property=prop, defaults=ownership_profile)
        if pricing_profile is not None:
            PropertyPricingProfile.objects.update_or_create(property=prop, defaults=pricing_profile)
        if features is not None:
            prop.features.all().delete()
            PropertyFeature.objects.bulk_create([
                PropertyFeature(property=prop, **feature) for feature in features if feature.get('name')
            ])
        if media_assets is not None:
            prop.media_assets.all().delete()
            PropertyMediaAsset.objects.bulk_create([
                PropertyMediaAsset(property=prop, **asset) for asset in media_assets if asset.get('external_url') or asset.get('file') or asset.get('title')
            ])
        if showings is not None:
            prop.showings.all().delete()
            PropertyShowing.objects.bulk_create([
                PropertyShowing(property=prop, **showing) for showing in showings if showing.get('start_at') and showing.get('end_at')
            ])

    def get_owner_name(self, obj):
        if not obj.owner:
            return ''
        full_name = obj.owner.get_full_name()
        return full_name or obj.owner.username

    def get_manager_name(self, obj):
        if not obj.manager:
            return ''
        full_name = obj.manager.get_full_name()
        return full_name or obj.manager.username

    def get_location_display(self, obj):
        if obj.formatted_address:
            return obj.formatted_address
        if obj.location_text:
            return obj.location_text
        if obj.location:
            parts = [obj.location.name, obj.location.city, obj.location.state]
            return ', '.join(part for part in parts if part)
        return ''

    def get_purpose_name(self, obj):
        return obj.purpose.name if obj.purpose else ''

    def get_purpose_slug(self, obj):
        return obj.purpose.slug if obj.purpose else ''

    def get_open_slots(self, obj):
        windows = obj.availability_windows.filter(is_active=True).order_by('start_at')[:3]
        slots = []
        for window in windows:
            slots.append({
                'id': window.id,
                'start_at': window.start_at,
                'end_at': window.end_at,
                'slot_duration_minutes': window.slot_duration_minutes,
            })
        return slots

    def get_primary_media(self, obj):
        media = next((asset for asset in obj.media_assets.all() if asset.is_primary), None)
        if not media:
            media = next(iter(obj.media_assets.all()), None)
        if not media:
            return None
        return PropertyMediaAssetSerializer(media, context=self.context).data

    def get_highlighted_features(self, obj):
        highlighted = [feature for feature in obj.features.all() if feature.is_highlighted][:6]
        return PropertyFeatureSerializer(highlighted, many=True).data
