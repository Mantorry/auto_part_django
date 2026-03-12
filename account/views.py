from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from django.contrib.auth.hashers import make_password


def login_view(request):
    if request.session.get('user_id'):
        return redirect('catalog:index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username, is_active=True)
            if user.check_password(password):
                request.session['user_id'] = user.id
                request.session['user_role'] = user.role
                request.session['user_name'] = user.full_name
                return redirect('catalog:index')
            else:
                messages.error(request, 'Неверный пароль')
        except User.DoesNotExist:
            messages.error(request, 'Пользователь не найден')
    return render(request, 'account/login.html')


def logout_view(request):
    request.session.flush()
    return redirect('account:login')


def settings_view(request):
    from .decorators import login_required_custom
    user = get_current_user(request)
    if not user:
        return redirect('account:login')
    if request.method == 'POST':
        theme = request.POST.get('theme', 'light')
        notifications = request.POST.get('notifications_enabled') == 'on'
        user.theme = theme
        user.notifications_enabled = notifications
        user.save()
        request.session['user_theme'] = theme
        messages.success(request, 'Настройки сохранены')
        return redirect('account:settings')
    return render(request, 'account/settings.html', {'user': user})


def get_current_user(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            pass
    return None
