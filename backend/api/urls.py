from django.urls import include, path
from djoser.views import UserViewSet
from users.views import SafeUserViewSet, CustomUserViewSet
from rest_framework.routers import DefaultRouter
from api.constansions import CREATE_METHOD, POST_RESET_PASSWORD

router = DefaultRouter()

router.register(r'save_user', SafeUserViewSet, basename='save_users')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('register/', UserViewSet.as_view(CREATE_METHOD), name='user-create'),
    path('reset_password/', CustomUserViewSet.as_view(POST_RESET_PASSWORD),name='reset_password'),
]