from django.core.management.base import BaseCommand, CommandError
from post.models import Posts
from category.models import Category


class Command(BaseCommand):
    help = "Удаляет все новости из указанной категории после подтверждения."

    def add_arguments(self, parser):
        parser.add_argument('category_name', type=str, help="Имя категории для удаления новостей")

    def handle(self, *args, **options):
        category_name = options['category_name']
        try:
            # Проверяем, есть ли такая категория
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            raise CommandError(f"Категория '{category_name}' не найдена.")

        # Получаем все посты, связанные с данной категорией
        posts_to_delete = Posts.objects.filter(categories=category)

        if not posts_to_delete.exists():
            self.stdout.write(f"Нет новостей в категории '{category_name}' для удаления.")
            return

        self.stdout.write(f"Будут удалены следующие новости из категории '{category_name}':")
        for post in posts_to_delete:
            self.stdout.write(f"- {post.title}")

        # Подтверждение действия
        confirm = input("Вы уверены, что хотите удалить все эти новости? [y/N]: ").strip().lower()
        if confirm == 'y':
            count, _ = posts_to_delete.delete()
            self.stdout.write(self.style.SUCCESS(f"Удалено {count} новостей из категории '{category_name}'."))
        else:
            self.stdout.write(self.style.WARNING("Операция отменена."))

