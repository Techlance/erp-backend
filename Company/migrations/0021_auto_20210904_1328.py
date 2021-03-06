# Generated by Django 3.2.5 on 2021-09-04 07:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0010_auto_20210904_1328'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Company', '0020_alter_ledger_master_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acc_group',
            name='company_master_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Company.company_master'),
        ),
        migrations.AlterField(
            model_name='acc_head',
            name='company_master_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Company.company_master'),
        ),
        migrations.AlterField(
            model_name='company_master',
            name='base_currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Company.currency'),
        ),
        migrations.AlterField(
            model_name='company_master_docs',
            name='company_master_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Company.company_master'),
        ),
        migrations.AlterField(
            model_name='cost_category',
            name='company_master_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Company.company_master'),
        ),
        migrations.AlterField(
            model_name='cost_category',
            name='name',
            field=models.TextField(max_length=200),
        ),
        migrations.AlterField(
            model_name='cost_center',
            name='company_master_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Company.company_master'),
        ),
        migrations.AlterField(
            model_name='historicalcost_category',
            name='name',
            field=models.TextField(max_length=200),
        ),
        migrations.AlterField(
            model_name='ledger_master',
            name='company_master_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Company.company_master'),
        ),
        migrations.AlterField(
            model_name='ledger_master_docs',
            name='company_master_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Company.company_master'),
        ),
        migrations.AlterField(
            model_name='ledger_master_docs',
            name='ledger_master_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ledger_docs', to='Company.ledger_master'),
        ),
        migrations.AlterField(
            model_name='user_company',
            name='company_master_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Company.company_master'),
        ),
        migrations.AlterField(
            model_name='user_company',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user_company',
            name='user_group_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Users.user_group'),
        ),
        migrations.AlterField(
            model_name='voucher_type',
            name='authorization_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='voucher_type',
            name='company_master_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Company.company_master'),
        ),
        migrations.AlterField(
            model_name='year_master',
            name='company_master_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Company.company_master'),
        ),
        migrations.AlterUniqueTogether(
            name='cost_category',
            unique_together={('name', 'company_master_id')},
        ),
    ]
