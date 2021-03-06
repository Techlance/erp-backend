# Generated by Django 3.2.5 on 2021-08-14 09:32

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ledger_balance', '0005_auto_20210814_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalledger_bal_billwise',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 422043, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='historicalledger_balance',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 413313, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='historicalop_bal_brs',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 429956, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='ledger_bal_billwise',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 422043, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='ledger_balance',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 413313, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='op_bal_brs',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 429956, tzinfo=utc)),
        ),
    ]
