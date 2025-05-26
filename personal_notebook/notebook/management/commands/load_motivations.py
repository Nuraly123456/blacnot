from django.core.management.base import BaseCommand
from notebook.models import Motivation

MOTIVATIONS = [
    {"phrase": "Өзіңе сен - барлық қиындықтарды жеңе аласың!", "author": "", "phrase_type": "daily"},
    {"phrase": "Қиындықтар сені мықты етеді, олардан қашпа", "author": "", "phrase_type": "daily"},
    # Қосымша 50-100 мотивациялық мәтін...
]

class Command(BaseCommand):
    help = 'Мотивациялық мәтіндерді жүктеу'

    def handle(self, *args, **options):
        for item in MOTIVATIONS:
            Motivation.objects.get_or_create(
                phrase=item['phrase'],
                defaults={
                    'author': item['author'],
                    'phrase_type': item['phrase_type']
                }
            )
        self.stdout.write(self.style.SUCCESS(f'{len(MOTIVATIONS)} мотивациялық мәтін жүктелді'))