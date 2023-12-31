# Generated by Django 4.0 on 2023-10-15 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_for_front', '0045_alter_step_responsible_persons_scheme'),
    ]

    operations = [
        migrations.AddField(
            model_name='step',
            name='active',
            field=models.BooleanField(default=False, verbose_name='В процессе'),
        ),
        migrations.AddField(
            model_name='step',
            name='finished',
            field=models.BooleanField(default=False, verbose_name='Завершенность'),
        ),
    ]
