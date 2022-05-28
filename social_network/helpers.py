import os
import secrets
from io import BytesIO
from random import randint

import requests
from PIL import Image
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.db.models import ImageField
from django.middleware.csrf import get_token


class UniqueImageField(ImageField):
    def generate_filename(self, instance, filename):
        path, ext = os.path.splitext(filename)
        name = secrets.token_hex(randint(0, 10000000)) + ext
        return super().generate_filename(instance, name)


def get_subs(username, request):
    session_id = request.session.session_key
    csrf_token = get_token(request)
    return requests.get(
        "http://localhost:8080/api/get_subs",
        data={"user_id": User.objects.get(username__exact=username).id},
        headers={"sessionid": session_id, "csrftoken": csrf_token},
    ).json()
