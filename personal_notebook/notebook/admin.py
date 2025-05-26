from django.contrib import admin
from .models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'published_at', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'content')
    list_editable = ('is_active',)
    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    make_active.short_description = "Таңдалған жаңалықтарды белсендіру"

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    make_inactive.short_description = "Таңдалған жаңалықтарды белсенсіздендіру"