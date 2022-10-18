from django.db import models
from accounts.models import CustomUser
from datetime import datetime


class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    # link = models.CharField(max_length = 200)
    date = models.DateTimeField(auto_now_add=True)
