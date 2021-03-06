# Generated by Django 3.2.5 on 2021-08-27 15:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0019_alter_ledger_master_docs_ledger_master_id'),
        ('lc', '0010_auto_20210824_2243'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicallc',
            name='base_currency',
            field=models.ForeignKey(blank=True, db_constraint=False, default='1', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='Company.currency'),
        ),
        migrations.AddField(
            model_name='lc',
            name='base_currency',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='Company.currency'),
        ),
    ]
