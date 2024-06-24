from rest_framework import serializers
from .models import User
from djoser.serializers import UserCreatePasswordRetypeSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'last_name',
            'first_name',
            'username',
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
            'username',
            'patronymic',
            'password',
        )

    def create(self, validated_data):
        if 'last_name' in validated_data:
            validated_data['last_name'] = validated_data['last_name'].capitalize()
        if 'first_name' in validated_data:
            validated_data['first_name'] = validated_data['first_name'].capitalize()
        if 'username' in validated_data:
            validated_data['username'] = validated_data['username'].capitalize()
        if 'patronymic' in validated_data:
            validated_data['patronymic'] = validated_data['patronymic'].capitalize()
        return super().create(validated_data)

class SafeUserSerializer(UserSerializer):
    class Meta:
        ref_name = 'safe_user'
        model = User
        fields = (
            'id',
            'email',
            'last_name',
            'first_name',
            'username',
            'patronymic',
            'data_processing_agreement',
            'confidential_policy_agreement',
        )