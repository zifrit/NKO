# Generated by Django 4.0 on 2023-10-19 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_for_front', '0071_alter_stepimages_link_main_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='steptemplates',
            name='template_main_project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api_for_front.templatemainko', verbose_name='Шаблон КО'),
            preserve_default=False,
        ),
    ]
