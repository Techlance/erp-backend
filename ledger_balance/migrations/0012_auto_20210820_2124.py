# Generated by Django 3.2.5 on 2021-08-20 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0019_alter_ledger_master_docs_ledger_master_id'),
        ('ledger_balance', '0011_alter_ledger_bal_billwise_ledger_bal_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ledger_bal_billwise',
            name='ledger_bal_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ledger_balance_billwise', to='ledger_balance.ledger_balance'),
        ),
        migrations.AlterField(
            model_name='ledger_balance',
            name='fc_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Company.currency'),
        ),
        migrations.AlterField(
            model_name='ledger_balance',
            name='ledger_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Company.ledger_master'),
        ),
        migrations.AlterField(
            model_name='ledger_balance',
            name='year_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Company.year_master'),
        ),
        migrations.AlterField(
            model_name='op_bal_brs',
            name='bank_ledger_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ledger_balance.ledger_balance'),
        ),
        migrations.AlterField(
            model_name='op_bal_brs',
            name='year_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='Company.year_master'),
        ),
    ]
