from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import NetworkUser

@receiver(post_save, sender=User)
def create_network_user(sender, instance, created, **kwargs):
    if created:
        NetworkUser.objects.create(user=instance)