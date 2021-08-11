# Generated by Django 3.2.5 on 2021-08-11 09:50

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0025_auto_20210811_0105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction_right',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 11, 9, 50, 29, 361719, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 11, 9, 50, 29, 358726, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user_group',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 11, 9, 50, 29, 360722, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user_group_logs',
            name='altered_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 11, 9, 50, 29, 361719, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user_logs',
            name='altered_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 11, 9, 50, 29, 360722, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user_right',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 11, 9, 50, 29, 361719, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user_right_logs',
            name='altered_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 11, 9, 50, 29, 362716, tzinfo=utc)),
        ),
    ]
