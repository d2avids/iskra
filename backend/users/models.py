from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

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
    username = models.CharField(
        verbose_name='Ник нейм',
        max_length=30,
        unique=True
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

    class Meta:
        verbose_name = 'Пользователь'

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.email and User.objects.exclude(pk=self.pk).filter(
                email__iexact=self.email
        ).exists():
            raise ValidationError('Данный Email уже зарегистрирован.')

    def __str__(self):
        return f'Пользователь {self.user_name} '

