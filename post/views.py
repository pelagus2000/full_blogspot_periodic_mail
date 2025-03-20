from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytz.reference import Eastern

from .filters import PostsFilter
from .models import Posts
# from pprint import pprint
from .forms import NewsForm, ArticleForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, mail_managers
from author.models import Author, CategoryMail
from django.contrib import messages
from django.utils.timezone import now
from django.template.loader import render_to_string
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import redirect, render
from django.http import Http404, HttpResponse
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from comment.models import Comment
from comment.forms import CommentForm
from django.core.cache import cache
from django.utils.translation import gettext as _
from pytz import timezone
from datetime import datetime, timedelta
import pytz
from django.utils import timezone
from django.utils.timezone import activate
from django.utils.timezone import now




# Create your views here.

class Index(View):
    def get(self, request):
        current_time = timezone.now()
        models = Posts.objects.all()

        context = {
            'models': models,
            'current_time': current_time,
            'timezones': pytz.common_timezones
        }

        return HttpResponse(render(request, 'index.html', context))

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')

def set_timezone(request):
    if request.method == 'POST':
        timezone = request.POST.get('timezone')
        if timezone in pytz.all_timezones:
            request.session['django_timezone'] = timezone  # Save the timezone in the session
            activate(timezone)  # Activate the selected timezone
        # Redirect back to the page the user came from
        return redirect(request.META.get('HTTP_REFERER', '/'))


class PostsList(ListView):
    model = Posts
    ordering = '-id'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        # Оригинальный запрос
        queryset = super().get_queryset()

        # Инициализация фильтра
        self.filterset = PostsFilter(self.request.GET, queryset)

        # Если фильтр неподключён или запрос пустой, возвращаем полный набор записей
        if not any(self.request.GET.values()) or not self.filterset.is_valid():
            return queryset

        # Если есть применённые фильтры, возвращаем отфильтрованные записи
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        user_timezone = timezone.get_current_timezone()  # Get the user's current timezone
        context['current_time'] = timezone.now().astimezone(user_timezone)  # Adjust to user's timezone
        context['timezones'] = pytz.common_timezones

        return context


from django.contrib.auth.mixins import PermissionRequiredMixin

class PostsDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Posts
    template_name = 'post.html'
    context_object_name = 'post'
    permission_required = 'post.view_posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.all()
        user_timezone = timezone.get_current_timezone()
        context['current_time'] = timezone.now().astimezone(user_timezone)  # Adjust to user's timezone
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Получаем текущий пост

        # Убедимся, что пользователь аутентифицирован
        if not request.user.is_authenticated:
            messages.error(request, "Вы должны быть авторизованы, чтобы оставлять комментарии.")
            return redirect(self.object.get_absolute_url_detail())

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object  # Установка поста для комментария
            comment.user = request.user  # Связывание комментария с текущим пользователем
            comment.author = self.object.author  # Установка автора из поста
            comment.save()  # Сохраняем комментарий в базе данных
            messages.success(request, "Комментарий успешно добавлен.")
        else:
            messages.error(request, "Ошибка при добавлении комментария.")

        return redirect(self.object.get_absolute_url_detail())
    def get(self, request, *args, **kwargs):
        print("DEBUG: PostsDetail accessed with PK =", kwargs.get('pk'))
        return super().get(request, *args, **kwargs)

    def get_object(self, *args, **kwargs):  # hash this function if URL cache is activated
        # Define the cache key based on the post id
        cache_key = f'post-{self.kwargs["pk"]}'

        # Check if the object is already cached
        obj = cache.get(cache_key, None)

        if not obj:
            # Fetch the object from the database
            obj = super().get_object(*args, **kwargs)

            # Cache the object for 5 minutes (300 seconds)
            cache.set(cache_key, obj, timeout=300)

        return obj


