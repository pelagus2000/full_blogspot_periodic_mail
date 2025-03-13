from django.urls import path
# from .views import IndexView
from .views import SubscriberView


app_name='subscriber'
urlpatterns = [
   # path('', IndexView.as_view(), name='index'),
    path('subscriber/', SubscriberView.as_view(), name='subscription'),
]

