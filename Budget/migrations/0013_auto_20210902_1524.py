# Generated by Django 3.2.5 on 2021-09-02 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0019_alter_ledger_master_docs_ledger_master_id'),
        ('Budget', '0012_alter_budget_details_budget_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalrevised_budget_details',
            name='company_master_id',
            field=models.ForeignKey(blank=True, db_constraint=False, default=11, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='Company.company_master'),
        ),
        migrations.AddField(
            model_name='revised_budget_details',
            name='company_master_id',
            field=models.ForeignKey(default=11, on_delete=django.db.models.deletion.CASCADE, to='Company.company_master'),
        ),
    ]
