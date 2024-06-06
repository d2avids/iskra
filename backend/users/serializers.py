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
        )

    def create(self, validated_data):
        if 'last_name' in validated_data:
            validated_data['last_name'] = validated_data['last_name'].capitalize()
        if 'first_name' in validated_data:
            validated_data['first_name'] = validated_data['first_name'].capitalize()
        if 'patronymic' in validated_data:
            validated_data['patronymic'] = validated_data['patronymic'].capitalize()
        return super().create(validated_data)
    
    def validate(self, attrs):
        if User.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError({
                'email': 'Пользователь с таким email уже существует.'
            })
        return super().validate(attrs)