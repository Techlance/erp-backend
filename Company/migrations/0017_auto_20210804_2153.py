# Generated by Django 3.2.5 on 2021-08-04 16:23

import datetime
from django.db import migrations, models
import django.db.models.expressions
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0016_auto_20210804_2153'),
        ('Company', '0016_auto_20210803_0838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acc_group',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 4, 16, 23, 51, 51868, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='acc_head',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 4, 16, 23, 51, 51868, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='company_master',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 4, 16, 23, 51, 47829, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='company_master_docs',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 4, 16, 23, 51, 49869, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='cost_category',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 4, 16, 23, 51, 53832, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='cost_center',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 4, 16, 23, 51, 53832, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='currency',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 4, 16, 23, 51, 47829, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='fixed_account_group',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 4, 16, 23, 51, 55830, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='fixed_account_head',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 4, 16, 23, 51, 55830, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='fixed_ledger_master',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 4, 16, 23, 51, 55830, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='fixed_vouchertype',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 4, 16, 23, 51, 54831, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='ledger_master',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 4, 16, 23, 51, 52872, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user_company',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 4, 16, 23, 51, 48870, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user_company',
            name='user_group_id',
            field=models.ForeignKey(on_delete=django.db.models.expressions.Case, to='Users.user_group'),
        ),
        migrations.AlterField(
            model_name='voucher_type',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 4, 16, 23, 51, 50892, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='year_master',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 4, 16, 23, 51, 49869, tzinfo=utc)),
        ),
        migrations.AlterUniqueTogether(
            name='cost_center',
            unique_together={('cost_category_id', 'company_master_id')},
        ),
    ]