# Generated by Django 3.2.5 on 2021-09-04 07:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0021_auto_20210904_1328'),
        ('lc', '0011_auto_20210827_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lc',
            name='bank_ac',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ledger_master2', to='Company.ledger_master'),
        ),
        migrations.AlterField(
            model_name='lc',
            name='base_currency',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.PROTECT, to='Company.currency'),
        ),
        migrations.AlterField(
            model_name='lc',
            name='company_master_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Company.company_master'),
        ),
        migrations.AlterField(
            model_name='lc',
            name='cost_center',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Company.cost_center'),
        ),
        migrations.AlterField(
            model_name='lc',
            name='party_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ledger_master1', to='Company.ledger_master'),
        ),
        migrations.AlterField(
            model_name='lc',
            name='year_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Company.year_master'),
        ),
        migrations.AlterField(
            model_name='lc_amend',
            name='company_master_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='Company.company_master'),
        ),
        migrations.AlterField(
            model_name='lc_amend',
            name='lc_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lc.lc'),
        ),
        migrations.AlterField(
            model_name='lc_docs',
            name='company_master_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='Company.company_master'),
        ),
        migrations.AlterField(
            model_name='lc_docs',
            name='lc_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lc.lc'),
        ),
    ]
