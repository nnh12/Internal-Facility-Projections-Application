# Generated by Django 4.0 on 2022-03-11 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_upload_system', '0005_alter_record_upload_id_alter_uploadhistory_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountParentLevelE',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]
