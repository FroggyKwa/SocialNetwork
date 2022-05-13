from django.contrib.auth.models import User
from rest_framework import serializers

from social_network.models import Profile, Post


class ProfileRetrieveUpdateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", required=False)
    username = serializers.CharField(source="user.username")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.CharField(source="user.email")
    last_login = serializers.DateTimeField(source="user.last_login")

    class Meta:
        model = Profile
        fields = [
            "user_id",
            "username",
            "first_name",
            "last_name",
            "email",
            "image",
            "last_login",
        ]
        read_only_fields = ["username"]

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        instance.save()
        return instance

    def get_image(self, obj):
        return obj.image if obj.image else "media/"


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileRetrieveUpdateSerializer(required=True)

    class Meta:
        model = User
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=True)
    name = serializers.CharField(max_length=64)
    description = serializers.CharField(max_length=512)
    picture_url = serializers.ImageField()
    thumbnail_url = serializers.ImageField()

    class Meta:
        model = Post
        fields = ["author", "name", "picture_url", "thumbnail_url"]
