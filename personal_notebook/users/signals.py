from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User  # or your custom user model
from .models import Profile, NotificationSettings, UserTheme

@receiver(post_save, sender=User)
def create_user_related_models(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
        NotificationSettings.objects.get_or_create(user=instance)
        UserTheme.objects.get_or_create(user=instance)
