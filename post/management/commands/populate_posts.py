from django.core.management.base import BaseCommand
from post.models import Posts


class Command(BaseCommand):
    help = 'Populate the Posts model with test data (50 articles and 50 news)'

    def handle(self, *args, **kwargs):
        # Создание 50 статей
        articles = [
            Posts(
                blog_type='Article',
                title=f'Test Article {i + 1}',
                body=f'This is the body of Test Article {i + 1}.',
            )
            for i in range(50)
        ]
        Posts.objects.bulk_create(articles)

        # Создание 50 новостей
        news = [
            Posts(
                blog_type='News',
                title=f'Test News {i + 1}',
                body=f'This is the body of Test News {i + 1}.',
            )
            for i in range(50)
        ]
        Posts.objects.bulk_create(news)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully added {Posts.objects.filter(blog_type='Article').count()} articles and {Posts.objects.filter(blog_type='News').count()} news."
            )
        )
