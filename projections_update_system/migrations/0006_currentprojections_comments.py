# Generated by Django 2.2.24 on 2022-03-27 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projections_update_system', '0005_auto_20220324_0137'),
    ]

    operations = [
        migrations.AddField(
            model_name='currentprojections',
            name='comments',
            field=models.CharField(blank=True, max_length=1500, null=True),
        ),
    ]
