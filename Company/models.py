from django.db import models
from django.utils import timezone
from Users.models import *
# Create your models here.



class currency(models.Model):
    currency = models.TextField(max_length=50, null=False, unique=True)
    currency_name = models.TextField(max_length=100, null=False, unique=True)
    created_by = models.TextField(max_length=200, null=False)
    created_on = models.DateField(default=timezone.now())


class company_master(models.Model):
    company_name = models.TextField(max_length=200, unique=True, null=False)
    address = models.TextField(max_length=1000, null=False)
    country = models.TextField(max_length=100, null=False)
    state =  models.TextField(max_length=100, null=False)
    email = models.EmailField(null=True)
    website = models.TextField(max_length=1000, null=True)
    contact_no = models.TextField(max_length=20, null=True)
    base_currency = models.ForeignKey(to=currency, null=False, on_delete=models.CASCADE)
    cr_no = models.TextField(max_length=500, null=True)
    registration_no = models.TextField(max_length=500, null=True)
    tax_id_no = models.TextField(max_length=500, null=True)
    vat_id_no = models.TextField(max_length=500, null=True)
    year_start_date = models.DateField(null=False)
    year_end_date = models.DateField(null=False)
    logo = models.ImageField(upload_to="logo", null=True)
    created_by = models.TextField(max_length=200, null=False)
    created_on = models.DateField(default=timezone.now())

class user_company(models.Model):
    user = models.ForeignKey(to=User, null=False, on_delete=models.CASCADE)
    user_group_id = models.ForeignKey(to=user_group, null=False, on_delete=models.CASCADE)
    company_master_id = models.ForeignKey(to=company_master, null=False, on_delete=models.CASCADE)
    created_by = models.TextField(max_length=200, null=False)
    created_on = models.DateField(default=timezone.now())


class company_master_docs(models.Model):
    doc_name = models.TextField(max_length=500, null=False)
    file = models.FileField(upload_to="files", null=False)
    company_master_id = models.ForeignKey(to=company_master, null=False, on_delete=models.CASCADE)
    created_by = models.TextField(max_length=200, null=False)
    created_on = models.DateField(default=timezone.now())


class year_master(models.Model):
    year_no = models.IntegerField(null=False)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    company_master_id = models.ForeignKey(to=company_master, null=False, on_delete=models.CASCADE)
    status = models.BooleanField(default=True, null=False)
    created_by = models.TextField(max_length=200, null=False)
    created_on = models.DateField(default=timezone.now())


class voucher_type(models.Model):
    voucher_name = models.TextField(max_length=500, null=False)
    voucher_class = models.TextField(max_length=500, null=False)
    company_master_id = models.ForeignKey(to=company_master, null=False, on_delete=models.CASCADE)
    authorization_id = models.ForeignKey(to=User, null=False, on_delete=models.CASCADE)
    auto_numbering = models.BooleanField(default=False)
    prefix = models.TextField(max_length=200, null=True)
    restart = models.TextField(max_length=50, null=True)
    is_fixed = models.BooleanField(default=True)
    created_by = models.TextField(max_length=200, null=False)
    created_on = models.DateField(default=timezone.now())


class acc_head(models.Model):
    acc_head_name = models.TextField(max_length=200, null=False)
    title = models.TextField(max_length=200, null=False)
    company_master_id = models.ForeignKey(to=company_master, null=False, on_delete=models.CASCADE)
    bs = models.BooleanField(default=True, null=False)
    schedule_no = models.IntegerField(null=False)
    is_fixed = models.BooleanField(default=True)
    created_by = models.TextField(max_length=200, null=False)
    created_on = models.DateField(default=timezone.now())


class acc_group(models.Model):
    group_name = models.TextField(max_length=1000, null=False)
    acc_head_id = models.ForeignKey(to=acc_head, null=False, on_delete=models.CASCADE)
    group_code = models.TextField(max_length=4, null=False)
    company_master_id = models.ForeignKey(to=company_master, null=False, on_delete=models.CASCADE)
    child_of = models.TextField(max_length=1000, null=True)
    is_fixed = models.BooleanField(default=True, null=False)
    created_by = models.TextField(max_length=200, null=False)
    created_on = models.DateField(default=timezone.now())


class ledger_master(models.Model):
    acc_group_id = models.ForeignKey(to=acc_group, null=False, on_delete=models.CASCADE)
    ledger_id = models.TextField(max_length=200, null=False)
    old_ledger_id = models.TextField(max_length=200, null=True)
    ledger_name = models.TextField(max_length=200, null=False)
    company_master_id = models.ForeignKey(to=company_master, null=False, on_delete=models.CASCADE)
    maintain_billwise = models.BooleanField(default=True, null=False)
    address = models.TextField(max_length=1000, null=True)
    tel = models.TextField(max_length=15, null=True)
    email = models.EmailField(null=True)
    contact_person = models.TextField(max_length=50, null=True)
    bank_name = models.TextField(max_length=250, null=True)
    branch_name = models.TextField(max_length=250, null=True)
    bank_code = models.TextField(max_length=250, null=True)
    bank_ac_no = models.TextField(max_length=250, null=True)
    credit_limit = models.TextField(max_length=150, null=True)
    credit_days = models.IntegerField(null=True)
    credit_rating = models.TextField(max_length=150, null=True)
    block_ac = models.BooleanField(default=False, null=True)
    tax_reg_no = models.TextField(max_length=250, null=True)
    cr_no = models.TextField(max_length=250, null=True)
    cr_exp_date = models.DateField(null=True)
    id_no = models.TextField(max_length=250)
    id_exp_date = models.DateField(null=True)
    cc_no = models.TextField(null=True)
    cc_exp_date = models.DateField(null=True)
    vat_no = models.TextField(max_length=250, null=True)
    delivery_terms = models.TextField(max_length=1500, null=True)
    payment_terms = models.TextField(max_length=1500, null=True)
    is_fixed = models.BooleanField(default=True)
    created_by = models.TextField(max_length=200, null=False)
    created_on = models.DateField(default=timezone.now())


    











