from celery import shared_task
from django.core.mail import send_mail
from subscriber.models import Subscriber
from author.models import CategoryMail


@shared_task
def notify_subscribers_about_new_post(post_id, title, preview, categories, post_url):
    """
    Асинхронная задача для уведомления подписчиков о новом посте.
    """
    from category.models import Category  # Импорт внутри функции, чтобы избежать проблем с circular imports
    from post.models import Posts  # Импорт модели Posts

    try:
        # Получаем категорию по идентификаторам
        category_queryset = Category.objects.filter(id__in=categories)
        category_names = ', '.join([category.name for category in category_queryset])

        # Получаем подписчиков категорий
        subscribers = Subscriber.objects.filter(
            categorymail__category3__in=category_queryset
        ).distinct()

        # Генерация списка email адресов
        subscriber_emails = subscribers.values_list('email', flat=True)

        if subscriber_emails:
            # Формируем сообщение
            message = (
                f"Вышел новый пост на сайте:\n\n"
                f"Заголовок: {title}\n\n"
                f"Превью: {preview}\n\n"
                f"Категории: {category_names}\n\n"
                f"Ссылка: {post_url}\n\n"
                f"Спасибо, что остаетесь с нами!"
            )

            # Отправляем письмо всем подписчикам
            send_mail(
                subject=f"Новый пост: {title}",
                message=message,
                from_email='pelagus2000@yandex.ru',  # Укажите ваш email отправителя
                recipient_list=list(subscriber_emails),
            )
        else:
            print(f'Нет подписчиков для поста {post_id}.')
    except Exception as e:
        print(f"Ошибка при выполнении задачи уведомления: {e}")
