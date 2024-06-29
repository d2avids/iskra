from django.urls import path
from api.constants import POST_RESET_PASSWORD
from users.views import CustomUserViewSet

urlpatterns = [
    path(
        'reset_password/',
        CustomUserViewSet.as_view(POST_RESET_PASSWORD),
        name='reset_password'
    ),
]
