from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..post.serializer import PostViewResponseSerializer

User = get_user_model()

class UserSignupRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'description')
    def create(self, validated_data):
        if User.objects.filter(username=validated_data['username']).exists():
            raise serializers.ValidationError("Username already exists.")
        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError("Email already exists.")
        return User.objects.create_user(**validated_data)

class UserSigninRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class UserEditRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'description')
    def update(self, instance, validated_data):
        if 'username' in validated_data and validated_data['username'] != instance.username:
            if User.objects.filter(username=validated_data['username']).exists():
                raise serializers.ValidationError("Username already exists.")
        instance.username = validated_data.get('username', instance.username)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

class UserDeleteRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username')

class UserViewResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'description')

class UserDetailViewResponseSerializer(serializers.ModelSerializer):
    posts = PostViewResponseSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'description', 'posts')
    

    
