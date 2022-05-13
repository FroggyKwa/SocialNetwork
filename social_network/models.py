import os.path
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from . import validators
from .helpers import UniqueImageField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(150)], blank=True, null=True
    )
    phone = models.CharField(max_length=13, blank=True, null=True)
    bio = models.TextField(blank=True)
    subscriptions = models.ManyToManyField(User, blank=True, related_name="subscribers")
    avatar = UniqueImageField(
        upload_to="images/users/avatars/", default="avatars/default.jpg"
    )
    avatar_thumbnail = UniqueImageField(
        upload_to="images/users/avatars/thumbnails", default="avatars/default.jpg"
    )

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

    def make_thumbnail(self):
        image = Image.open(self.avatar)
        image.thumbnail((512, 512), Image.ANTIALIAS)
        th_name, th_ext = os.path.splitext(self.avatar.name)
        th_ext = th_ext.lower()
        thumb_filename = f"{th_name}_thumb{th_ext}"
        if th_ext in [".jpg", ".jpeg"]:
            filetype = "JPEG"
        elif th_ext == ".gif":
            filetype = "GIF"
        elif th_ext == ".png":
            filetype = "PNG"
        else:
            return False  # Unrecognized file type
        temp_th = BytesIO()
        image.save(temp_th, filetype)
        temp_th.seek(0)

        self.avatar_thumbnail.save(thumb_filename, ContentFile(temp_th.read()), save=False)
        temp_th.close()
        return True

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return f"id{self.user.id} {self.user.username}"

    class Meta:
        db_table = "profiles"


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=512, blank=True, null=True)
    picture_url = UniqueImageField(
        upload_to="images/posts/",
        height_field=None,
        width_field=None,
        null=True,
        validators=[validators.validate_minimum_size(1000, 1000)],
    )
    thumbnail_url = UniqueImageField(
        upload_to="images/posts/thumbnails",
        height_field=None,
        width_field=None,
        null=True,
    )

    def save(self, *args, **kwargs):
        if not self.make_thumbnail():
            raise Exception('Could not create thumbnail - is the file type valid?')

        super(Post, self).save(*args, **kwargs)

    def make_thumbnail(self):
        image = Image.open(self.picture_url)
        image.thumbnail((512, 512), Image.ANTIALIAS)
        th_name, th_ext = os.path.splitext(self.picture_url.name)
        th_ext = th_ext.lower()
        thumb_filename = f"{th_name}_thumb{th_ext}"
        if th_ext in [".jpg", ".jpeg"]:
            filetype = "JPEG"
        elif th_ext == ".gif":
            filetype = "GIF"
        elif th_ext == ".png":
            filetype = "PNG"
        else:
            return False  # Unrecognized file type
        temp_th = BytesIO()
        image.save(temp_th, filetype)
        temp_th.seek(0)

        self.thumbnail_url.save(thumb_filename, ContentFile(temp_th.read()), save=False)
        temp_th.close()
        return True

    class Meta:
        db_table = "posts"
