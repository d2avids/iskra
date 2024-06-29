from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    

class User(AbstractUser):
    username = None
    email = models.EmailField(
        verbose_name='Email',
        unique=True,
        max_length=254,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=30
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=30
    )
    patronymic = models.CharField(
        verbose_name='Отчество',
        max_length=40,
        blank=True,
        null=True
    )
    data_processing_agreement = models.BooleanField(
        verbose_name='Согласие на обработку персональных данных',
        default=True
    )
    confidential_policy_agreement = models.BooleanField(
        verbose_name='Согласие с политикой конфиденциальности',
        default=True
    )

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    class Meta:
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'

    def __str__(self):
        return f'Пользователь {self.first_name}'
