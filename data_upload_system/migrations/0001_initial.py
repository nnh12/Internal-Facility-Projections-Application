# Generated by Django 4.0 on 2022-02-17 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fiscal_year', models.PositiveSmallIntegerField()),
                ('month', models.CharField(max_length=9)),
                ('fund_type_parent_level_A', models.CharField(max_length=50)),
                ('fund_type_parent_level_B', models.CharField(max_length=50)),
                ('fund_type', models.CharField(max_length=50)),
                ('fund_source_parent_level_C', models.CharField(max_length=50)),
                ('fund_source_parent_level_D', models.CharField(max_length=50)),
                ('fund_source', models.CharField(max_length=50)),
                ('organization_parent_level_B', models.CharField(max_length=50)),
                ('organization_parent_level_C', models.CharField(max_length=50)),
                ('organization_parent_level_D', models.CharField(max_length=50)),
                ('organization_parent_level_E', models.CharField(max_length=50)),
                ('organization', models.CharField(max_length=50)),
                ('account_parent_level_B', models.CharField(max_length=50)),
                ('account_parent_level_C', models.CharField(max_length=50)),
                ('account_parent_level_D', models.CharField(max_length=50)),
                ('account_parent_level_E', models.CharField(max_length=50)),
                ('account', models.CharField(max_length=50)),
                ('budget_amount', models.FloatField()),
                ('actual_YTD_beginning_of_period', models.FloatField()),
                ('period_net', models.FloatField()),
                ('actual_YTD_end_of_period', models.FloatField()),
                ('PO_Req_other_encumbrances', models.FloatField()),
                ('salary_encumbrance', models.FloatField()),
                ('remaining_budget', models.FloatField()),
                ('program', models.CharField(max_length=20)),
                ('activity', models.CharField(max_length=20)),
                ('location', models.CharField(max_length=20)),
            ],
        ),
    ]