"""Model User"""
import jwt
import logging
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)
from rest_framework.authtoken.models import Token
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from binance_automation.utils.models import BinanceAutomationModel
from binance_automation.users.manager.user import UserManager
log = logging.getLogger(__name__)


class User(BinanceAutomationModel, AbstractBaseUser, PermissionsMixin):
    """binance_automation User"""

    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(verbose_name='Correo Electrónico', unique=True, db_index=True,
        error_messages={'unique': 'Ya existe un usuario con ese correo electrónico'})
    is_active = models.BooleanField(verbose_name='Activo', default=True)
    is_verify = models.BooleanField(verbose_name='Verify', default=False, help_text='Consigna si el usuario ha verificado su email')
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        """
        A dynamic way to let us get the user's token
        """
        # return self._generate_jwt_token()
        return self._generate_token()


    def _generate_token(self):
        """
        Generates or Create Django Token
        """
        token, _ = Token.objects.get_or_create(user=self)
        return token.key


