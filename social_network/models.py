from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(150)], null=True
    )
    phone = models.CharField(max_length=13, null=True)
    bio = models.TextField(blank=True)
    friends = models.ManyToManyField(User, related_name="friends")
    subscriptions = models.ManyToManyField(User, related_name="subscribers")

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    class Meta:
        db_table = "Profiles"
