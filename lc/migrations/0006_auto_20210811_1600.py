# Generated by Django 3.2.5 on 2021-08-11 10:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('lc', '0005_auto_20210811_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lc',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 11, 10, 30, 38, 697875, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='lc_amend',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 11, 10, 30, 38, 700867, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='lc_amend_logs',
            name='altered_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 11, 10, 30, 38, 700867, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='lc_docs',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 11, 10, 30, 38, 698912, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='lc_docs_logs',
            name='altered_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 11, 10, 30, 38, 699879, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='lc_logs',
            name='altered_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 11, 10, 30, 38, 697875, tzinfo=utc)),
        ),
    ]
