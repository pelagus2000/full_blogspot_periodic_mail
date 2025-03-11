from django.db import models
from django.contrib.auth.models import User
# from category.models import Category
# from subscriber.models import Subscriber



class Author(models.Model):
    author_name = models.CharField(max_length=75, blank=False, default='John Doe')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.author_name

class CategoryMail(models.Model):
    category3 = models.ForeignKey('category.Category', on_delete=models.CASCADE)
    subscriber3 = models.ForeignKey('subscriber.Subscriber', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('category3', 'subscriber3')

    def __str__(self):
        return f"{self.subscriber3.email} -> {self.category3.name}"


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#
#     avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
#     bio = models.TextField()
#
#     def __str__(self):
#         return self.user.username

