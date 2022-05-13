from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from social_network.models import Post


class PostUploadView(APIView):
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
            return Response({"content": "hello django"}, status=status.HTTP_200_OK)
