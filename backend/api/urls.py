from rest_framework import routers
from django.urls import path, include

from api.constants import POST_RESET_PASSWORD
from users.views import CustomUserViewSet, EducationalOrganizationViewSet

router = routers.DefaultRouter()
router.register(
    r'educational_organizations',
    EducationalOrganizationViewSet,
    basename='educationl_organization'
)


urlpatterns = [
    path(
        'reset_password/',
        CustomUserViewSet.as_view(POST_RESET_PASSWORD),
        name='reset_password'
    ),
    path('', include(router.urls)),
]
