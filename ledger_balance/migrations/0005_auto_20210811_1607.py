# Generated by Django 3.2.5 on 2021-08-11 10:37

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ledger_balance', '0004_auto_20210811_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ledger_bal_billwise',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 11, 10, 37, 35, 654422, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='ledger_balance',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 11, 10, 37, 35, 654422, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='op_bal_brs',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 11, 10, 37, 35, 666476, tzinfo=utc)),
        ),
    ]
