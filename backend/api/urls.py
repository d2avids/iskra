from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import SafeUserViewSet, CustomUserViewSet, UserRegistrationView

router = DefaultRouter()
router.register(r'safe_users', SafeUserViewSet, basename='safe_users')
router.register(r'users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
] + router.urls