from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request

from api.db_methods.post_methods import get_feed_for_user

from api.serializers import (
    SignUpSerializer,
    SignInSerializer,
    UserSerializer,
    PostUploadSerializer,
    PostSerializer,
    PostLikeSerializer,
    PostDislikeSerializer,
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
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    lookup_field = "username"

    def retrieve(self, request, username, *args, **kwargs):
        user = get_object_or_404(User, username=username)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class PostRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = PostSerializer

    def retrieve(self, request, *args, **kwargs):
        post_id = request.data.get("post_id", None)
        post = get_object_or_404(Post, id=post_id)
        serializer = self.serializer_class(post)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostLikeAPIview(APIView):
    permission_classes = [
        AllowAny,
    ]
    serializer_class = PostLikeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        post = serializer.save()
        return Response(PostSerializer(post).data, status=status.HTTP_200_OK)


class PostDisLikeAPIview(APIView):
    permission_classes = [
        AllowAny,
    ]
    serializer_class = PostDislikeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        post = serializer.save()
        return Response(PostSerializer(post).data, status=status.HTTP_200_OK)


class GetUserFeed(APIView):
    def get(self, request, *args, **kwargs):
        print(request.data.get("user_id"))
        user = get_object_or_404(User, id=request.data.get("user_id", None))
        return Response(PostSerializer(get_feed_for_user(user), many=True).data)
