from django.shortcuts import render, redirect
from django.views import View
from .forms import SubscriberForm
from django.urls import reverse_lazy
from django.core.mail import send_mail
from author.models import CategoryMail
from .models import Subscriber
from django.contrib import messages
from django.http import HttpResponse
# from .tasks import hello
# from django.db import IntegrityError
# from pytz import timezone
# from datetime import datetime, timedelta
# import pytz
# from django.utils import timezone
# from django.utils.timezone import activate
# from django.utils.timezone import now
# from post.models import Posts
from django.views.generic import ListView

# class Index(View):
#     def get(self, request):
#         current_time = timezone.now()
#         models = Posts.objects.all()
#
#         context = {
#             'models': models,
#             'current_time': current_time,
#             'timezones': pytz.common_timezones
#         }
#
#         return HttpResponse(render(request, 'index.html', context))
#
#     def post(self, request):
#         request.session['django_timezone'] = request.POST['timezone']
#         return redirect('/')
#
# def set_timezone(request):
#     if request.method == 'POST':
#         timezone = request.POST.get('timezone')
#         if timezone in pytz.all_timezones:
#             request.session['django_timezone'] = timezone  # Save the timezone in the session
#             activate(timezone)  # Activate the selected timezone
#         # Redirect back to the page the user came from
#         return redirect(request.META.get('HTTP_REFERER', '/'))

class SubscriberView(ListView):
    success_url = reverse_lazy('posts_list')
    context_object_name = 'subscriber'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user_timezone = timezone.get_current_timezone()
    #     context['current_time'] = timezone.now().astimezone(user_timezone)  # Adjust to user's timezone
    #     context['timezones'] = pytz.common_timezones
    #     return context

    def get(self, request, *args, **kwargs):
        form = SubscriberForm()  # Создаем пустую форму
        return render(request, 'subscriber/make_subscription.html', {'form': form})

    def post(self, request, *args, **kwargs):
        # request.session['django_timezone'] = request.POST['timezone']
        form = SubscriberForm(request.POST)  # Заполняем форму данными POST-запроса

        if form.is_valid():
            # Проверяем, существует ли подписчик с данным email
            email = form.cleaned_data.get('email')
            subscriber, created = Subscriber.objects.get_or_create(email=email)  # Создаем или получаем подписчика

            # Обрабатываем факт существующего подписчика:
            if not created:  # Если подписчик уже существует
                messages.info(request,
                              f"Подписчик с email {email} уже существует. Вы можете добавить дополнительные категории.")

            # Сохраняем категории только те, на которые подписчик еще не подписан
            categories = form.cleaned_data['categories']
            new_categories = []  # Для списка новых категорий
            for category in categories:
                # Проверяем уникальность подписки
                _, cat_created = CategoryMail.objects.get_or_create(subscriber3=subscriber, category3=category)
                if cat_created:  # Добавляем только новые категории
                    new_categories.append(category)

            # Генерируем строку только для новых категорий
            categories_str = ', '.join([category.name for category in new_categories])

            # Отправляем уведомление пользователю о новых категориях, если есть новые
            if new_categories:
                send_mail(
                    subject=f'{subscriber.email} подписался на новые категории',  # Тема письма
                    message=(
                        f'Спасибо за подписку на категории: {categories_str}. Мы будем держать вас в курсе всех новостей!'
                    ),
                    from_email='pelagus2000@yandex.ru',  # Почта отправителя
                    recipient_list=[subscriber.email],  # Письмо отправляется пользователю
                )
                messages.success(request, f"Вы успешно подписались на: {categories_str}")
            else:
                messages.info(request, "Вы уже подписаны на выбранные категории.")

            # Перенаправляем на успешную страницу
            return redirect(self.success_url)
        else:
            # Если данные невалидны, возвращаем форму с ошибками
            return render(request, 'subscriber/make_subscription.html', {'form': form})


# class IndexView(View):
#     def get(self, request):
#         hello.delay()
#         return HttpResponse('Hello!')
