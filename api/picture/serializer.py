from rest_framework import serializers
from .model import Picture
from api.post.model import Post

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
    class Meta:
        model = Picture
        fields = ('longitude', 'latitude', 'description', 'file')
    

class PictureEditRequestSerializer(serializers.ModelSerializer):
    file = FileOrPathField(required=True)
    class Meta:
        model = Picture
        fields = ('longitude', 'latitude', 'description', 'file')


    def validate(self, data):
        if not data.get('file') and not data.get('file_path'):
            raise serializers.ValidationError("Either 'file' or 'file_path' must be provided.")
        return data
    
    def update(self, instance, validated_data):
        instance.longitude = validated_data.get('longitude', instance.longitude)
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
    
class PictureViewResponseSerializer(serializers.ModelSerializer):
    postId = serializers.IntegerField(source='post.id')
    class Meta:
        model = Picture
        fields = ('fileDir', 'longitude', 'latitude', 'description', 'postId')