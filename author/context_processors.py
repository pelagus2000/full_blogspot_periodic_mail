from django.contrib.auth.models import Group

def is_author(request):
    """
       Проверяет, состоит ли пользователь в группе 'author' и добавляет переменную 'is_author' в контекст шаблона.
       """
    if request.user.is_authenticated:
        return {'is_author': Group.objects.filter(name='author', user=request.user).exists()}
    return {'is_author': False}

