# Generated by Django 3.2.5 on 2021-08-29 08:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0019_alter_ledger_master_docs_ledger_master_id'),
        ('ledger_balance', '0015_auto_20210826_1806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalop_bal_brs',
            name='acc_code',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='Company.ledger_master'),
        ),
        migrations.AlterField(
            model_name='historicalop_bal_brs',
            name='bank_ledger_id',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='Company.ledger_master'),
        ),
        migrations.AlterField(
            model_name='op_bal_brs',
            name='acc_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acc_code_ledger', to='Company.ledger_master'),
        ),
        migrations.AlterField(
            model_name='op_bal_brs',
            name='bank_ledger_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bank_ledger', to='Company.ledger_master'),
        ),
    ]