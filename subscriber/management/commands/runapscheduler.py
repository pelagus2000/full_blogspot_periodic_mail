import logging
from datetime import timedelta

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution


from post.models import Posts
from subscriber.models import Subscriber
# from category.models import Category
from subscriber.models import CategoryMail

logger = logging.getLogger(__name__)

job_execution_counter = 0
# наша задача по выводу текста на экран
def my_job():
    global job_execution_counter

    # Increment the counter on every execution
    job_execution_counter += 1
    print(f"Job executed {job_execution_counter} times.")

    week_ago = now() - timedelta(days=7)

    # Получаем всех подписчиков
    subscribers = Subscriber.objects.all()

    for subscriber in subscribers:
        # Ищем категории, на которые подписан пользователь
        categories = subscriber.get_categories()
        if not categories.exists():
            continue  # Пропускаем, если пользователь ни на что не подписан

        # Находим посты за последнюю неделю из подписанных категорий
        relevant_posts = Posts.objects.filter(
            categories__in=categories, date__gte=week_ago
        ).distinct()

        # Если новые статьи есть, отправляем email
        if relevant_posts.exists():
            content = "Новые статьи за неделю:\n\n"
            for post in relevant_posts:
                content += f"- {post.title}: {post.get_absolute_url_detail()}\n"

            # Формируем и отправляем email
            send_mail(
                subject="Еженедельное обновление категорий",
                message=content,
                from_email="pelagus2000@yandex.ru",
                recipient_list=[subscriber.email],
            )

    # Check if the counter reached 10
    if job_execution_counter >= 10:
        print("Apscheduler stopped after 10 executions.")

        scheduler = BlockingScheduler()# Notify the user
        scheduler.start()  # Gracefully stop the scheduler


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/59"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
