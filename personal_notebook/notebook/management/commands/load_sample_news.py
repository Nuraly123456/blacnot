import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from notebook.models import News
from django.utils import timezone

class Command(BaseCommand):
    help = 'BAQ.KZ сайтынан IT жаңалықтарды жүктеу'

    def handle(self, *args, **kwargs):
        url = 'https://baq.kz/tag/it_qzg4ps9h4h/'

        response = requests.get(url)
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR('Сайтқа қосыла алмадым'))
            return

        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.select('.news-item')  # Мақалалар блоктарын таңдаңыз

        for article in articles:
            title_tag = article.select_one('.title a')
            if not title_tag:
                continue

            title = title_tag.text.strip()
            link = title_tag['href']
            full_url = 'https://baq.kz' + link

            summary_tag = article.select_one('.description')
            summary = summary_tag.text.strip() if summary_tag else ''

            News.objects.get_or_create(
                title=title,
                defaults={
                    'content': summary,
                    'category': 'tech',
                    'source': full_url,
                    'published_at': timezone.now()
                }
            )

        self.stdout.write(self.style.SUCCESS('BAQ.KZ жаңалықтары жүктелді!'))
