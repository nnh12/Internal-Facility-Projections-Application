# Generated by Django 4.0 on 2022-03-24 17:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('projections_update_system', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectionsupdatelog',
            name='time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
