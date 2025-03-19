
from django.urls import path
from django.views.decorators.cache import cache_page # TODO if URL cache based used instead normal path used at low level cache
from .views import (PostsList, PostsDetail, NewsCreate, ArticleCreate, NewsDelete, NewsUpdate,
                    ArticleUpdate, ArticleDelete)


# app_name='post' FIXME unknown connection use
urlpatterns = [
   # path('', index, name='index'),

   path('', PostsList.as_view(), name='posts_list'),
   # path('post/<int:pk>/', cache_page(60*5) (PostsDetail.as_view()), name='post_detail'), # cache for the classviews/genericviews
   path('post/<int:pk>/', PostsDetail.as_view(), name='post_detail'), # low-level cache - only Article

   path('posts/create/news/', NewsCreate.as_view(), name='news_create'),
   path('posts/create/article/', ArticleCreate.as_view(), name='article_create'),
   path('posts/news/<int:pk>/update/', NewsUpdate.as_view(), name='news_update'), # FIXME not working
   path('posts/news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'), # FIXME not working
   path('posts/article/<int:pk>/update/', ArticleUpdate.as_view(), name='article_update'), # FIXME not working
   path('posts/article/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'), # FIXME not working
]