from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from post.models import Posts
from .tasks import notify_subscribers_about_new_post


@receiver(m2m_changed, sender=Posts.categories.through)
def notify_if_post_create(sender, instance, action, **kwargs):
    """
    Уведомляет подписчиков категорий о создании поста.
    """
    if action == 'post_add':  # Убедимся, что обрабатываем событие добавления
        categories = instance.categories.values_list('id', flat=True)  # Получаем ID всех категорий
        post_url = instance.get_absolute_url_detail()  # Генерация URL поста
        notify_subscribers_about_new_post.delay(
            post_id=instance.id,
            title=instance.title,
            preview=instance.preview,
            categories=list(categories),
            post_url=post_url
        )
