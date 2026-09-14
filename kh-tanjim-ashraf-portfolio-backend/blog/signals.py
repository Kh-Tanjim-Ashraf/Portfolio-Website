from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Post, PostLikeViewCount



@receiver(post_save, sender=Post)
def create_post_analytics(sender, instance, created, **kwargs):
    if created:
        PostLikeViewCount.objects.create(post=instance)