from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fileds):
        """Creates and saves a new user"""

        if not email:
            raise ValueError('User must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fileds)
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""

        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custon user model that supportsusing email instead of username"""

    email = models.EmailField(max_length=255, unique=True)
    chat_id = models.BigIntegerField(unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self) -> str:
        return self.email


class Budjet(models.Model):
    """Money budjet model"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='budjets',
        on_delete=models.SET_NULL,
        null=True
    )
    name = models.CharField(max_length=255)
    amount = models.IntegerField()

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    """Expense category model"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='cetagories',
        on_delete=models.SET_NULL,
        null=True
    )
    codename = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255)
    aliases = models.TextField()

    def __str__(self) -> str:
        return self.codename


class Expense(models.Model):
    """Base expense model"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='expenses',
        on_delete=models.SET_NULL,
        null=True
    )
    category = models.ForeignKey(
        'Category',
        verbose_name='expenses',
        on_delete=models.SET_NULL,
        null=True
    )
    amount = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    expense_text = models.TextField()

    def __str__(self) -> str:
        return str(self.user)
