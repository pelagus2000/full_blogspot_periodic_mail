from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import AuthorForm


class ProfileCommonView(LoginRequiredMixin, TemplateView):
    template_name = 'profile/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context



# @login_required
# def upgrade_me(request):
#     user = request.user
#     author_group = Group.objects.get(name='author')
#     if not request.user.groups.filter(name='author').exists():
#         author_group.user_set.add(user)
#     return redirect('users-profile')
#
# class CommonGroupView(PermissionRequiredMixin, View):
#     permission_required = 'post.view_posts'
#
# class AuthorGroupView(PermissionRequiredMixin, View):
#     permission_required = ('post.view_posts',
#                            'post.add_posts',
#                            'post.change_posts'
#                            'post.delete_posts')
#
@login_required
def create_author(request):
    # Проверяем, является ли пользователь уже автором
    if request.user.groups.filter(name='author').exists():
        return redirect('users-profile')  # Перенаправляем, если уже автор

    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            # Создаём нового автора
            author = form.save(commit=False)
            author.user = request.user
            author.save()

            # Добавляем пользователя в группу "author"
            author_group, created = Group.objects.get_or_create(name='author')
            author_group.user_set.add(request.user)

            return redirect('users-profile')  # Перенаправляем в профиль после сохранения
    else:
        form = AuthorForm()

    return render(request, 'profile/author_creation.html', {'form': form})
@login_required
def upgrade_me(request):
    user = request.user
    author_group, created = Group.objects.get_or_create(name='author')  # Получаем или создаём группу "author"

    # Проверяем, состоит ли пользователь в группе "author"
    if user.groups.filter(name='author').exists():
        return redirect('users-profile')  # Перенаправляем, если уже автор

    # Обрабатываем форму создания автора
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            # Создаём объект автора, связывая его с текущим пользователем
            author = form.save(commit=False)
            author.user = user  # Связываем автора с пользователем
            author.save()

            # Добавляем пользователя в группу "author"
            author_group.user_set.add(user)

            return redirect('users-profile')  # После сохранения возвращаемся в профиль
    else:
        form = AuthorForm()  # Пустая форма, если GET-запрос

    # Рендерим страницу с формой, если запрос не POST или форма некорректна
    return render(request, 'profile/author_creation.html', {'form': form})