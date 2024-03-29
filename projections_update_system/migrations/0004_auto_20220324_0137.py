# Generated by Django 2.2.24 on 2022-03-24 06:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projections_update_system', '0003_projectionsupdatelog_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectionsupdatelog',
            name='id',
            field=models.AutoField(auto_created=True, default=None, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='projectionsupdatelog',
            name='accE',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_upload_system.AccountParentLevelE'),
        ),
    ]
