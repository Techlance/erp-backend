# Generated by Django 3.2.5 on 2021-08-07 10:35

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0022_auto_20210807_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction_right',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 7, 10, 35, 42, 122206, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 7, 10, 35, 42, 119215, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user_group',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 7, 10, 35, 42, 121225, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user_group_logs',
            name='altered_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 7, 10, 35, 42, 121225, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user_logs',
            name='altered_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 7, 10, 35, 42, 121225, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user_right',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 7, 10, 35, 42, 122206, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user_right_logs',
            name='altered_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 7, 10, 35, 42, 122206, tzinfo=utc)),
        ),
    ]
