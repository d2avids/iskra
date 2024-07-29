from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from djoser.views import UserViewSet
import djoser.serializers
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotFound, ValidationError


from users.serializers import (EmailSerializer,
                               EducationalOrganizationSerializer, UserCertificateSerializer,
                               UserTestAnswerSerializer, AnswerRetrieveSerializer)
from rest_framework import permissions, generics
from rest_framework.pagination import PageNumberPagination


from users.models import User, EducationalOrganization, UserCertificate, UserTestAnswer
from users.mixins import ListRetrieveViewSet, ListRetrieveCreateDeleteViewSet, ListRetrieveCreateViewSet
from api.tasks import send_reset_password_email_without_user
from django.utils.timezone import now


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


class UserCertificateViewSet(ListRetrieveCreateDeleteViewSet):
    """Для работы с сертификатами юзера.

    Авторизованный имеет доступ к получению и удалению только своих сертификатов.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserCertificateSerializer

    def get_queryset(self):
        return UserCertificate.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CustomUserViewSet(UserViewSet):
    """Кастомный вьюсет юзера.

    Изменен метод сброса пароля reset_password
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


class TestPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserTestAnswerView(ListRetrieveCreateViewSet):
    serializer_class = UserTestAnswerSerializer
    pagination_class = TestPagination
    permission_classes = (permissions.IsAuthenticated,)

    @method_decorator(cache_page(settings.TEST_ANSWER_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        return UserTestAnswer.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        last_answer = UserTestAnswer.objects.filter(user=user).order_by('-created').first()
        if last_answer and (now() - last_answer.created).days < 120: 
            raise ValidationError("Тест можно пройти раз в 4 месяца.")
        serializer.save(user=user)

    @action(detail=False, methods=['get'], url_path='latest')
    def get_latest(self, request):
        user = request.user
        latest_answers = UserTestAnswer.objects.filter(user=user).order_by('-created')[:2]
        if len(latest_answers) == 2:
            previous_answers = latest_answers[1]
            current_answers = latest_answers[0]
        elif len(latest_answers) == 1:
            previous_answers = None
            current_answers = latest_answers[0]
        else:
            previous_answers = None
            current_answers = None
        response_data = {
            "previous": UserTestAnswerSerializer(previous_answers).data if previous_answers else None,
            "current": UserTestAnswerSerializer(current_answers).data if current_answers else None
        }
        return Response(response_data)

    @action(detail=True, methods=['get'], url_path='answers/(?P<index>[^/.]+)')
    def get_answer(self, request, pk=None, index=None):
        try:
            test_answer = self.get_object()
        except UserTestAnswer.DoesNotExist:
            raise NotFound('Test answer not found.')
        try:
            index = int(index)
            answer = test_answer.answers[index]
        except (IndexError, ValueError):
            raise NotFound('Answer index out of range.')
        serializer = AnswerRetrieveSerializer({'answer': answer})
        return Response(serializer.data)