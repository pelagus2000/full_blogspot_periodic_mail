from django.db import models
from django.shortcuts import redirect
from django.contrib import messages
from post.models import Posts
from django.contrib.auth.models import User
from author.models import Author


class Comment(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='author_comments')
    content = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)



    def comment_like(self):
        self.comment_rating += 1
        self.save()

    def comment_dislike(self):
        self.comment_rating -= 1
        self.save()

    def __str__(self):
        return f'Комментарий от {self.user} на посте {self.post} {self.author}'
