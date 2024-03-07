# Generated by Django 4.0 on 2022-03-11 01:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('data_upload_system', '0006_accountparentlevele'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectionsUpdateLog',
            fields=[
                ('accE', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('org', models.CharField(max_length=50)),
                ('byUserName', models.CharField(max_length=50)),
                ('fromValue', models.IntegerField()),
                ('toValue', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CurrentProjections',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projection', models.FloatField(default=0)),
                ('accE', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_upload_system.accountparentlevele')),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_upload_system.organization')),
            ],
        ),
    ]
