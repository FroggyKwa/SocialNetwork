from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request

from api.serializers import SignUpSerializer, SignInSerializer, UserSerializer
from social_network.models import Post


class PostUploadView(APIView):  # TODO: serializer for post
    def post(self, request, *args, **kwargs):
        author_id = request.data["author_id"]
        name = request.data["name"]
        description = request.data["description"]
        picture = request.data["picture_url"]
        try:
            p = Post.objects.create(
                author=User.objects.get(pk=author_id),
                name=name,
                description=description,
                picture_url=picture,
            )
        except Exception as e:
            raise e
        else:
            return Response(status=status.HTTP_200_OK)


class SignUpAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        print(type(user))
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
    lookup_field = 'username'

    def retrieve(self, request, username, *args, **kwargs):
        user = User.objects.get(username__exact=username)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
