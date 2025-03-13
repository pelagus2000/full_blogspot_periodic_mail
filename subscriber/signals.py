from django_celery_beat.models import PeriodicTask, CrontabSchedule


def setup_periodic_tasks(sender, **kwargs):
    """
    Set up periodic tasks after migrations complete successfully.
    """
    # Ensure tasks are only created if they don't already exist
    schedule, _ = CrontabSchedule.objects.get_or_create(
        minute="0", hour="8", day_of_week="1",  # Every Monday at 8:00 AM
        day_of_month="*", month_of_year="*",
    )
    PeriodicTask.objects.get_or_create(
        crontab=schedule,
        name="Weekly Newsletter Task",
        task="subscriber.tasks.weekly_newsletter",
    )
