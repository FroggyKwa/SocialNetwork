from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from social_network.models import Profile, Post


class ProfileRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "phone",
            "bio",
            "avatar",
            "avatar_thumbnail",
        ]

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        instance.save()
        return instance

    def get_image(self, obj):
        return obj.image


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileRetrieveSerializer(required=True)

    class Meta:
        model = User
        # fields = "__all__"
        exclude = ("password",)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=True)
    name = serializers.CharField(max_length=64)
    description = serializers.CharField(max_length=512)
    picture_url = serializers.ImageField()
    thumbnail_url = serializers.ImageField()

    class Meta:
        model = Post
        fields = ["author", "name", "picture_url", "thumbnail_url"]


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=128, write_only=True)
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )

    def validate(self, data):
        super().validate(data)
        email = data.get("email", None)
        print(email)
        if email and User.objects.filter(email__exact=email).exists():
            raise serializers.ValidationError("Email has already exists")
        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ("email", "username", "password")


class SignInSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    email = serializers.EmailField(max_length=128, read_only=True)

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        if username is None:
            raise serializers.ValidationError("An username is required to log in.")
        if password is None:
            raise serializers.ValidationError("A password is required to log in.")
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                "A user with this email and password was not found."
            )
        if not user.is_active:
            raise serializers.ValidationError("This user has been deactivated.")
        return UserSerializer(user).data
