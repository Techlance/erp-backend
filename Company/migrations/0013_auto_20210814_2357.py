# Generated by Django 3.2.5 on 2021-08-14 18:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0012_auto_20210814_2349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acc_group',
            name='child_of',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Company.acc_group'),
        ),
        migrations.AlterField(
            model_name='fixed_account_group',
            name='child_of',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Company.fixed_account_group'),
        ),
    ]
