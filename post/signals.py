from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from .models import Posts
from author.models import CategoryMail
from subscriber.models import Subscriber
from allauth.account.signals import user_signed_up

@receiver(m2m_changed, sender=Posts.categories.through)
def notify_if_post_create(sender, instance, **kwargs):
    """
    Уведомляет подписчиков категорий о создании или обновлении поста.
    """
    print(f'Processing post: {instance.title}')

    # Получаем категории текущего поста
    categories = instance.categories.all()
    if not categories.exists():
        print(f"No categories found for post: {instance.title}")
        return

    print('Categories found:')
    for category in categories:
        print(f'- {category.name}')

    # Получаем всех подписчиков через связь CategoryMail
    all_subscribers = Subscriber.objects.filter(
        categorymail__category3__in=categories  # Категории, связанные с постом
    ).distinct()  # Убираем возможные дубликаты подписчиков

    # Формируем список email для подписчиков
    subscriber_emails = all_subscribers.values_list('email', flat=True)
    print(f'Subscribers emails: {list(subscriber_emails)}')

    # Проверяем, есть ли подписчики
    if not subscriber_emails:
        print(f'No subscribers found for post: {instance.title}')
        return

    # Генерируем текст письма
    category_names = ', '.join([category.name for category in categories])
    message = (
        f'Notification of a New Post on your subscription in example.com'
        f'Title: {instance.title}\n\n'
        f'Preview: {instance.preview}\n\n'
        f'Categories: {category_names}\n\n'
        f'Link: {instance.get_absolute_url_detail()}'
    )
    print('Message built! Sending emails...')

    # Отправляем всем подписчикам email
    send_mail(
        subject=f'New Post: {instance.title} in Categories: {category_names}',
        message=message,
        from_email='pelagus2000@yandex.ru',  # Укажите email отправителя
        recipient_list=list(subscriber_emails),  # Преобразуем данные в обычный список
    )
    print(f'Emails sent successfully to: {", ".join(subscriber_emails)}')

@receiver(user_signed_up)
def send_welcome_email(request, user, **kwargs):
    """
    Отправляем приветственное письмо новому пользователю
    сразу после завершения регистрации.
    """
    subject = "Добро пожаловать на наш сайт!"
    message = (
        f"Здравствуйте, {user.first_name}!\n\n"
        "Мы рады приветствовать вас на нашем сайте. Надеемся, что вы найдете полезную информацию. "
        "Если у вас возникнут вопросы, не стесняйтесь связаться с нами."
    )
    from_email = "pelagus2000@yandex.ru"
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)

