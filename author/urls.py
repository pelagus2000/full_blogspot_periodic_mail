from django.urls import path
from .views import ProfileCommonView, upgrade_me, create_author

urlpatterns = [
    # Add this
    path('', ProfileCommonView.as_view(), name='users-profile'),
    path('upgrade/', upgrade_me, name='profile_upgrade'),
    path('author/create/', create_author, name='author_creation'),
]