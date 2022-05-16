import os
import secrets
from io import BytesIO
from random import randint

from PIL import Image
from django.core.files.base import ContentFile
from django.db.models import ImageField


class UniqueImageField(ImageField):
    def generate_filename(self, instance, filename):
        path, ext = os.path.splitext(filename)
        name = secrets.token_hex(randint(0, 10000000)) + ext
        return super().generate_filename(instance, name)
