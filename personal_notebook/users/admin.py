# users/admin.py
from django.contrib import admin
from users.models import Profile  # Егер сізде Profile моделі болса

admin.site.register(Profile)
