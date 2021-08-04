# Generated by Django 3.2.5 on 2021-08-04 16:23

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0015_auto_20210803_0838'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='can_create_company',
        ),
        migrations.RemoveField(
            model_name='user',
            name='can_create_user',
        ),
        migrations.RemoveField(
            model_name='user',
            name='can_create_user_groups',
        ),
        migrations.RemoveField(
            model_name='user',
            name='can_delete_company',
        ),
        migrations.RemoveField(
            model_name='user',
            name='can_delete_user',
        ),
        migrations.RemoveField(
            model_name='user',
            name='can_delete_user_groups',
        ),
        migrations.RemoveField(
            model_name='user',
            name='can_edit_company',
        ),
        migrations.RemoveField(
            model_name='user',
            name='can_edit_user',
        ),
        migrations.RemoveField(
            model_name='user',
            name='can_edit_user_groups',
        ),
        migrations.RemoveField(
            model_name='user',
            name='can_view_company',
        ),
        migrations.RemoveField(
            model_name='user',
            name='can_view_user',
        ),
        migrations.RemoveField(
            model_name='user',
            name='can_view_user_groups',
        ),
        migrations.AlterField(
            model_name='transaction_right',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 4, 16, 23, 51, 45871, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 4, 16, 23, 51, 43866, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user_group',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 4, 16, 23, 51, 45871, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user_right',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 4, 16, 23, 51, 45871, tzinfo=utc)),
        ),
    ]
