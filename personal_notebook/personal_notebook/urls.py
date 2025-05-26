from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from notebook import views as notebook_views
from notebook.views import EventCreateView, EventUpdateView, EventDeleteView
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('notebook.urls')),

    # Django аутентификация маршруты
    path('accounts/', include('django.contrib.auth.urls')),

    # Қолданба users маршрутын қосу — барлық users.urls ішіндегі маршруттар 'users/' префиксімен қолжетімді болады
    path('users/', include('users.urls')),

    # Негізгі бет пен басқа беттер
    path('', notebook_views.home, name='home'),
    path('news/', notebook_views.news_feed, name='news_feed'),
    path('calendar/', notebook_views.calendar, name='calendar'),

    # Оқиғаға қатысты маршруттар
    path('entry/<int:entry_id>/pin/', notebook_views.toggle_pin, name='toggle_pin'),
    path('event/create/', EventCreateView.as_view(), name='event_create'),
    path('event/<int:pk>/update/', EventUpdateView.as_view(), name='event_update'),
    path('event/<int:pk>/delete/', EventDeleteView.as_view(), name='event_delete'),
    path('event/<int:pk>/toggle/', notebook_views.toggle_event_completion, name='toggle_event_completion'),

    # Кіру-шығу және тіркелу
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('signup/', user_views.register, name='signup'),

    # Профиль және құпия сөзді өзгерту тек users/urls.py ішінен шақырылады, мұнда қайталанбауы тиіс!
]

# Медиа файлдарды дамыту режимінде көрсету
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
