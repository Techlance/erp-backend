# Generated by Django 3.2.5 on 2021-09-05 16:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0021_auto_20210904_1328'),
        ('ledger_balance', '0018_auto_20210904_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ledger_bal_billwise',
            name='ledger_bal_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ledger_bal_billwise', to='ledger_balance.ledger_balance'),
        ),
        migrations.AlterField(
            model_name='ledger_balance',
            name='ledger_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ledger_balance', to='Company.ledger_master'),
        ),
        migrations.AlterField(
            model_name='op_bal_brs',
            name='bank_ledger_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bank_ledger', to='Company.ledger_master'),
        ),
        migrations.AlterUniqueTogether(
            name='op_bal_brs',
            unique_together={('bank_ledger_id', 'company_master_id')},
        ),
    ]
