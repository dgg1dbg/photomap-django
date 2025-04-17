from rest_framework import serializers
from api.post.model import Post
from ..picture.serializer import *

from ..hashtag.model import Hashtag
from ..hashtag.serializer import *
from django.core.files import File

class PostCreateRequestSerializer(serializers.ModelSerializer):
    pictures = PictureCreateRequestSerializer(many=True, required=False)
    hashtags = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = Post
        fields = ('name', 'date', 'time', 'description', 'pictures', 'hashtags')

    def create(self, validated_data):
        pictures_data = validated_data.pop('pictures', [])
        hashtag_str = validated_data.pop('hashtags', '')
        hashtag_data = hashtag_str[1:].split('#') if hashtag_str else []
        post = Post.objects.create(**validated_data, user=self.context['request'].user)
        for picture_data in pictures_data:
            Picture.objects.create_picture(post=post, **picture_data)
        if hashtag_data:
            for tag in hashtag_data:
                if tag:
                    hashtag, _ = Hashtag.objects.get_or_create(name=tag)
                    post.hashtags.add(hashtag)
        return post


class PostEditRequestSerializer(serializers.ModelSerializer):
    pictures = PictureEditRequestSerializer(many=True, required=False)
    hashtags = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = Post
        fields = ('name', 'date', 'time', 'description', 'pictures', 'hashtags')
    def update(self, instance, validated_data):
        pictures_data = validated_data.pop('pictures', [])
        hashtag_str = validated_data.pop('hashtags', '')
        hashtag_data = hashtag_str[1:].split('#') if hashtag_str else []
        instance.name = validated_data.get('name', instance.name)
        instance.date = validated_data.get('date', instance.date)
        instance.time = validated_data.get('time', instance.time)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        existing_picture_ids = set(p.id for p in instance.pictures.all())
        for picture_data in pictures_data:
            if isinstance(picture_data.get('file'), File):
                Picture.objects.create_picture(post=instance, **picture_data)
            else:
                picture_instance = Picture.objects.get_by_url(picture_data.get('file'))
                serializer = PictureEditRequestSerializer(picture_instance, data=picture_data)
                if picture_instance.id in existing_picture_ids:
                    existing_picture_ids.remove(picture_instance.id)
                if serializer.is_valid():
                    serializer.save()
                else:
                    raise serializers.ValidationError(serializer.errors)
        for picture in instance.pictures.filter(id__in=existing_picture_ids):
            Picture.objects.delete_picture(picture)
        instance.hashtags.clear()
        if hashtag_data:
            for tag in hashtag_data:
                if tag:
                    hashtag, _ = Hashtag.objects.get_or_create(name=tag)
                    instance.hashtags.add(hashtag)
        return instance


class PostViewResponseSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    date = serializers.DateField(required=False, allow_null=True)
    time = serializers.TimeField(required=False, allow_null=True)
    user = serializers.CharField(source='user.username')
    hashtag = serializers.SerializerMethodField()
    pictures = PictureViewResponseSerializer(many=True, required=False, allow_null=True)

    def get_hashtag(self, obj):
        return ''.join([f"#{tag.name}" for tag in obj.hashtags.all()])


class PostCreateResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Post
        fields = ('id',)