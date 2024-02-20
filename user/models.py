from datetime import datetime
from typing import Optional
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def _create_user(self, username: str= None, password: str= '',date_joined=timezone.now(), **extra_fields):
        if not username:
            raise ValueError("Ajouter un nom d'utilisateur valide")

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username: str = None, password: str = '', date_joined=timezone.now(),**extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(username, password, extra_fields)

    def create_superuser(self, username: str = None, password: str = '',date_joined=timezone.now() ,**extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(username, password, extra_fields)
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, blank=True, unique=True)
    first_name = models.CharField(max_length=200, blank=True, default='')
    last_name = models.CharField(max_length=200, blank=True, default='')
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=datetime.now())
    last_login = models.DateTimeField(blank=True, null=True)
    image=models.ImageField(upload_to='images/')

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'  #

    REQUIRED_FIELDS = ['email'] 

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_full_name(self) -> Optional[str]:
        return self.username

    def get_short_name(self) -> Optional[str]:
        return self.username.split('@')[0]
    















