# Generated by Django 3.2.5 on 2021-08-14 09:32

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0006_auto_20210814_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acc_group',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 348189, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='acc_head',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 347191, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='company_master',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 313988, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='company_master_docs',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 325741, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='cost_category',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 368236, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='cost_center',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 372120, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='currency',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 309156, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='fixed_account_group',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 374863, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='fixed_account_head',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 374863, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='fixed_ledger_master',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 382059, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='fixed_vouchertype',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 374863, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='historicalacc_group',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 348189, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='historicalacc_head',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 347191, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='historicalcompany_master',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 313988, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='historicalcompany_master_docs',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 325741, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='historicalcost_category',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 368236, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='historicalcost_center',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 372120, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='historicalcurrency',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 309156, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='historicalledger_master',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 361030, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='historicaluser_company',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 323116, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='historicalvoucher_type',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 339746, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='historicalyear_master',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 325741, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='ledger_master',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 361030, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user_company',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 323116, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='voucher_type',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 339746, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='year_master',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 325741, tzinfo=utc)),
        ),
        migrations.AlterUniqueTogether(
            name='cost_center',
            unique_together={('cost_center_name', 'company_master_id')},
        ),
    ]
