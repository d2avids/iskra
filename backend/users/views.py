from django.shortcuts import render
from djoser.views import UserViewSet
from rest_framework.response import Response, permissions
from api.tasks import send_reset_password_email_without_user
from users.models import User
from rest_framework import status
from users.serializers import SafeUserSerializer

class CustomUserViewSet(UserViewSet):
    def reset_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            User.objects.get(email__iexact=data.get('email'))
            send_reset_password_email_without_user.delay(data=data)
            return Response(status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {'detail': 'Пользователь с введённым email не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
        except User.MultipleObjectsReturned:
            return Response(
                {'detail': 'Найдено несколько пользователей с данным email'},
                status=status.HTTP_409_CONFLICT
            )
        
class SafeUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = SafeUserSerializer
    permission_classes = (permissions.IsAuthenticated,)
