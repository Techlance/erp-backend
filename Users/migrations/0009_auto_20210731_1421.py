# Generated by Django 3.2.5 on 2021-07-31 08:51

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0008_auto_20210731_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction_right',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 31, 8, 51, 53, 563557, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 31, 8, 51, 53, 558594, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user_group',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 31, 8, 51, 53, 562600, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user_right',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 31, 8, 51, 53, 564559, tzinfo=utc)),
        ),
    ]
