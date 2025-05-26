from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
from django.contrib.auth import logout
from django.shortcuts import redirect

from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Profile
from notebook.models import Entry, CalendarEvent


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт құрылды! {username} енді жүйеге кіре аласыз.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile_view(request):
    user = request.user
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Профиль сәтті жаңартылды.")
            return redirect('users:profile')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileUpdateForm(instance=profile)

    return render(request, 'users/profile.html', {
        'u_form': user_form,
        'p_form': profile_form
    })


@login_required
def profile_stats(request):
    today = timezone.now().date()
    entries_count = Entry.objects.filter(user=request.user).count()
    pinned_count = Entry.objects.filter(user=request.user, is_pinned=True).count()
    today_events = CalendarEvent.objects.filter(user=request.user, date=today).count()

    return JsonResponse({
        'entries_count': entries_count,
        'pinned_count': pinned_count,
        'today_events': today_events,
    })


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Пайдаланушы сессиясын жаңарту
            messages.success(request, 'Құпия сөз сәтті өзгертілді!')
            return redirect('users:profile')
        else:
            messages.error(request, 'Қателер бар, өтінеміз тексеріңіз.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'users/change_password.html', {'form': form})

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        return redirect('home')  # Немесе қалаған бетіңізге бағыттаңыз
    return redirect('users:profile')
