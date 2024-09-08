from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField

from users.constants import PROFESSIONAL_COMPETENCES_VALIDATION_MSG, PROFESSIONAL_INTERESTS_VALIDATION_MSG
from users.utils import users_files_path


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


class EducationalOrganization(models.Model):
    name = models.TextField(
        verbose_name='Наименование образовательной организации'
    )

    class Meta:
        verbose_name_plural = 'Образовательные организации'
        verbose_name = 'Образовательная организация'

    def __str__(self):
        return self.name
    

class User(AbstractUser):
    username = None
    email = models.EmailField(
        verbose_name='Email',
        unique=True,
        max_length=254,
    )
    photo = models.ImageField(
        verbose_name='Фото',
        upload_to=users_files_path,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=30,
        blank=True,
        null=True
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=30,
        blank=True,
        null=True
    )
    phone_number = PhoneNumberField(
        region='RU',
        blank=True,
        null=True
    )
    patronymic = models.CharField(
        verbose_name='Отчество',
        max_length=40,
        blank=True,
        null=True
    )
    telegram = models.CharField(
        verbose_name='Telegram',
        max_length=45,
        blank=True,
        null=True
    )
    professional_competencies = models.JSONField(
        verbose_name='Профессиональные компетенции',
        default=dict,
        blank=True,
        null=True
    )
    professional_interests = models.JSONField(
        max_length=255,
        verbose_name='Профессиональные интересы',
        default=dict,
        blank=True,
        null=True
    )
    specialty = models.TextField(
        verbose_name='Специальность',
        blank=True,
        null=True
    )
    achievements = models.TextField(
        verbose_name='Достижения',
        blank=True,
        null=True
    )
    competitions = models.TextField(
        verbose_name='Конкурсы',
        blank=True,
        null=True
    )
    educational_organization = models.ForeignKey(
        to='EducationalOrganization',
        verbose_name='Образование',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    competencies = models.TextField(
        verbose_name='Компетенции',
        blank=True,
        null=True
    )
    data_processing_confidential_policy_agreement = models.BooleanField(
        verbose_name='Согласие на обработку персональных '
                     'данных и политикой конфиденциальности',
        default=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=20,
        choices=(
            ('student', 'Студент'),
            ('teacher', 'Преподаватель'),
            ('director', 'Руководитель'),
            ('parent', 'Родитель'),
        ),
        default='student'
    )

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    class Meta:
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'

    def __str__(self):
        return self.email

    def clean(self):
        if (
                self.professional_competencies and self.professional_competencies not in ('[]', '{}')
                and not isinstance(self.professional_competencies, list)
        ):
            raise ValidationError(PROFESSIONAL_COMPETENCES_VALIDATION_MSG)
        if(
                self.professional_interests and self.professional_interests not in ('[]', '{}')
                and not isinstance(self.professional_interests, list)
        ):
            raise ValidationError(PROFESSIONAL_INTERESTS_VALIDATION_MSG)


class UserCertificate(models.Model):
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='certificates',
        verbose_name='Сертификаты'
    )
    certificate = models.FileField(
        verbose_name='Сертификат',
        upload_to=users_files_path
    )

    def __str__(self):
        return f'Сертификат id {self.id} пользователя id {self.user.id}'

    class Meta:
        verbose_name_plural = 'Сертификаты пользователей'
        verbose_name = 'Сертификат пользователя'


class UserTestAnswer(models.Model):
    user = models.ForeignKey(
        to='User',
        verbose_name='Пользователь',
        on_delete=models.CASCADE
    )
    answers = models.JSONField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Ответы на тест'
        verbose_name = 'Ответы на тест'
        ordering = ['-created', '-id']

    def __str__(self):
        return f'Ответы пользователя {self.user.email} {self.created}'
