# Generated by Django 4.0 on 2023-10-03 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('my_user', '0005_userprofile_is_chief'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='chief_department',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chief', to='auth.group', verbose_name='Отдел которым руководит'),
        ),
    ]
