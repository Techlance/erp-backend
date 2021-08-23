from django.db import models
from django.utils import timezone
from Company.models import currency, company_master, user_company, year_master, ledger_master
from simple_history.models import HistoricalRecords
# Create your models here.

class ledger_balance(models.Model):
    ledger_id = models.ForeignKey(to=ledger_master, null=False, on_delete=models.PROTECT)
    year_id = models.ForeignKey(to=year_master, null=False, on_delete=models.PROTECT)
    company_master_id = models.ForeignKey(to=company_master, null=False, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    dr = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    cr = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    fc_amount = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    fc_name = models.ForeignKey(to=currency, null=False, on_delete=models.PROTECT)
    fc_rate = models.DecimalField(max_digits=100, decimal_places=4, default=0, null=False)
    total_dr = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    total_cr = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    created_by = models.TextField(max_length=200, null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    altered_by = models.TextField(max_length=200, null=True, blank=True)
    history = HistoricalRecords()
    class Meta:
        unique_together = ('ledger_id', 'year_id',)

    def __str__(self):
        return self.ledger_id


class ledger_bal_billwise(models.Model):
    ledger_bal_id = models.ForeignKey(to=ledger_balance,related_name="ledger_bal_billwise", null=False, on_delete=models.PROTECT)
    company_master_id = models.ForeignKey(to=company_master, null=False, on_delete=models.CASCADE)
    ref_no = models.TextField(max_length=100, null=False)
    bill_date = models.DateField(null=True)
    dr = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    cr = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    due_date = models.DateField(null=True)
    amount = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    fc_amount = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    fc_name = models.ForeignKey(to=currency, null=False, on_delete=models.CASCADE)
    fc_rate = models.DecimalField(max_digits=100, decimal_places=4, default=0, null=False)
    created_by = models.TextField(max_length=200, null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    altered_by = models.TextField(max_length=200, null=True, blank=True)
    history = HistoricalRecords()
    class Meta:
        unique_together = ('ledger_bal_id', 'ref_no',)

    def __str__(self):
        return self.ref_no

class op_bal_brs(models.Model):
    bank_ledger_id = models.ForeignKey(to=ledger_balance, null=False, on_delete=models.PROTECT)
    company_master_id = models.ForeignKey(to=company_master, null=False, on_delete=models.CASCADE)
    acc_code = models.TextField(max_length=200, null=False) # check
    year_id = models.ForeignKey(to=year_master, null=False, on_delete=models.PROTECT, default=0)#remove default
    name = models.TextField(max_length=200, null=False)
    chq_date = models.DateField(null=True)
    chq_no = models.IntegerField(max_length=200, null=True)
    transaction_date = models.DateField(null=True)
    transaction_no = models.IntegerField(max_length=200, null=True)
    amount = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    remarks = models.TextField(max_length=200, null=True)
    transaction_type = models.TextField(max_length=200, null=True)
    reco_date = models.DateField(null=True)
    created_by = models.TextField(max_length=200, null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    altered_by = models.TextField(max_length=200, null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.bank_ledger_id