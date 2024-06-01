from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    EMAIL_FIELD = 'email'
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
