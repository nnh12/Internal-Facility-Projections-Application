# Generated by Django 4.0 on 2022-02-22 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_upload_system', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='month',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
