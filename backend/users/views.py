from djoser.views import UserViewSet
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import User
from .serializers import UserCreateSerializer
from api.tasks import send_reset_password_email_without_user
from rest_framework.views import APIView


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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