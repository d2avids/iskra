# Generated by Django 5.0.6 on 2024-09-07 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='professional_interests',
            field=models.JSONField(blank=True, default=dict, max_length=255, null=True, verbose_name='Профессиональные интересы'),
        ),
    ]
