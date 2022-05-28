from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from social_network.models import Profile, Post


class ProfileRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "phone",
            "bio",
            "age",
            "avatar",
            "avatar_thumbnail",
        ]


class ProfileUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        allow_blank=True, allow_null=True, required=False, default=None
    )
    email = serializers.EmailField(
        allow_blank=True,
        required=False,
    )
    first_name = serializers.CharField(
        allow_blank=True, allow_null=True, required=False, default=None
    )
    last_name = serializers.CharField(
        allow_blank=True, allow_null=True, required=False, default=None
    )
    phone = serializers.CharField(
        allow_blank=True, allow_null=True, required=False, default=None
    )
    age = serializers.IntegerField(allow_null=True, required=False, default=None)
    bio = serializers.CharField(
        allow_blank=True, allow_null=True, required=False, default=None
    )
    is_hidden = serializers.BooleanField(allow_null=True, required=False, default=None)
    avatar = serializers.ImageField(allow_null=True, default=None)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "age",
            "bio",
            "avatar",
            "is_hidden",
        ]

    def update(self, instance, validated_data):
        filtered = {
            k: v for k, v in dict(validated_data).items() if v or k == "is_hidden"
        }
        print(filtered)
        instance.username = filtered.get("username", instance.username)
        instance.first_name = filtered.get("first_name", instance.first_name)
        instance.last_name = filtered.get("last_name", instance.last_name)
        instance.email = filtered.get("email", instance.email)
        instance.profile.age = filtered.get("age", instance.profile.age)
        instance.profile.bio = filtered.get("bio", instance.profile.bio)
        instance.profile.phone = filtered.get("phone", instance.profile.phone)
        instance.profile.avatar = filtered.get("avatar", instance.profile.avatar)
        instance.profile.is_hidden = filtered.get(
            "is_hidden", instance.profile.is_hidden
        )
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileRetrieveSerializer(required=True)

    class Meta:
        model = User
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
    author = UserSerializer()
    name = serializers.CharField(max_length=64)
    description = serializers.CharField(max_length=512)
    picture_url = serializers.ImageField()
    thumbnail_url = serializers.ImageField()

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "name",
            "description",
            "picture_url",
            "thumbnail_url",
            "rating",
        ]


class PostUploadSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField()
    name = serializers.CharField(max_length=64)
    description = serializers.CharField(max_length=512, allow_blank=True)
    picture_url = serializers.ImageField()

    class Meta:
        model = Post
        fields = ("author_id", "name", "description", "picture_url")

    def create(self, validated_data):
        return Post.objects.create(**validated_data)


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


class PostLikeSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    def validate(self, data):
        post_id = data.get("post_id", None)
        liker_id = data.get("user_id", None)
        if not post_id:
            return serializers.ValidationError("Post id is required")
        if not liker_id:
            return serializers.ValidationError("User id is required")
        return data

    def save(self, **kwargs):
        post_id = self.validated_data.get("post_id", None)
        liker_id = self.validated_data.get("user_id", None)
        post = get_object_or_404(Post, id=post_id)
        user = get_object_or_404(User, id=liker_id)
        if user in set(post.likes.all()):
            raise serializers.ValidationError("User has already liked the post.")
        if user in set(post.dislikes.all()):
            post.dislikes.remove(user)
        post.likes.add(user)
        return post


class PostDislikeSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    def validate(self, data):
        post_id = data.get("post_id", None)
        disliker_id = data.get("user_id", None)
        if not post_id:
            return serializers.ValidationError("Post id is required")
        if not disliker_id:
            return serializers.ValidationError("User id is required")
        return data

    def save(self, **kwargs):
        post_id = self.validated_data.get("post_id", None)
        disliker_id = self.validated_data.get("user_id", None)
        post = get_object_or_404(Post, pk=post_id)
        user = get_object_or_404(User, pk=disliker_id)
        if user in set(post.dislikes.all()):
            raise serializers.ValidationError("User has already disliked the post.")
        if user in set(post.likes.all()):
            post.likes.remove(user)
        post.dislikes.add(user)
        post.save()
        return post


class SubscribeSerializer(serializers.Serializer):
    from_id = serializers.IntegerField(required=False)
    to_id = serializers.IntegerField(required=False)

    def validate(self, data):
        from_id = data.get("from_id")
        to_id = data.get("to_id")
        if not to_id or not from_id:
            raise serializers.ValidationError("No data provided.")
        return data

    def save(self, **kwargs):
        from_id = self.validated_data.get("from_id")
        to_id = self.validated_data.get("to_id")

        subscribe_from = get_object_or_404(User, pk=from_id)
        subscribe_to = get_object_or_404(User, pk=to_id)
        if subscribe_from.profile in subscribe_to.subscribers.all():
            subscribe_to.subscribers.remove(subscribe_from.profile)
            return {"Success": "Subscribe"}
        else:
            subscribe_to.subscribers.add(subscribe_from.profile)
            return {"Success": "Unsubscribe"}
