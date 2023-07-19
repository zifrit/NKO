# Generated by Django 3.2.5 on 2023-07-19 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_for_front', '0002_auto_20230719_1631'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectfiles',
            name='link_step',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='step_files', to='api_for_front.step', verbose_name='связь с этапом'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='projectfiles',
            name='link_main_project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_files', to='api_for_front.mainproject', verbose_name='связь с проектом'),
        ),
    ]
