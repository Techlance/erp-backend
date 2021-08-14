# Generated by Django 3.2.5 on 2021-08-14 07:51

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Budget', '0005_auto_20210813_0859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 7, 51, 27, 138984, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='budget_cashflow_details',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 7, 51, 27, 153348, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='budget_details',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 7, 51, 27, 140408, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='historicalbudget',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 7, 51, 27, 138984, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='historicalbudget_cashflow_details',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 7, 51, 27, 153348, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='historicalbudget_details',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 7, 51, 27, 140408, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='historicalrevised_budget_cashflow_details',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 7, 51, 27, 158950, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='historicalrevised_budget_details',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 7, 51, 27, 148810, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='revised_budget_cashflow_details',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 7, 51, 27, 158950, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='revised_budget_details',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 7, 51, 27, 148810, tzinfo=utc)),
        ),
    ]