@method_decorator(login_required, name='dispatch')
class NewsCreate(PermissionRequiredMixin, CreateView):
    form_class = NewsForm
    model = Posts
    # context_object_name = 'post'
    template_name = 'news_edit.html'
    success_url = reverse_lazy('posts_list')

    permission_required = 'post.add_posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_timezone = timezone.get_current_timezone()
        context['current_time'] = timezone.now().astimezone(user_timezone)  # Adjust to user's timezone
        context['timezones'] = pytz.common_timezones
        return context

    def form_valid(self, form):
        # Установка текущего автора
        author = get_object_or_404(Author, user=self.request.user)

        # Проверка количества постов автора за текущий день
        today_posts = Posts.objects.filter(author=author, date__date=now().date()).count()

        if today_posts >= 23:  # Ограничение: максимум 3 поста в день
            messages.error(self.request, 'Вы можете публиковать только 2-3 поста в день.')
            return self.form_invalid(form)

        # Устанавливаем автора и тип блога
        form.instance.author = author
        form.instance.blog_type = 'News'

        # Сохраняем объект без коммита, чтобы Many-to-Many поля могли быть добавлены
        post = form.save(commit=False)
        post.save()  # Сохраняем объект в базе

        # Теперь сохраняем Many-to-Many отношения
        form.save_m2m()
        print("Связанные категории поста:", post.categories.all())
        return super().form_valid(form)

        # # Работа с категориями поста
        # post = form.instance
        # categories = post.categories.all()  # Получаем связанные категории поста
        #
        # # Лог: проверяем связанные категории
        # print("Категории поста:", categories)
        #
        # # Получение подписчиков из модели CategoryMail
        # subscribers = set()  # Используем set для избежания дублирующихся подписчиков
        # for category in categories:
        #     # Фильтруем подписчиков соответствующей категории
        #     category_subscribers = CategoryMail.objects.filter(category3=category).values_list('subscriber3__email',
        #                                                                                        flat=True)
        #     subscribers.update(category_subscribers)
        #
        # # Лог: проверяем найденных подписчиков
        # print("Подписчики категорий:", subscribers)

        # # Составление списка email для отправки
        # recipient_list = list(subscribers)  # Преобразуем в список
        # print("Список email для отправки:", recipient_list)
        #
        # # Если есть подписчики, отправляем письма
        # if recipient_list:
        #     send_mail(
        #         subject=f'Новый пост в категории "{categories.first().name}"',
        #         message=(
        #             f'Заголовок: {post.title}\n\n'
        #             f'{post.preview}\n\n'
        #             f'Читать дальше: {post.get_absolute_url_detail()}'
        #         ),
        #         from_email='pelagus2000@yandex.ru',
        #         recipient_list=recipient_list,
        #     )
        #     print("Письма отправлены!")
        #
        # return response

class CreatorPermissionMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author.user != self.request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class ArticleCreate(PermissionRequiredMixin, CreateView):
    form_class = ArticleForm
    model = Posts
    template_name = 'article_edit.html'
    success_url = reverse_lazy('posts_list')

    permission_required = 'post.add_posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_timezone = timezone.get_current_timezone()
        context['current_time'] = timezone.now().astimezone(user_timezone)  # Adjust to user's timezone
        context['timezones'] = pytz.common_timezones
        return context

    def form_valid(self, form):
        # Установка текущего автора
        author = get_object_or_404(Author, user=self.request.user)

        # Проверка количества постов автора за текущий день
        today_posts = Posts.objects.filter(author=author, date__date=now().date()).count()

        if today_posts >= 23:  # Ограничение: максимум 3 поста в день
            messages.error(self.request, 'Вы можете публиковать только 2-3 поста в день.')
            return self.form_invalid(form)

        # Устанавливаем автора и тип блога
        form.instance.author = author
        form.instance.blog_type = 'Article'

        # Сохраняем объект без коммита, чтобы Many-to-Many поля могли быть добавлены
        post = form.save(commit=False)
        post.save()  # Сохраняем объект в базе

        # Теперь сохраняем Many-to-Many отношения
        form.save_m2m()
        print("Связанные категории поста:", post.categories.all())
        return super().form_valid(form)


            # response = super().form_valid(form)
            # form.save_m2m()  # Сохраняем связи Many-to-Many
            # return response

        # Работа с категориями поста
        # post = form.instance
        # categories = post.categories.all()  # Получаем связанные категории поста
        #
        # # Лог: проверяем категории
        # print("Категории поста:", categories)
        #
        # # Получение подписчиков из модели CategoryMail
        # subscribers = set()  # Используем set для избежания дублирующихся подписчиков
        # for category in categories:
        #     # Получаем подписчиков для каждой категории
        #     category_subscribers = CategoryMail.objects.filter(
        #         category3=category
        #     ).values_list('subscriber3__email', flat=True)
        #     subscribers.update(category_subscribers)
        #
        # # Лог: проверяем список подписчиков
        # print("Подписчики категорий:", subscribers)
        #
        # # Преобразуем set в список для отправки email
        # recipient_list = list(subscribers)
        # print("Список email для отправки:", recipient_list)

        # Если есть подписчики, отправляем письма
        # if recipient_list:
        #     send_mail(
        #         subject=f'Новая статья в категории "{categories.first().name}"',
        #         message=(
        #             f'Заголовок: {post.title}\n\n'
        #             f'{post.preview}\n\n'
        #             f'Читать дальше: {post.get_absolute_url_detail()}'
        #         ),
        #         from_email='pelagus2000@yandex.ru',
        #         recipient_list=recipient_list,
        #     )
        #     print("Письма отправлены!")

        # return response


