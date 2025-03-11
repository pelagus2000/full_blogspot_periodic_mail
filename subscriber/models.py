from django.db import models
from author.models import CategoryMail


class Subscriber(models.Model):
    email = models.EmailField(max_length=75, unique=False)
    datetime = models.DateTimeField(auto_now_add=True)  # Дата подписки

    def __str__(self):
        return self.email

    def get_categories(self):
        """
        Получить категории, на которые подписан пользователь, через связь CategoryMail
        """
        from category.models import Category
        return Category.objects.filter(categorymail__subscriber3=self)
