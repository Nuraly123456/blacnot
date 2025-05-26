import feedparser
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timezone as dt_timezone
from django.db import IntegrityError # IntegrityError-ды импорттау

# Сіздің News моделіңізді дұрыс импорттаңыз
# Мысалы, егер сіздің моделіңіз 'notebook' қосымшасында болса:
from notebook.models import News

class Command(BaseCommand):
    help = 'RSS арналарынан жаңалықтарды алып, дерекқорға сақтайды.'

    # Қазақстандық RSS арналарының тізімі
    # Қажетті арналарды осы жерге қосыңыз немесе алып тастаңыз
    FEED_URLS = [
        'https://www.inform.kz/kaz/rss', # ҚазАқпарат (қазақша)
        'https://tengrinews.kz/rss/',    # Tengrinews.kz (орысша)
        'https://kaz.nur.kz/rss.xml',    # NUR.KZ (қазақша)
        'https://baq.kz/kk/rss',         # Baq.kz (қазақша)
        # Басқа қазақстандық жаңалықтар сайттарының RSS арналарын қосыңыз
    ]

    def handle(self, *args, **kwargs):
        total_new_items = 0
        self.stdout.write(self.style.HTTP_INFO('Жаңалықтарды алу процесі басталды...'))

        for url in self.FEED_URLS:
            self.stdout.write(self.style.NOTICE(f'"{url}" арнасынан жаңалықтарды алуда...'))
            try:
                feed = feedparser.parse(url)
                if feed.bozo: # Егер RSS арнасында қателер болса
                    self.stdout.write(self.style.WARNING(f'Ескерту: "{url}" арнасында парсинг қателері бар: {feed.bozo_exception}'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Қате: "{url}" арнасын өңдеу мүмкін болмады: {e}'))
                continue # Келесі арнаға өту

            new_items_current_feed = 0
            for entry in feed.entries:
                title = getattr(entry, 'title', 'Атауы жоқ жаңалық')
                link = getattr(entry, 'link', None)

                # RSS арнасынан алынған жарияланған уақытты өңдеу
                published_at = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    try:
                        # feedparser уақытты UTC timezone-ға айналдырамыз
                        published_at = timezone.datetime(*entry.published_parsed[:6], tzinfo=dt_timezone.utc)
                    except (ValueError, TypeError):
                        self.stdout.write(self.style.WARNING(f'Ескерту: Дұрыс емес уақыт форматы немесе мән: "{getattr(entry, "published_parsed", "N/A")}" для "{title}". Қазіргі уақыт қолданылады.'))
                        published_at = timezone.now() # Қате болса, қазіргі уақытты қолдану

                # Мазмұнды алу: summary немесе description
                content = getattr(entry, 'summary', '')
                if not content and hasattr(entry, 'description'):
                    content = entry.description
                # Мазмұн өте ұзын болса, шектеу қоюға болады (мысалы, 65535 белгі)
                # content = content[:65535]

                # Егер сілтеме жоқ болса, бұл жаңалықты өткізіп жіберуіміз мүмкін,
                # себебі 'source' өрісі unique=True және маңызды
                if not link:
                    self.stdout.write(self.style.WARNING(f'Ескерту: Сілтемесі жоқ жаңалық өткізіліп тасталды: "{title}"'))
                    continue

                try:
                    # News моделіне жаңалықты сақтау
                    news_item = News(
                        title=title,
                        content=content,
                        source=link, # Сілтемені 'source' өрісіне сақтау
                        published_at=published_at,
                        is_active=True,
                        category='general', # Әдепкі категория
                    )
                    news_item.save()
                    new_items_current_feed += 1
                    total_new_items += 1
                    self.stdout.write(self.style.SUCCESS(f'Қосылды: "{title}"'))

                except IntegrityError:
                    # 'source' өрісі unique болғандықтан, қайталанатын сілтемелер осы қатені тудырады
                    self.stdout.write(self.style.WARNING(f'Жаңалық бұрыннан бар (сілтеме қайталанады): "{title}"'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Қате: Жаңалықты сақтауда проблема туындады "{title}": {e}'))

            self.stdout.write(self.style.SUCCESS(f'"{url}" арнасынан қосылған жаңа жаңалықтар саны: {new_items_current_feed}.'))

        self.stdout.write(self.style.SUCCESS(f'Жаңалықтарды алу аяқталды. Барлығы қосылды: {total_new_items} жаңа жаңалық.'))