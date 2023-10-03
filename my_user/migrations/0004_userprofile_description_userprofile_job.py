# Generated by Django 4.0 on 2023-10-03 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_user', '0003_alter_userprofile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='description',
            field=models.TextField(blank=True, verbose_name='Доп.Инфо'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='job',
            field=models.CharField(choices=[('Frontend', 'Frontend'), ('Backend', 'Backend')], default='Frontend', max_length=20, verbose_name='Должность'),
        ),
    ]