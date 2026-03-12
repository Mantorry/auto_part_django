from .models import User


def user_context(request):
    user_id = request.session.get('user_id')
    user = None
    if user_id:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            pass
    theme = request.session.get('user_theme', 'light')
    if user:
        theme = user.theme
    return {
        'current_user': user,
        'current_theme': theme,
    }
