from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.utils.timezone import now

from django.utils.timezone import now

from django.utils.text import slugify
import uuid

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that suppors using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'


class Restaurant(models.Model):
    """Restaurant to be used for a menu"""
    name = models.CharField(max_length=255)
    last_updated = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(default=now, editable=True)

    def __str__(self):
        return self.name


class Vote(models.Model):
    """Vote to be used to define winner of day"""
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    date = models.DateField(default=date.today, editable=True)

    last_updated = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(default=now, editable=True)
    # def __str__(self):
    #     return self.id


class Menu(models.Model):
    """Menu object"""
    restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    items = models.CharField(max_length=255, default=None, blank=True, null=True)
    date = models.DateField(default=date.today, editable=True)
    winner = models.BooleanField(default=False)

    last_updated = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(default=now, editable=True)
    def __str__(self):
        return self.name
