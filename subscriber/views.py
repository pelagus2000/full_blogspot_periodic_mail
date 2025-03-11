from django.shortcuts import render, redirect
from django.views import View
from .forms import SubscriberForm
from django.urls import reverse_lazy
from django.core.mail import send_mail
from author.models import CategoryMail
from .models import Subscriber
from django.contrib import messages
# from django.db import IntegrityError

class SubscriberView(View):
    success_url = reverse_lazy('posts_list')

    def get(self, request, *args, **kwargs):
        form = SubscriberForm()  # Создаем пустую форму
        return render(request, 'subscriber/make_subscription.html', {'form': form})

    def post(self, request, *args, **kwargs):
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
