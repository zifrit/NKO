# Generated by Django 3.2.5 on 2023-04-09 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_for_front', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='maintableko',
            name='stages',
            field=models.ManyToManyField(to='api_for_front.KoStage', verbose_name='Список Этапов'),
        ),
    ]
