# Generated by Django 3.2.5 on 2021-08-16 17:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0009_auto_20210814_2335'),
        ('Company', '0014_auto_20210815_0034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acc_group',
            name='child_of',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='child', to='Company.acc_group'),
        ),
        migrations.AlterField(
            model_name='cost_category',
            name='company_master_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Company.company_master'),
        ),
        migrations.AlterField(
            model_name='cost_category',
            name='name',
            field=models.TextField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='cost_center',
            name='child_of',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='Company.cost_center'),
        ),
        migrations.AlterField(
            model_name='cost_center',
            name='company_master_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Company.company_master'),
        ),
        migrations.AlterField(
            model_name='cost_center',
            name='cost_category_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cost_center', to='Company.cost_category'),
        ),
        migrations.AlterField(
            model_name='historicalcost_category',
            name='name',
            field=models.TextField(db_index=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='ledger_master',
            name='acc_group_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ledger_master', to='Company.acc_group'),
        ),
        migrations.AlterField(
            model_name='user_company',
            name='user_group_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.user_group'),
        ),
    ]
