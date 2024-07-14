from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from djoser.views import UserViewSet
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, filters
from users.serializers import (EmailSerializer,
                               EducationalOrganizationSerializer)
from rest_framework import permissions


from users.models import User, EducationalOrganization
from users.mixins import ListRetrieveViewSet
from api.tasks import send_reset_password_email_without_user


class EducationalOrganizationViewSet(ListRetrieveViewSet):
    """Представляет должности для юзеров.

    Доступны только операции чтения.
    """

    queryset = EducationalOrganization.objects.all()
    serializer_class = EducationalOrganizationSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    ordering = ('name',)

    @method_decorator(cache_page(settings.EDUCATIONAL_ORGANIZATIONS_LIST_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


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
