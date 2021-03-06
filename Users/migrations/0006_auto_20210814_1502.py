# Generated by Django 3.2.5 on 2021-08-14 09:32

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0005_auto_20210814_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaluser',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 244551, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='historicaluser_group',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 254632, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='historicaluser_right',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 259377, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transaction_right',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 256667, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 244551, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user_group',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 254632, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user_right',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 14, 9, 32, 2, 259377, tzinfo=utc)),
        ),
    ]
