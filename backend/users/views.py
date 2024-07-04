from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from users.serializers import EmailSerializer
from .serializers import UserSerializer
from .premissions import IsUserOrReadOnly
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied

from .models import User
from api.tasks import send_reset_password_email_without_user


class CustomUserViewSet(UserViewSet):
    """Кастомный вьюсет юзера.
    Доступно изменение метода сброса пароля reset_password
    """

    @action(
            methods=['post'],
            detail=False,
            permission_classes=(permissions.AllowAny,),
            serializer_class=EmailSerializer,
    )
    def reset_password(self, request, *args, **kwargs):
        """
        POST-запрос с адресом почты в json`е
        высылает ссылку на почту на подтвеждение смены пароля.
        Вид ссылки в письме:
        'https://<домен>/password/reset/confirm/{uid}/{token}'
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        try:
            User.objects.get(email__iexact=data.get('email'))
            send_reset_password_email_without_user.delay(data=data)
            return Response(status=status.HTTP_200_OK)
        except (User.DoesNotExist, AttributeError):
            return Response(
                {'detail': (
                    'Нет пользователя с введенным email или опечатка в адресе.'
                )},
                status=status.HTTP_204_NO_CONTENT
            )
        except User.MultipleObjectsReturned:
            return Response(
                {'detail': (
                    'В БД несколько юзеров с одним адресом почты.'
                    ' Отредактируйте дубликаты и повторите попытку.'
                )},
                status=status.HTTP_409_CONFLICT
            )
        

class UserDetailViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserOrReadOnly]

    def get_queryset(self):
        return self.queryset
    
    def perform_update(self, serializer):
        if serializer.instance != self.request.user:
            raise PermissionDenied("У вас недостаточно прав, для изменения информации другого пользователя")
        serializer.save()

    def perform_destroy(self, instance):
        if instance != self.request.user:
            raise PermissionDenied("У вас недостаточно прав, для удаления информации другого пользователя")
        instance.delete()