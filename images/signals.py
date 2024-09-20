from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Image

"""Reciver will triggered when the user like is update and total like will
    will be updated by the instance"""
@receiver(m2m_changed, sender=Image.users_like.through)
def users_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.users_like.count()
    instance.save()