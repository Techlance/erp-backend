# Generated by Django 3.2.5 on 2021-08-14 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0010_auto_20210814_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acc_group',
            name='child_of',
            field=models.TextField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='historicalacc_group',
            name='child_of',
            field=models.TextField(max_length=1000, null=True),
        ),
    ]
