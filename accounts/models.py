from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


# Create your models here.
class MyUserManager(UserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email))

        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    last_modified = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    objects = MyUserManager()

    def __str__(self):
        return self.username
