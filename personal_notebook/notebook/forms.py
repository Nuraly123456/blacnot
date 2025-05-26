from django import forms
from .models import Entry, CalendarEvent, News

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'content', 'media_file', 'media_type', 'is_pinned']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }

class CalendarEventForm(forms.ModelForm):
    class Meta:
        model = CalendarEvent
        fields = [
            'title', 'description', 'date', 'time',
            'priority', 'notification_time', 'color'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'notification_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
        labels = {
            'title': 'Тақырып',
            'description': 'Сипаттама',
            'date': 'Күні',
            'time': 'Уақыты',
            'priority': 'Басымдылық',
            'notification_time': 'Ескерту уақыты',
            'color': 'Түсі',
        }

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'category', 'source', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'title': 'Тақырып',
            'content': 'Мазмұны',
            'category': 'Санат',
            'source': 'Дереккөз',
            'image': 'Сурет',
        }
