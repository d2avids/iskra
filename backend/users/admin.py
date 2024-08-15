from django.contrib import admin
from django.contrib.auth.models import Group
from django.conf import settings
from rest_framework.authtoken.models import TokenProxy
import openpyxl
from django.http import HttpResponse

from users.models import User, EducationalOrganization, UserCertificate, UserTestAnswer


class CertificateAdmin(admin.StackedInline):
    model = UserCertificate
    extra = 0



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
    inlines = [CertificateAdmin]


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


@admin.register(UserTestAnswer)
class TestAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user_email', 'get_user_id')
    search_fields = ('user__email',)
    actions = ['export_to_excel']

    def get_user_id(self, obj):
        return obj.user.id
    
    def get_user_email(self, obj):
        return obj.user.email

    def export_to_excel(self, request, queryset):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = 'Test Answers'

        headers = [
            '№',
            'user id',
            'email',
            'ERM',
            'TMM',
            'SS',
            'ERS',
            'TMS',
            'EMP',
            'ERI',
            'PL',
            'PRO',
            'SF',
            'IMP',
            'NEU',
            'CNTL'
        ]
        sheet.append(headers)

        for index, obj in enumerate(queryset, start=1):
            answers = obj.answers
            erm = answers[0] if len(answers) > 0 else ''
            tmm = answers[1] if len(answers) > 1 else ''
            ss = answers[2] if len(answers) > 2 else ''
            ers = answers[3] if len(answers) > 3 else ''
            tms = answers[4] if len(answers) > 4 else ''
            emp = answers[5] if len(answers) > 5 else ''
            eri = answers[6] if len(answers) > 6 else ''
            pl = answers[7] if len(answers) > 7 else ''
            pro = answers[8] if len(answers) > 8 else ''
            sf = answers[9] if len(answers) > 9 else ''
            imp = answers[10] if len(answers) > 10 else ''
            neu = answers[11] if len(answers) > 11 else ''
            cntl = answers[12] if len(answers) > 12 else ''

            row = [
                index,
                obj.user.id,
                obj.user.email,
                erm,
                tmm,
                ss,
                ers,
                tms,
                emp,
                eri,
                pl,
                pro,
                sf,
                imp,
                neu,
                cntl
            ]
            sheet.append(row)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=test_answers.xlsx'

        workbook.save(response)
        return response