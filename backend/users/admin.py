from django.contrib import admin
from django.contrib.auth.models import Group
from django.conf import settings
from rest_framework.authtoken.models import TokenProxy

from users.models import User, EducationalOrganization


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'first_name',
        'last_name',
        'patronymic',
        'photo',
        'phone_number',
        'telegram',
        'data_processing_confidential_policy_agreement',
    )
    search_fields = (
        'email',
        'first_name',
        'last_name',
        'patronymic',
        'phone_number',
        'telegram'
    )


@admin.register(EducationalOrganization)
class EducationalOrganizationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name'
    )
    search_fields = ('name',)


admin.site.unregister(Group)
if not settings.DEBUG:
    admin.site.unregister(TokenProxy)
