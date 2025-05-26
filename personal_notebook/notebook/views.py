from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Count
from datetime import timedelta

from .models import Entry, CalendarEvent, News, Post
from .forms import EntryForm, CalendarEventForm, NewsForm


@login_required
def home(request):
    pinned_entries = Entry.objects.filter(user=request.user, is_pinned=True).order_by('-updated_at')
    if request.method == 'POST':
        form = EntryForm(request.POST, request.FILES)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.success(request, 'Жазба қосылды!')
            return redirect('home')
    else:
        form = EntryForm()
    return render(request, 'notebook/home.html', {
        'pinned_entries': pinned_entries,
        'form': form,
    })


@login_required
def news_feed(request):
    query = request.GET.get('q', '')
    news_list = News.objects.filter(is_active=True).order_by('-published_at')

    if query:
        news_list = news_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )

    today = timezone.now().date()
    daily_motivation = News.objects.filter(
        category='motivation',
        published_at__date=today,
        is_active=True
    ).first()

    if not daily_motivation:
        daily_motivation = News.objects.filter(
            category='motivation',
            is_active=True
        ).order_by('?').first()

    advice = News.objects.filter(
        category='advice',
        is_active=True
    ).order_by('?').first()

    paginator = Paginator(news_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'daily_motivation': daily_motivation,
        'advice': advice,
        'page_obj': page_obj,
        'query': query,
        'categories': dict(News.CATEGORIES),
    }

    return render(request, 'notebook/news_feed.html', context)


@login_required
def check_news_updates(request):
    recent_time = timezone.now() - timezone.timedelta(minutes=5)
    has_updates = News.objects.filter(published_at__gte=recent_time, is_active=True).exists()
    return JsonResponse({'has_updates': has_updates})


@login_required
def calendar(request):
    today = timezone.now().date()
    events = CalendarEvent.objects.filter(user=request.user, date__gte=today).order_by('date')

    if request.method == 'POST':
        form = CalendarEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            messages.success(request, 'Оқиға қосылды!')
            return redirect('calendar')
    else:
        form = CalendarEventForm()

    return render(request, 'notebook/calendar.html', {
        'events': events,
        'form': form,
        'today': today,
    })


class CalendarView(ListView):
    model = CalendarEvent
    template_name = 'notebook/calendar.html'
    context_object_name = 'events'

    def get_queryset(self):
        today = timezone.now().date()
        return CalendarEvent.objects.filter(
            user=self.request.user,
            date__gte=today
        ).order_by('date', 'time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        week_days = []
        for i in range(7):
            day = today + timezone.timedelta(days=i)
            week_days.append({
                'date': day,
                'events': CalendarEvent.objects.filter(
                    user=self.request.user,
                    date=day
                ).order_by('time'),
                'is_today': day == today
            })

        context.update({
            'today': today,
            'week_days': week_days,
            'form': CalendarEventForm(),
            'priorities': dict(CalendarEvent.PRIORITY_CHOICES),
        })
        return context


class EventCreateView(CreateView):
    model = CalendarEvent
    form_class = CalendarEventForm
    success_url = reverse_lazy('calendar')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Оқиға сәтті қосылды!')
        return super().form_valid(form)


class EventUpdateView(UpdateView):
    model = CalendarEvent
    form_class = CalendarEventForm
    success_url = reverse_lazy('calendar')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Оқиға сәтті жаңартылды!')
        return super().form_valid(form)


class EventDeleteView(DeleteView):
    model = CalendarEvent
    success_url = reverse_lazy('calendar')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Оқиға сәтті жойылды!')
        return super().delete(request, *args, **kwargs)


@login_required
def toggle_event_completion(request, pk):
    event = get_object_or_404(CalendarEvent, pk=pk, user=request.user)
    event.is_completed = not event.is_completed
    event.save()
    return JsonResponse({
        'status': 'success',
        'is_completed': event.is_completed
    })


@login_required
def profile(request):
    pass


@login_required
def toggle_pin(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id, user=request.user)
    entry.is_pinned = not entry.is_pinned
    entry.save()
    return redirect('home')


@login_required
def statistics(request):
    posts_stats = Post.objects.filter(
        user=request.user,
        created_at__date__gte=timezone.now().date() - timedelta(days=7)
    ).values(
        'created_at__date'
    ).annotate(
        count=Count('id')
    ).order_by('created_at__date')

    today = timezone.now().date()
    events_stats = CalendarEvent.objects.filter(
        user=request.user,
        date__range=[today - timedelta(days=7), today]
    ).values(
        'date'
    ).annotate(
        count=Count('id')
    ).order_by('date')

    return render(request, 'notebook/statistics.html', {
        'posts_stats': posts_stats,
        'events_stats': events_stats,
    })
