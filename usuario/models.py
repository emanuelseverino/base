from datetime import datetime

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class UsuarioMaganer(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Usuário precisa ter is_superuser=True')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Usuário precisa ter is_staff=True')

        return self._create_user(email, password, **extra_fields)


class CustomUsuario(AbstractUser):
    foto = models.ImageField(upload_to='usuarios', blank=True, null=True)
    email = models.EmailField('e-mail', unique=True)
    celular = models.CharField('celular', max_length=17, unique=True, blank=True, null=True)
    vencimento = models.DateTimeField()
    visivel = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', ]

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.vencimento = timezone.now()
        super().save(*args, **kwargs)


    class Meta:
        ordering = ['first_name', 'last_name']

    objects = UsuarioMaganer()
