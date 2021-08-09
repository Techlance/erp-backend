# Generated by Django 3.2.5 on 2021-07-31 08:51

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0009_auto_20210731_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acc_group',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 31, 8, 51, 53, 571671, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='acc_head',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 31, 8, 51, 53, 571671, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='company_master',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 31, 8, 51, 53, 567677, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='company_master_docs',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 31, 8, 51, 53, 568673, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='currency',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 31, 8, 51, 53, 566670, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='ledger_master',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 31, 8, 51, 53, 573675, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user_company',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 31, 8, 51, 53, 568673, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='voucher_type',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 31, 8, 51, 53, 570669, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='year_master',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 31, 8, 51, 53, 569670, tzinfo=utc)),
        ),
    ]