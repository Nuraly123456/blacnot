import feedparser
from django.utils import timezone
from .models import News
import random

MOTIVATIONAL_PHRASES = [
    "Өзіңе сен - барлық қиындықтарды жеңе аласың!",
    "Бүгін жасаған әрекетің болашақтағы жетістігіңнің негізі болады",
    "Ұстазсыз ғылым жоқ, талпынмай табыс жоқ",
    "Әр күнді өзіңнің ең жақсы күнің етіп өткіз",
]

def fetch_news_and_motivations():
    # RSS желілерінен жаңалықтар
    rss_sources = [
        {'url': 'https://informburo.kz/feed', 'category': 'education'},
        {'url': 'https://www.inform.kz/kaz/rss', 'category': 'news'},
        {'url': 'https://24.kz/kz/rss', 'category': 'news'},
    ]

    for source in rss_sources:
        feed = feedparser.parse(source['url'])
        for entry in feed.entries[:5]:  # Соңғы 5 жаңалық
            News.objects.get_or_create(
                title=entry.title,
                defaults={
                    'content': entry.description,
                    'category': source['category'],
                    'source': entry.link,
                    'published_at': timezone.now()
                }
            )

    # Күнделікті мотивациялық хабарлама
    if not News.objects.filter(category='motivation',
                             published_at__date=timezone.now().date()).exists():
        News.objects.create(
            title="Күнделікті мотивация",
            content=random.choice(MOTIVATIONAL_PHRASES),
            category='motivation',
            published_at=timezone.now()
        )