from django.db import models
from author.models import CategoryMail

class Category(models.Model):
    name = models.CharField(max_length=75, unique=True) # FIXME  NAME LIMIT TO ONE WORD OTHERWISE COMMAND DELETE POSTS BY CATEGORY DO NOT WORK

    def __str__(self):
        return self.name

    def get_subscribers(self):
        """
        Получить всех подписчиков по связи через CategoryMail
        """
        from subscriber.models import Subscriber
        return Subscriber.objects.filter(categorymail__category3=self)



