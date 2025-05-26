from django.http import JsonResponse
from django.views import View
from .models import News
from django.utils import timezone


class CheckNewsUpdates(View):
    def get(self, request):
        last_update = News.objects.latest('published_at').published_at
        user_last_visit = request.session.get('last_news_visit')

        has_updates = False
        if not user_last_visit or last_update > user_last_visit:
            has_updates = True

        request.session['last_news_visit'] = timezone.now()
        return JsonResponse({'has_updates': has_updates})