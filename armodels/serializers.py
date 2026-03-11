from rest_framework import serializers
from armodels.models import ARModel
import os

class ARModelSerializer(serializers.ModelSerializer):
    glb_url = serializers.SerializerMethodField()
    usdz_url = serializers.SerializerMethodField()
    poster_url = serializers.SerializerMethodField()

    class Meta:
        model = ARModel
        fields = ['id', 'name', 'glb_file', 'usdz_file', 'poster', 'glb_url', 'usdz_url', 'poster_url', 'created_at', 'share_url']
        read_only_fields = ['id', 'created_at', 'share_url']
        extra_kwargs = {
            'glb_file': {'write_only': True},
            'usdz_file': {'write_only': True},
            'poster': {'write_only': True, 'required': False}
        }

    def get_glb_url(self, obj):
        return obj.glb_file.url if obj.glb_file else None

    def get_usdz_url(self, obj):
        return obj.usdz_file.url if obj.usdz_file else None

    def get_poster_url(self, obj):
        return obj.poster.url if obj.poster else None

    def validate_glb_file(self, value):
        if not value.name.lower().endswith('.glb'):
            raise serializers.ValidationError("File must end with .glb")
        if value.size > 20 * 1024 * 1024:
            raise serializers.ValidationError("Max file size 20MB")
        return value

    def validate_usdz_file(self, value):
        if not value.name.lower().endswith('.usdz'):
            raise serializers.ValidationError("File must end with .usdz")
        if value.size > 20 * 1024 * 1024:
            raise serializers.ValidationError("Max file size 20MB")
        return value

    def validate_poster(self, value):
        if value and value.size > 20 * 1024 * 1024:
            raise serializers.ValidationError("Max file size 20MB")
        return value
