from django.urls import path
from . import views

urlpatterns = [
    # Другие пути...
    path('add-category/', views.add_category, name='add-category'),  # URL для добавления категорий
]
