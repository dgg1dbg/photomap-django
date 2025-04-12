from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    objects = CustomUserManager()
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']