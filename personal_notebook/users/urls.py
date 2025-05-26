from django.urls import path
from .views import profile_view, change_password, delete_account

app_name = 'users'

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('change-password/', change_password, name='change_password'),
    path('delete-account/', delete_account, name='delete_account'),
]
