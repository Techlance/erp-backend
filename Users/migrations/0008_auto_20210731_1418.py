# Generated by Django 3.2.5 on 2021-07-31 08:48

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0007_auto_20210729_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction_right',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 31, 8, 47, 57, 165583, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 31, 8, 47, 57, 159581, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user_group',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 31, 8, 47, 57, 164583, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user_right',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 31, 8, 47, 57, 166582, tzinfo=utc)),
        ),
    ]