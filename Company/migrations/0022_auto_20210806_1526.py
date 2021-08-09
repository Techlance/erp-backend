# Generated by Django 3.2.5 on 2021-08-06 09:56

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0021_auto_20210806_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acc_group',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 6, 9, 55, 46, 923897, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='acc_group_logs',
            name='altered_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 6, 9, 55, 46, 924897, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='acc_head',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 6, 9, 55, 46, 922898, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='acc_head_logs',
            name='altered_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 6, 9, 55, 46, 922898, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='company_master',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 6, 9, 55, 46, 910899, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='company_master_docs',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 6, 9, 55, 46, 916900, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='company_master_docs_logs',
            name='altered_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 6, 9, 55, 46, 917900, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='company_master_docs_logs',
            name='file',
            field=models.FileField(upload_to='files_logs'),
        ),
        migrations.AlterField(
            model_name='company_master_logs',
            name='altered_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 6, 9, 55, 46, 912899, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='cost_category',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 6, 9, 55, 46, 927897, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='cost_category_logs',
            name='altered_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 6, 9, 55, 46, 928899, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='cost_center',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 6, 9, 55, 46, 929897, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='cost_center_logs',
            name='altered_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 6, 9, 55, 46, 930897, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='currency',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 6, 9, 55, 46, 908899, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='currency_logs',
            name='altered_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 6, 9, 55, 46, 909900, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='fixed_account_group',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 6, 9, 55, 46, 931897, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='fixed_account_head',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 6, 9, 55, 46, 931897, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='fixed_ledger_master',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 6, 9, 55, 46, 932897, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='fixed_vouchertype',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 6, 9, 55, 46, 930897, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='ledger_master',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 6, 9, 55, 46, 925897, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='ledger_master_logs',
            name='altered_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 6, 9, 55, 46, 926897, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user_company',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 6, 9, 55, 46, 914899, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user_company_logs',
            name='altered_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 6, 9, 55, 46, 915899, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='voucher_type',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 6, 9, 55, 46, 920898, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='voucher_type_logs',
            name='altered_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 6, 9, 55, 46, 921897, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='year_master',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 6, 9, 55, 46, 918900, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='year_master_logs',
            name='altered_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 6, 9, 55, 46, 919899, tzinfo=utc)),
        ),
    ]