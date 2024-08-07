from rest_framework import routers
from django.urls import path, include

from api.constants import POST_RESET_PASSWORD
from users.views import CustomUserViewSet, EducationalOrganizationViewSet, UserCertificateViewSet, UserTestAnswerView

router = routers.DefaultRouter()
router.register(r'users/certificates', UserCertificateViewSet, basename='certificates')
router.register(
    r'educational_organizations',
    EducationalOrganizationViewSet,
    basename='educational_organizations'
)
router.register(r'users/me/main-test',  UserTestAnswerView, basename='usertestanswer')


urlpatterns = [
    path(
        'reset_password/',
        CustomUserViewSet.as_view(POST_RESET_PASSWORD),
        name='reset_password'
    ),
    path('', include(router.urls)),
]
