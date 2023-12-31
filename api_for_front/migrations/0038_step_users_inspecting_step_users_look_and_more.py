# Generated by Django 4.0 on 2023-10-05 09:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('api_for_front', '0037_alter_step_noda_front'),
    ]

    operations = [
        migrations.AddField(
            model_name='step',
            name='users_inspecting',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inspecting', to='auth.user', verbose_name='Тот кто проверяет'),
        ),
        migrations.AddField(
            model_name='step',
            name='users_look',
            field=models.ManyToManyField(blank=True, related_name='look', to=settings.AUTH_USER_MODEL, verbose_name='Те кто смотрят'),
        ),
        migrations.AddField(
            model_name='step',
            name='users_responsible',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='responsible', to='auth.user', verbose_name='Тот кто ответственен'),
        ),
    ]
