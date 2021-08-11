# Generated by Django 3.2.5 on 2021-08-10 19:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0023_auto_20210807_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction_right',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 10, 19, 30, 47, 203665, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 10, 19, 30, 47, 191697, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user_group',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 10, 19, 30, 47, 200666, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user_group_logs',
            name='altered_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 10, 19, 30, 47, 201716, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user_logs',
            name='altered_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 10, 19, 30, 47, 198671, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user_right',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 10, 19, 30, 47, 205019, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user_right_logs',
            name='altered_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 10, 19, 30, 47, 206564, tzinfo=utc)),
        ),
    ]
