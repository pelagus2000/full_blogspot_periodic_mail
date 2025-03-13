from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now
from datetime import timedelta
from post.models import Posts
from subscriber.models import Subscriber


@shared_task
def weekly_newsletter():
    week_ago = now() - timedelta(days=7)

    # Fetch all subscribers
    subscribers = Subscriber.objects.all()

    for subscriber in subscribers:
        # Get the categories the subscriber is subscribed to
        categories = subscriber.get_categories()
        if not categories.exists():
            continue  # Skip if the user isn't subscribed to any categories

        # Find posts from the past week in subscribed categories
        relevant_posts = Posts.objects.filter(
            categories__in=categories, date__gte=week_ago
        ).distinct()

        if relevant_posts.exists():
            # Format the email content with new posts
            content = "Here are the latest articles from the past week:\n\n"
            for post in relevant_posts:
                content += f"- {post.title}: {post.get_absolute_url_detail()}\n"

            # Send the email to the user
            send_mail(
                subject="Weekly Category Updates",
                message=content,
                from_email="pelagus2000@yandex.ru",
                recipient_list=[subscriber.email],
            )
