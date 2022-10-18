from django.urls import path
from .views import NotificationList

app_name = 'notifications'

urlpatterns = [
    path('all/', NotificationList.as_view(), name='list-notifications'),
]