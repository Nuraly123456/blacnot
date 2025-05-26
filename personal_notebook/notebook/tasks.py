from celery import shared_task
from .utils import fetch_news_and_motivations

@shared_task
def update_news_daily():
    fetch_news_and_motivations()
    return "Жаңалықтар сәтті жаңартылды"