# Generated by Django 3.2.5 on 2021-08-26 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ledger_balance', '0014_alter_ledger_balance_ledger_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ledger_bal_billwise',
            name='ledger_bal_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ledger_bal_billwise', to='ledger_balance.ledger_balance'),
        ),
        migrations.AlterField(
            model_name='op_bal_brs',
            name='bank_ledger_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ledger_balance.ledger_balance'),
        ),
    ]
