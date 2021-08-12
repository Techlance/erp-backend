# Generated by Django 3.2.5 on 2021-08-12 01:32

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.utils.timezone import utc
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0029_auto_20210811_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction_right',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 12, 1, 31, 56, 80197, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 12, 1, 31, 56, 75270, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user_group',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 12, 1, 31, 56, 79197, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user_group_logs',
            name='altered_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 12, 1, 31, 56, 79197, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user_logs',
            name='altered_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 12, 1, 31, 56, 78196, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user_right',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 12, 1, 31, 56, 80197, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user_right_logs',
            name='altered_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 12, 1, 31, 56, 80197, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='HistoricalUser',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.TextField(max_length=200)),
                ('email', models.EmailField(db_index=True, max_length=254)),
                ('created_by', models.TextField(default='primary', max_length=200)),
                ('created_on', models.DateTimeField(default=datetime.datetime(2021, 8, 12, 1, 31, 56, 75270, tzinfo=utc))),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical user',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
