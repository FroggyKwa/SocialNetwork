from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import (
    RetrieveUpdateAPIView,
    get_object_or_404,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.db_methods.post_methods import get_feed_for_user

from api.serializers import (
    SignUpSerializer,
    SignInSerializer,
    UserSerializer,
    PostUploadSerializer,
    PostSerializer,
    PostLikeSerializer,
    PostDislikeSerializer,
    ProfileUpdateSerializer,
    SubscribeSerializer,
)
from social_network.forms import LoginForm
from social_network.models import Post


class PostUploadView(APIView):
    permission_classes = [
        AllowAny,
    ]
    serializer_class = PostUploadSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save()
        return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)


class SignUpAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class LogInApiView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SignInSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    lookup_field = "username"

    def retrieve(self, request, username, *args, **kwargs):
        user = get_object_or_404(User, username=username)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserUpdateAPIView(UpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProfileUpdateSerializer

    def update(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=request.data["user_id"])
        data = {}
        for k, v in dict(request.data).items():
            data[k] = v[0] if v is not None else None
        data = dict(data, **{"avatar": request.FILES.get("avatar", None)})
        serializer = self.serializer_class(
            user,
            data=data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = PostSerializer

    def retrieve(self, request, *args, **kwargs):
        post_id = request.data.get("post_id", None)
        post = get_object_or_404(Post, id=post_id)
        serializer = self.serializer_class(post)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostLikeAPIview(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = PostLikeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        post = serializer.save()
        return Response(PostSerializer(post).data, status=status.HTTP_200_OK)


class PostDisLikeAPIview(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = PostDislikeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        post = serializer.save()
        return Response(PostSerializer(post).data, status=status.HTTP_200_OK)


class GetUserFeedAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=request.data.get("user_id", None))
        return Response(PostSerializer(get_feed_for_user(user), many=True).data)


class GetUserFriendsFeed(APIView):
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=request.data.get("user_id", None))
        return Response(
            PostSerializer(get_feed_for_user(user, subscriptions=True), many=True).data
        )


class GetUsersQueryByUsernameAPIView(APIView):
    permission_classes = [
        # IsAuthenticated,
    ]

    def get(self, request, *args, **kwargs):
        query_username = request.data.get("username", None)
        exclude_username = request.data.get("exclude_username", None)
        queryset = (
            User.objects.filter(username__icontains=query_username)
            .exclude(username__exact=exclude_username)
            .all()
        )
        return Response(UserSerializer(queryset, many=True).data)


class SubscribeAPIView(APIView):
    serializer_class = SubscribeSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        post_data = {
            "from_id": request.data.get("from_id"),
            "to_id": request.data.get("to_id"),
        }
        serializer = self.serializer_class(data=post_data)
        if serializer.is_valid(raise_exception=True):
            response = serializer.save()
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class GetUserSubsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        user = get_object_or_404(User, pk=user_id)
        if user:
            return Response(
                data={
                    "subscribers": UserSerializer(
                        map(lambda x: x.user, user.subscribers.all()), many=True
                    ).data,
                    "subscriptions": UserSerializer(
                        user.profile.subscriptions.all(), many=True
                    ).data,
                },
                status=status.HTTP_200_OK,
            )
        return Response("User not found", status=status.HTTP_404_NOT_FOUND)
