# Generated by Django 5.0.6 on 2024-07-26 08:49

import django.db.models.deletion
import users.utils
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='achievements',
            field=models.TextField(blank=True, null=True, verbose_name='Достижения'),
        ),
        migrations.AddField(
            model_name='user',
            name='competitions',
            field=models.TextField(blank=True, null=True, verbose_name='Конкурсы'),
        ),
        migrations.AddField(
            model_name='user',
            name='professional_interests',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Профессиональные интересы'),
        ),
        migrations.AddField(
            model_name='user',
            name='specialty',
            field=models.TextField(blank=True, null=True, verbose_name='Специальность'),
        ),
        migrations.CreateModel(
            name='UserCertificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certificate', models.FileField(upload_to=users.utils.users_files_path, verbose_name='Сертификат')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certificates', to=settings.AUTH_USER_MODEL, verbose_name='Сертификаты')),
            ],
            options={
                'verbose_name': 'Сертификат пользователя',
                'verbose_name_plural': 'Сертификаты пользователей',
            },
        ),
    ]