class NewsUpdate(CreatorPermissionMixin, PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = NewsForm
    model = Posts
    template_name = 'news_edit.html'
    permission_required = 'post.change_posts'
    success_url = reverse_lazy('posts_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_timezone = timezone.get_current_timezone()
        context['current_time'] = timezone.now().astimezone(user_timezone)  # Adjust to user's timezone
        context['timezones'] = pytz.common_timezones
        return context

    def test_func(self):
    # Проверка прав пользователя, например, только автор может редактировать
        post = self.get_object()

        return self.request.user == post.author


    def handle_no_permission(self):
    # Добавление сообщения об ошибке, если пользователь не имеет прав
        messages.error(self.request, "У вас недостаточно прав для редактирования этой новости!")
        return redirect('post_detail', pk=self.get_object().pk)


class NewsDelete(CreatorPermissionMixin, PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Posts
    template_name = 'news_delete.html'
    success_url = reverse_lazy('posts_list')
    permission_required = 'post.delete_posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_timezone = timezone.get_current_timezone()
        context['current_time'] = timezone.now().astimezone(user_timezone)  # Adjust to user's timezone
        context['timezones'] = pytz.common_timezones
        return context

    def test_func(self):
    # Проверка прав пользователя, например, только автор может редактировать
        post = self.get_object()

        return self.request.user == post.author


    def handle_no_permission(self):
    # Добавление сообщения об ошибке, если пользователь не имеет прав
        messages.error(self.request, "У вас недостаточно прав для удаления этой новости!")
        return redirect('post_detail', pk=self.get_object().pk)


class ArticleUpdate(CreatorPermissionMixin, PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = ArticleForm
    model = Posts
    template_name = 'news_edit.html'
    permission_required = 'post.change_posts'
    success_url = reverse_lazy('posts_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_timezone = timezone.get_current_timezone()
        context['current_time'] = timezone.now().astimezone(user_timezone)  # Adjust to user's timezone
        context['timezones'] = pytz.common_timezones
        return context

    def test_func(self):
    # Проверка прав пользователя, например, только автор может редактировать
        post = self.get_object()

        return self.request.user == post.author


    def handle_no_permission(self):
    # Добавление сообщения об ошибке, если пользователь не имеет прав
        messages.error(self.request, "У вас недостаточно прав для редактирования этой статьи!")
        return redirect('post_detail', pk=self.get_object().pk)


class ArticleDelete(CreatorPermissionMixin, PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Posts
    template_name = 'article_delete.html'
    success_url = reverse_lazy('posts_list')
    permission_required = 'post.delete_posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_timezone = timezone.get_current_timezone()
        context['current_time'] = timezone.now().astimezone(user_timezone)  # Adjust to user's timezone
        context['timezones'] = pytz.common_timezones
        return context

    def test_func(self):
    # Проверка прав пользователя, например, только автор может редактировать
        post = self.get_object()

        return self.request.user == post.author


    def handle_no_permission(self):
    # Добавление сообщения об ошибке, если пользователь не имеет прав
        messages.error(self.request, "У вас недостаточно прав для удаления этой статьи!")
        return redirect('post_detail', pk=self.get_object().pk)

