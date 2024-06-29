from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreatePasswordRetypeSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'last_name',
            'first_name',
            'patronymic',
            'data_processing_agreement',
            'confidential_policy_agreement',
        )


class UserCreateSerializer(UserCreatePasswordRetypeSerializer):
    class Meta(UserCreatePasswordRetypeSerializer.Meta):
        model = User
        fields = (
            'email',
            'last_name',
            'first_name',
            'patronymic',
            'password',
            're_password',
            'data_processing_agreement',
            'confidential_policy_agreement',
        )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Пользователь с таким email уже существует.')
        return value

    def create(self, validated_data):
        validated_data['last_name'] = validated_data['last_name'].capitalize()
        validated_data['first_name'] = validated_data['first_name'].capitalize()
        validated_data['patronymic'] = validated_data.get('patronymic', '').capitalize()

        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            patronymic=validated_data['patronymic'],
            data_processing_agreement=validated_data['data_processing_agreement'],
            confidential_policy_agreement=validated_data['confidential_policy_agreement']
        )
        return user
