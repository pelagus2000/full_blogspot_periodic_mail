from django.urls import path

from .views import SubscriberView


app_name='subscriber'
urlpatterns = [
   # path('', index, name='index'),
    path('subscriber/', SubscriberView.as_view(), name='subscription'),

]

