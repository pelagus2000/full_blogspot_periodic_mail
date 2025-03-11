# from datetime import timedelta
# from django.utils.timezone import now
# from django.core.mail import send_mail
# from post.models import Posts  # Импорт модели статей
# from subscriber.models import Subscriber  # Импорт модели подписчиков
#
#
# def send_weekly_email_update():
#     # Берем текущую дату и отступаем на 7 дней назад
#     week_ago = now() - timedelta(days=7)
#
#     # Получаем всех подписчиков
#     subscribers = Subscriber.objects.all()
#
#     for subscriber in subscribers:
#         # Ищем категории, на которые подписан пользователь
#         categories = subscriber.get_categories()
#         if not categories.exists():
#             continue  # Пропускаем, если пользователь ни на что не подписан
#
#         # Находим посты за последнюю неделю из подписанных категорий
#         relevant_posts = Posts.objects.filter(
#             categories__in=categories, date__gte=week_ago
#         ).distinct()
#
#         # Если новые статьи есть, отправляем email
#         if relevant_posts.exists():
#             content = "Новые статьи за неделю:\n\n"
#             for post in relevant_posts:
#                 content += f"- {post.title}: {post.get_absolute_url_detail()}\n"
#
#             # Формируем и отправляем email
#             send_mail(
#                 subject="Еженедельное обновление категорий",
#                 message=content,
#                 from_email="admin@example.com",
#                 recipient_list=[subscriber.email],
#             )
