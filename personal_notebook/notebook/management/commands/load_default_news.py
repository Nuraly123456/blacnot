import feedparser
from django.core.management.base import BaseCommand
from notebook.models import News


class Command(BaseCommand):
    help = 'Әдепкі жаңалықтарды жүктеу'

    def handle(self, *args, **options):
        # Inform.kz RSS лентасы
        feed = feedparser.parse("https://www.inform.kz/kaz/rss")

        for entry in feed.entries[:10]:  # Соңғы 10 жаңалық
            News.objects.get_or_create(
                title=entry.title,
                defaults={
                    'content': entry.description,
                    'source': entry.link,
                    'category': 'education',
                    'is_active': True
                }
            )

        self.stdout.write(self.style.SUCCESS('Жаңалықтар сәтті жүктелді'))