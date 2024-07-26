from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreatePasswordRetypeSerializer

from users.constants import PROFESSIONAL_COMPETENCES_VALIDATION_MSG
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
        queryset=EducationalOrganization.objects.all()
    )
    certificates = UserCertificateSerializer(many=True, read_only=True)

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
            'certificates'
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


class LatestUserTestAnswerSerializer(serializers.Serializer):
    previous = UserTestAnswerSerializer()
    current = UserTestAnswerSerializer()
    

class AnswerRetrieveSerializer(serializers.Serializer):
    answer = serializers.IntegerField()