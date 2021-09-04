# Generated by Django 3.2.5 on 2021-09-04 07:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0009_auto_20210814_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_right',
            name='transaction_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Users.transaction_right'),
        ),
        migrations.AlterField(
            model_name='user_right',
            name='user_group_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Users.user_group'),
        ),
    ]