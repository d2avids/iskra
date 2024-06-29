from django.urls import path
from rest_framework.routers import DefaultRouter
from users.views import CustomUserViewSet, UserRegistrationView

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
] + router.urls
