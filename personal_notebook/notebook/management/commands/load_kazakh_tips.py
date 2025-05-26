from django.core.management.base import BaseCommand
from notebook.models import Tip

KAZAKH_TIPS = [
    {
        "title": "Уақытты тиімді пайдалану",
        "content": "Күнделікті жоспар жасап, маңызды тапсырмаларды таңертеңгі сағаттарда орындаңыз.",
        "category": "productivity"
    },
    # Қосымша кеңестер...
]

class Command(BaseCommand):
    help = 'Қазақ тіліндегі кеңестерді жүктеу'

    def handle(self, *args, **options):
        for tip in KAZAKH_TIPS:
            Tip.objects.get_or_create(
                title=tip['title'],
                defaults={
                    'content': tip['content'],
                    'category': tip['category']
                }
            )
        self.stdout.write(self.style.SUCCESS(f'{len(KAZAKH_TIPS)} кеңес жүктелді'))