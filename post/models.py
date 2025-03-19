from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import redirect
from django.utils.text import slugify
from category.models import Category
from django.urls import reverse
from author.models import Author
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from urllib.parse import unquote as urlunquote
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.utils.translation import gettext as _  # импортируем функцию для перевода



news = 'News'
article = 'Article'

BLOG_CHOICES = [
    (news, 'News'),
    (article, 'Article')
]

class Posts(models.Model):
    blog_type = models.CharField(
        max_length=20,
        choices=BLOG_CHOICES,
        default='Article'
    )
    title = models.CharField(max_length=75, blank=False)
    body = models.TextField(blank=False, default='Empty field')
    preview = models.CharField(max_length=127, blank=True)
    slug = models.SlugField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, related_name="PostCategory", blank=True)
    post_rating = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)

        if not self.preview and self.body:
            self.preview = f"{self.body[:124]}..."

        super().save(*args, **kwargs)

        cache_key = f'post-{self.pk}'
        cache.delete(cache_key)


    def post_like(self):
        self.post_rating += 1
        self.save()

    def post_dislike(self):
        self.post_rating -= 1
        self.save()

    def get_absolute_url_detail(self):
        current_site = Site.objects.get_current()
        # return f'http://{current_site.domain}{reverse("post_detail", kwargs={"pk": self.pk})}'
        # return f'/products/{self.id}'
        return reverse('post_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.title.title()}' #({self.price})'

    class Meta:
        ordering = ['-id']

class PostCategory(models.Model):
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)

    def add_category(self, category):
        """
        Associates the given category with the post and creates a PostCategory record.
        """
        self.categories.add(category)  # Assuming a ManyToMany relation exists
        PostCategory.objects.create(post_name=self, category_name=category)



