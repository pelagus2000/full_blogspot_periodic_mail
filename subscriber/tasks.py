from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from subscriber.scheduler import send_weekly_email_update
scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

# Импорт функции для отправки обновлений
from subscriber.tasks import send_weekly_email_update


def start():
    # Добавление периодической задачи
    scheduler.add_job(
        send_weekly_email_update,
        'cron',  # Расписание: раз в неделю
        day_of_week='sun',  # Запускать по воскресеньям
        hour=8,  # В 8 утра
        minute=0,
        id='weekly_email_update',  # Уникальный ID задачи
        replace_existing=True
    )
    scheduler.start()
