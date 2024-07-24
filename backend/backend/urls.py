from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, UserTestAnswerListView, UserTestAnswerListRetrieveView, UserTestAnswerRetrieveListView


router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    path('api/v1/', include('api.urls')),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.authtoken')),
    path('api/v1/', include(router.urls)),
    path('api/v1/users/me/main-test/', UserTestAnswerListView.as_view(), name='user-test-answer-list'),
    path('api/v1/users/me/main-test/<int:pk>/', UserTestAnswerListRetrieveView.as_view(), name='user-test-answer-retrieve'),
    path('api/v1/users/me/main-test/<int:test_answer_id>/answers/<int:index>/', UserTestAnswerRetrieveListView.as_view(), name='user-test-answer-item-list'),
]
