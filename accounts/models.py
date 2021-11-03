from decimal import Decimal

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.utils.translation import gettext_lazy as _


class MyAccountManager(BaseUserManager):
    """ Custom User Manager """

    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)
        return user


class Account(AbstractUser):
    """ Custom User model """

    username = None
    email = models.EmailField(verbose_name=_('email'), max_length=60, unique=True)
    first_name = models.CharField(verbose_name=_('first name'), max_length=150, blank=True)
    last_name = models.CharField(verbose_name=_('last name'), max_length=150, blank=True)
    balance = models.DecimalField(
        max_digits=8, decimal_places=2,
        verbose_name=_('balance'),
        default=Decimal(0)
    )
    date_joined = models.DateTimeField(verbose_name=_('date joined'), auto_now_add=True)
    last_login = models.DateTimeField(verbose_name=_('last login'), auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    hide_email = models.BooleanField(default=True)

    objects = MyAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
