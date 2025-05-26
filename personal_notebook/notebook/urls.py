from django.urls import path
from . import views

urlpatterns = [
    path('news/', views.news_feed, name='news_feed'),
    path('news/check-updates/', views.check_news_updates, name='check_news_updates'),
    path('statistics/', views.statistics, name='statistics'),
]
