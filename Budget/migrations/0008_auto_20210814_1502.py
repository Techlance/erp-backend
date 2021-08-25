# Generated by Django 3.2.5 on 2021-08-14 09:32

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Budget', '0007_auto_20210814_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 442313, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='budget_cashflow_details',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 461936, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='budget_details',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 445000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='historicalbudget',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 442313, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='historicalbudget_cashflow_details',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 461936, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='historicalbudget_details',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 445000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='historicalrevised_budget_cashflow_details',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 464655, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='historicalrevised_budget_details',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 455630, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='revised_budget_cashflow_details',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 464655, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='revised_budget_details',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 455630, tzinfo=utc)),
        ),
    ]