from django.db import models
from django.utils import timezone
from Company.models import company_master, ledger_master, year_master
from simple_history.models import HistoricalRecords
# Create your models here.
from Users.models import User

class budget(models.Model):
    budget_name = models.TextField(max_length=200, null=False)
    company_master_id = models.ForeignKey(to=company_master, null=False, on_delete=models.CASCADE)
    year_id = models.ForeignKey(to=year_master, null=False, on_delete=models.CASCADE)
    enforce_restrictions = models.BooleanField()
    authoriser = models.ForeignKey(to=User, null=False, on_delete=models.CASCADE)
    budget_type = models.TextField(max_length=100)
    created_by = models.TextField(max_length=200, null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        unique_together = ('id', 'company_master_id',)

    def __str__(self):
        return self.budget_name

class budget_details(models.Model):
    budget_id = models.ForeignKey(to=budget,null=False,on_delete=models.CASCADE)
    company_master_id = models.ForeignKey(to=company_master, null=False, on_delete=models.CASCADE)
    ledger_id = models.ForeignKey(to=ledger_master,null=False, on_delete=models.CASCADE)
    jan = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    feb = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    mar = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    apr = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    may = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    jun = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    jul = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    aug = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    sep = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    octo = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    nov = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    dec = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    created_by = models.TextField(max_length=200, null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()
    class Meta:
        unique_together = ('budget_id', 'ledger_id',)



class revised_budget_details(models.Model):
    budget_id = models.ForeignKey(to=budget,null=False, on_delete=models.CASCADE)
    ledger_id = models.ForeignKey(to=ledger_master,null=False, on_delete=models.CASCADE)
    # company_master_id = models.ForeignKey(to=company_master, null=False, on_delete=models.CASCADE)
    jan = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    feb = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    mar = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    apr = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    may = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    jun = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    jul = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    aug = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    sep = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    octo = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    nov = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    dec = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    created_by = models.TextField(max_length=200, null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()
    class Meta:
        unique_together = ('budget_id', 'ledger_id',)

    


class budget_cashflow_details(models.Model):
    budget_id = models.ForeignKey(to=budget,null=False, on_delete=models.CASCADE)
    company_master_id = models.ForeignKey(to=company_master, null=False, on_delete=models.CASCADE)
    ledger_id = models.ForeignKey(to=ledger_master,null=False, on_delete=models.CASCADE)
    jan = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    feb = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    mar = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    apr = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    may = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    jun = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    jul = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    aug = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    sep = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    octo = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    nov = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    dec = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    budget_type = models.TextField(max_length=100)
    cashflow_head = models.TextField(max_length=100)
    created_by = models.TextField(max_length=200, null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()
    class Meta:
        unique_together = ('budget_id', 'cashflow_head',)

class revised_budget_cashflow_details(models.Model):
    budget_id = models.ForeignKey(to=budget,null=False, on_delete=models.CASCADE)
    company_master_id = models.ForeignKey(to=company_master, null=False, on_delete=models.CASCADE)
    ledger_id = models.ForeignKey(to=ledger_master,null=False, on_delete=models.CASCADE)
    jan = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    feb = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    mar = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    apr = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    may = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    jun = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    jul = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    aug = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    sep = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    octo = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    nov = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    dec = models.DecimalField(max_digits=100, decimal_places=4, default=0)
    budget_type = models.TextField(max_length=100)
    cashflow_head = models.TextField(max_length=100)
    created_by = models.TextField(max_length=200, null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()
    class Meta:
        unique_together = ('budget_id', 'cashflow_head',)
