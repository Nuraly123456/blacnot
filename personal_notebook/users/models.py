from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class UserTheme(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    primary_color = models.CharField(max_length=7, default='#4285f4')
    secondary_color = models.CharField(max_length=7, default='#34a853')
    dark_mode = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} темасы"


class NotificationSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    event_reminders = models.BooleanField(default=True)
    news_updates = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} ескерту параметрлері"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(max_length=500, blank=True, verbose_name="Биография")
    location = models.CharField(max_length=100, blank=True, verbose_name="Орналасқан жері")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Туған күні")
    profile_image = models.ImageField(
        upload_to='profile_images/',
        default='profile_images/default.png',
        verbose_name="Профиль суреті"
    )
    website = models.URLField(blank=True, verbose_name="Веб-сайт")

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профильдер"

    def __str__(self):
        return f"{self.user.username} профилі"


@receiver(post_save, sender=User)
def create_user_related_models(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        UserTheme.objects.create(user=instance)
        NotificationSettings.objects.create(user=instance)