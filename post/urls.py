from operator import index

from django.urls import path
# Импортируем созданное нами представление
from .views import (PostsList, PostsDetail, NewsCreate, ArticleCreate, NewsDelete, NewsUpdate,
                    ArticleUpdate, ArticleDelete)


# app_name='post'
urlpatterns = [
   # path('', index, name='index'),

   path('', PostsList.as_view(), name='posts_list'),
   path('post/<int:pk>', PostsDetail.as_view(), name='post_detail'),
   path('posts/create/news/', NewsCreate.as_view(), name='news_create'),
   path('posts/create/article/', ArticleCreate.as_view(), name='article_create'),
   path('posts/news/<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
   path('posts/news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('posts/article/<int:pk>/update/', ArticleUpdate.as_view(), name='article_update'),
   path('posts/article/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
]