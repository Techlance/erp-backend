# Generated by Django 3.2.5 on 2021-08-14 17:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('lc', '0006_auto_20210814_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicallc',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 17, 14, 54, 302761, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='historicallc_amend',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 17, 14, 54, 311844, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='historicallc_docs',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 17, 14, 54, 307748, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='lc',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 17, 14, 54, 302761, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='lc_amend',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 17, 14, 54, 311844, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='lc_docs',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 17, 14, 54, 307748, tzinfo=utc)),
        ),
    ]
