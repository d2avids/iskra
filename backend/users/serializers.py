from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreatePasswordRetypeSerializer
from datetime import datetime, timedelta

from users.constants import PROFESSIONAL_COMPETENCES_VALIDATION_MSG, PROFESSIONAL_INTERESTS_VALIDATION_MSG
from users.models import EducationalOrganization, UserCertificate, UserTestAnswer

User = get_user_model()


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)


class UserCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCertificate
        fields = ('id', 'certificate')


class UserSerializer(serializers.ModelSerializer):
    educational_organization = serializers.PrimaryKeyRelatedField(
        queryset=EducationalOrganization.objects.all(),
        allow_null=True,
        required=False,
    )
    certificates = UserCertificateSerializer(many=True, read_only=True, required=False, allow_null=True)

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
            'professional_interests',
            'competencies',
            'specialty',
            'achievements',
            'competitions',
            'certificates',
            'role',
            'email'
        )
        read_only_fields = ('email',)

    def validate_professional_competencies(self, value):
        if isinstance(value, list):
            return value
        raise serializers.ValidationError(
            PROFESSIONAL_COMPETENCES_VALIDATION_MSG
        )
    
    def validate_professional_interests(self, value):
        if isinstance(value, list):
            return value
        raise serializers.ValidationError(
            PROFESSIONAL_INTERESTS_VALIDATION_MSG
        )

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        if repr['professional_interests'] in ({}, '{}', [], '[]'):
            repr['professional_interests'] = None
        if repr['professional_competencies'] in ({}, '{}', [], '[]'):
            repr['professional_competencies'] = None
        return repr


class UserCreateSerializer(UserCreatePasswordRetypeSerializer):
    class Meta(UserCreatePasswordRetypeSerializer.Meta):
        model = User
        fields = (
            'email',
            'password',
        )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует.'
            )
        return value


class EducationalOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationalOrganization
        fields = (
            'id',
            'name'
        )


class UserTestAnswerSerializer(serializers.ModelSerializer):
    answers = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        model = UserTestAnswer
        fields = (
            'id',
            'answers',
            'created'
        )

    def validate(self, data):
        user = self.context['request'].user
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        attempts_today = UserTestAnswer.objects.filter(user=user, created__range=(today_start, today_end)).count()
        self.context['attempts_today'] = attempts_today

        if attempts_today >= 10:
            raise serializers.ValidationError("Тест можно пройти не более 10 раз в день.")
        return data


class AnswerRetrieveSerializer(serializers.Serializer):
    answer = serializers.IntegerField()

    
class CustomUserDeleteSerializer(serializers.Serializer):
    pass

