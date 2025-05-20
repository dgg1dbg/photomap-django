from rest_framework import serializers
from .model import Picture
from api.post.model import Post
from django.contrib.gis.geos import Point
from .cache import get_grid_key_from_point
from django.core.cache import cache

class FileOrPathField(serializers.Field):
    def to_internal_value(self, data):
        if hasattr(data, 'read'):
            return data
        elif isinstance(data, str):
            return data
        else:
            raise serializers.ValidationError("Must be a file or a file path string.")

    def to_representation(self, value):
        return str(value)


class PictureCreateRequestSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=True)
    longitude = serializers.FloatField(required=True)
    latitude = serializers.FloatField(required=True)
    description = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = Picture
        fields = ('longitude', 'latitude', 'description', 'file')
    

class PictureEditRequestSerializer(serializers.ModelSerializer):
    file = FileOrPathField(required=True)
    longitude = serializers.FloatField(required=True)
    latitude = serializers.FloatField(required=True)
    description = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = Picture
        fields = ('longitude', 'latitude', 'description', 'file')


    def validate(self, data):
        if not data.get('file') and not data.get('file_path'):
            raise serializers.ValidationError("Either 'file' or 'file_path' must be provided.")
        return data
    
    def update(self, instance, validated_data):
        point = Point(validated_data.get('longitude'), validated_data.get('latitude'))
        if instance.location != point:
            old_grid_key = get_grid_key_from_point(instance.location)
            new_grid_key = get_grid_key_from_point(point)
            cache.delete(old_grid_key)
            cache.delete(new_grid_key)
        instance.location = point
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
    
class PictureViewResponseSerializer(serializers.ModelSerializer):
    postId = serializers.IntegerField(source='post.id')
    longitude = serializers.SerializerMethodField()
    latitude = serializers.SerializerMethodField()
    description = serializers.CharField(required=False, allow_blank=True)
    def get_longitude(self, obj):
        return obj.location.x
    def get_latitude(self, obj):
        return obj.location.y
    class Meta:
        model = Picture
        fields = ('file_id', 'longitude', 'latitude', 'description', 'postId')