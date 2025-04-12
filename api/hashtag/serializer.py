from rest_framework import serializers
from .model import Hashtag

class HashtagResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ('name',)

class HashtagCreateRequestSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50, required=True)
    class Meta:
        model = Hashtag
        fields = ('name',)
    def create(self, validated_data):
        if Hashtag.objects.filter(name=validated_data['name']).exists():
                raise serializers.ValidationError("Hashtag already exists.")
        return Hashtag.objects.create(**validated_data)