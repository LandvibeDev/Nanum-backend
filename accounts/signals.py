#signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

from accounts.models import NanumUser


@receiver(post_save, sender=NanumUser)
def init_new_user(sender, instance, signal, created, **kwargs):
    if created:
        Token.objects.create(user=instance)