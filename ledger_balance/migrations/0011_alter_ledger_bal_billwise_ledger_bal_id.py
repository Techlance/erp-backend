# Generated by Django 3.2.5 on 2021-08-20 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ledger_balance', '0010_alter_ledger_bal_billwise_ledger_bal_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ledger_bal_billwise',
            name='ledger_bal_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ledger_balance_billwise', to='ledger_balance.ledger_balance'),
        ),
    ]
