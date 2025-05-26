from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Entry(models.Model):
    MEDIA_TYPES = (
        ('text', 'Текст'),
        ('photo', 'Фото'),
        ('video', 'Видео'),
        ('audio', 'Аудио'),
        ('idea', 'Идея'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    media_file = models.FileField(upload_to='entries/', null=True, blank=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, default='text')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_pinned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} by {self.user.username}"


class CalendarEvent(models.Model):
    PRIORITY_CHOICES = (
        ('low', 'Төмен'),
        ('medium', 'Орташа'),
        ('high', 'Жоғары'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Қолданушы")
    title = models.CharField(max_length=100, verbose_name="Тақырып")
    description = models.TextField(blank=True, verbose_name="Сипаттама")
    date = models.DateField(verbose_name="Күні")
    time = models.TimeField(null=True, blank=True, verbose_name="Уақыты")
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium',
        verbose_name="Басымдылық"
    )
    notification_time = models.DateTimeField(null=True, blank=True, verbose_name="Ескерту уақыты")
    is_completed = models.BooleanField(default=False, verbose_name="Орындалды")
    color = models.CharField(max_length=7, default='#4285f4', verbose_name="Түсі")  # HEX

    class Meta:
        verbose_name = "Күнтізбе оқиғасы"
        verbose_name_plural = "Күнтізбе оқиғалары"
        ordering = ['date', 'time']

    def __str__(self):
        return f"{self.title} - {self.date}"


class News(models.Model):
    CATEGORIES = (
        ('motivation', 'Мотивация'),
        ('advice', 'Кеңес'),
        ('tech', 'Технология'),
        ('education', 'Білім'),
        ('general', 'Жалпы'), # Жаңалықтар үшін жалпы категория қосу ұсынылады
    )

    title = models.CharField(max_length=500, verbose_name="Тақырып") # Ұзындығын арттыруға болады
    content = models.TextField(verbose_name="Мазмұны")
    category = models.CharField(max_length=20, choices=CATEGORIES, default='general', verbose_name="Санат") # Әдепкі мәнін 'general' етіп өзгерту
    source = models.URLField(max_length=500, unique=True, verbose_name="Дереккөз") # max_length арттыру, unique=True қосу
    image = models.ImageField(upload_to='news_images/', blank=True, null=True, verbose_name="Сурет")
    published_at = models.DateTimeField(verbose_name="Жарияланған уақыт", null=True, blank=True) # auto_now_add=True алып тастап, null=True, blank=True қосу
    is_active = models.BooleanField(default=True, verbose_name="Белсенді")

    class Meta:
        verbose_name = "Жаңалық"
        verbose_name_plural = "Жаңалықтар"
        # Енді -published_at бойынша сұрыптауды немесе басқа өріс бойынша сұрыптауды таңдау
        ordering = ['-published_at', '-id'] # Жарияланған уақыты бойынша, содан кейін ID бойынша

    def __str__(self):
        return self.title

class Motivation(models.Model):
    PHRASE_TYPES = (
        ('daily', 'Күнделікті'),
        ('success', 'Жетістік'),
        ('work', 'Жұмыс'),
        ('life', 'Өмір'),
    )

    phrase = models.TextField(verbose_name="Мәтін")
    author = models.CharField(max_length=100, blank=True, verbose_name="Автор")
    phrase_type = models.CharField(
        max_length=20,
        choices=PHRASE_TYPES,
        default='daily',
        verbose_name="Түрі"
    )
    is_active = models.BooleanField(default=True, verbose_name="Белсенді")

    class Meta:
        verbose_name = "Мотивациялық мәтін"
        verbose_name_plural = "Мотивациялық мәтіндер"

    def __str__(self):
        return f"{self.phrase[:50]}..."


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Қолданушы")
    title = models.CharField(max_length=200, verbose_name="Тақырып")
    content = models.TextField(verbose_name="Мазмұны")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Құрылған уақыты")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Жаңартылған уақыты")
    is_published = models.BooleanField(default=True, verbose_name="Жарияланған")

    class Meta:
        verbose_name = "Жазба"
        verbose_name_plural = "Жазбалар"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Хабарландыру"
        verbose_name_plural = "Хабарландырулар"

    def __str__(self):
        return self.message