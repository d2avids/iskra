from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreatePasswordRetypeSerializer

from users.constants import PROFESSIONAL_COMPETENCES_VALIDATION_MSG

User = get_user_model()


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'photo',
            'last_name',
            'first_name',
            'patronymic',
            'phone_number',
            'telegram',
            'educational_organization',
            'professional_competencies',
            'competencies',
        )

    def validate_professional_competencies(self, value):
        if isinstance(value, list):
            return value
        raise serializers.ValidationError(
            PROFESSIONAL_COMPETENCES_VALIDATION_MSG
        )


class UserCreateSerializer(UserCreatePasswordRetypeSerializer):
    class Meta(UserCreatePasswordRetypeSerializer.Meta):
        model = User
        fields = (
            'email',
            'password',
        )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Пользователь с таким email уже существует.')
        return value
