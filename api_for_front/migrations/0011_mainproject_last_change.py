# Generated by Django 3.2.5 on 2023-07-22 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_for_front', '0010_auto_20230722_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainproject',
            name='last_change',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='последние изменения'),
        ),
    ]