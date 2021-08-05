from re import T
from django.db import models
from django.utils import timezone
from Users.models import *
# Create your models here.


class currency(models.Model):
    currency = models.TextField(max_length=50, null=False, unique=True)
    currency_name = models.TextField(max_length=100, null=False, unique=True)
    created_by = models.TextField(max_length=200, null=False)
    created_on = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.currency

class currency_logs(models.Model):
    currency = models.TextField(max_length=50, null=False, unique=True)
    currency_name = models.TextField(max_length=100, null=False, unique=True)
    altered_by = models.TextField(null=False)
    altered_on = models.DateTimeField(default=timezone.now())
    entry = models.TextField(default="before", null=False)
    is_deleted = models.BooleanField(default=False)
    operation = models.TextField(null=False)



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
    created_on = models.DateTimeField(default=timezone.now())
    def __str__(self):
        return self.company_name

class company_master_logs(models.Model):
    company_name = models.TextField(max_length=200, unique=True, null=False)
    address = models.TextField(max_length=1000, null=False)
    country = models.TextField(max_length=100, null=False)
    state =  models.TextField(max_length=100, null=False)
    email = models.EmailField(null=True)
    website = models.TextField(max_length=1000, null=True)
    contact_no = models.TextField(max_length=20, null=True)
    base_currency = models.ForeignKey(to=currency, null=False)
    cr_no = models.TextField(max_length=500, null=True)
    registration_no = models.TextField(max_length=500, null=True)
    tax_id_no = models.TextField(max_length=500, null=True)
    vat_id_no = models.TextField(max_length=500, null=True)
    year_start_date = models.DateField(null=False)
    year_end_date = models.DateField(null=False)
    logo = models.ImageField(upload_to="logo", null=True)
    altered_by = models.TextField(null=False)
    altered_on = models.DateTimeField(default=timezone.now())
    entry = models.TextField(default="before", null=False)
    is_deleted = models.BooleanField(default=False)
    operation = models.TextField(null=False)
    def __str__(self):
        return self.company_name


class user_company(models.Model):
    user = models.ForeignKey(to=User, null=False, on_delete=models.CASCADE)
    user_group_id = models.ForeignKey(to=user_group, null=False, on_delete=models.Case)
    company_master_id = models.ForeignKey(to=company_master, null=False, on_delete=models.CASCADE)
    created_by = models.TextField(max_length=200, null=False)
    created_on = models.DateTimeField(default=timezone.now())
    class Meta:
        unique_together = ('user', 'company_master_id',)
    
class user_company_logs(models.Model):
    user = models.ForeignKey(to=User, null=False, on_delete=models.CASCADE)
    user_group_id = models.ForeignKey(to=user_group, null=False, on_delete=models.Case)
    company_master_id = models.ForeignKey(to=company_master, null=False)
    altered_by = models.TextField(null=False)
    altered_on = models.DateTimeField(default=timezone.now())
    entry = models.TextField(default="before", null=False)
    is_deleted = models.BooleanField(default=False)
    operation = models.TextField(null=False)


class company_master_docs(models.Model): 
    doc_name = models.TextField(max_length=500, null=False)
    file = models.FileField(upload_to="files", null=False)
    company_master_id = models.ForeignKey(to=company_master, null=False, on_delete=models.CASCADE)
    created_by = models.TextField(max_length=200, null=False)
    created_on = models.DateTimeField(default=timezone.now())
    def __str__(self):
        return self.doc_name

class company_master_docs_logs(models.Model):
    doc_name = models.TextField(max_length=500, null=False)
    file = models.FileField(upload_to="files", null=False)
    company_master_id = models.ForeignKey(to=company_master, null=False)
    altered_by = models.TextField(null=False)
    altered_on = models.DateTimeField(default=timezone.now())
    entry = models.TextField(default="before", null=False)
    is_deleted = models.BooleanField(default=False)
    operation = models.TextField(null=False)



class year_master(models.Model):
    year_no = models.IntegerField(null=False, default=0)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    company_master_id = models.ForeignKey(to=company_master, null=False, on_delete=models.CASCADE)
    status = models.BooleanField(default=True, null=False)
    locked = models.BooleanField(default=True, null=False)
    created_by = models.TextField(max_length=200, null=False)
    created_on = models.DateTimeField(default=timezone.now())
    def __str__(self):
        return self.year_no

class year_master(models.Model):
    year_no = models.IntegerField(null=False, default=0)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    company_master_id = models.ForeignKey(to=company_master, null=False)
    status = models.BooleanField(default=True, null=False)
    locked = models.BooleanField(default=True, null=False)
    altered_by = models.TextField(null=False)
    altered_on = models.DateTimeField(default=timezone.now())
    entry = models.TextField(default="before", null=False)
    is_deleted = models.BooleanField(default=False)
    operation = models.TextField(null=False)



class voucher_type(models.Model):
    voucher_name = models.TextField(max_length=500, null=False)
    voucher_class = models.TextField(max_length=500, null=False)
    company_master_id = models.ForeignKey(to=company_master, null=False, on_delete=models.CASCADE)
    authorization_id = models.ForeignKey(to=User, null=True, on_delete=models.CASCADE)
    auto_numbering = models.BooleanField(default=False)
    prefix = models.TextField(max_length=200, null=True)
    restart = models.TextField(max_length=50, null=True)
    is_fixed = models.BooleanField(default=True)
    created_by = models.TextField(max_length=200, null=False)
    created_on = models.DateTimeField(default=timezone.now())
    class Meta:
        unique_together = ('voucher_name', 'company_master_id',)
    
    def __str__(self):
        return self.voucher_name
    
class voucher_type_logs(models.Model):
    voucher_name = models.TextField(max_length=500, null=False)
    voucher_class = models.TextField(max_length=500, null=False)
    company_master_id = models.ForeignKey(to=company_master, null=False)
    authorization_id = models.ForeignKey(to=User, null=True)
    auto_numbering = models.BooleanField(default=False)
    prefix = models.TextField(max_length=200, null=True)
    restart = models.TextField(max_length=50, null=True)
    is_fixed = models.BooleanField(default=True)
    altered_by = models.TextField(null=False)
    altered_on = models.DateTimeField(default=timezone.now())
    entry = models.TextField(default="before", null=False)
    is_deleted = models.BooleanField(default=False)
    operation = models.TextField(null=False)




class acc_head(models.Model):
    acc_head_name = models.TextField(max_length=200, null=False)
    title = models.TextField(max_length=200, null=False)
    company_master_id = models.ForeignKey(to=company_master, null=False, on_delete=models.CASCADE)
    bs = models.BooleanField(default=True, null=False)
    schedule_no = models.IntegerField(null=False)
    is_fixed = models.BooleanField(default=True)
    created_by = models.TextField(max_length=200, null=False)
    created_on = models.DateTimeField(default=timezone.now())
    class Meta:
        unique_together = ('acc_head_name', 'company_master_id',)
    def __str__(self):
        return self.acc_head_name

class acc_head_logs(models.Model):
    acc_head_name = models.TextField(max_length=200, null=False)
    title = models.TextField(max_length=200, null=False)
    company_master_id = models.ForeignKey(to=company_master, null=False, on_delete=models.CASCADE)
    bs = models.BooleanField(default=True, null=False)
    schedule_no = models.IntegerField(null=False)
    is_fixed = models.BooleanField(default=True)
    altered_by = models.TextField(null=False)
    altered_on = models.DateTimeField(default=timezone.now())
    entry = models.TextField(default="before", null=False)
    is_deleted = models.BooleanField(default=False)
    operation = models.TextField(null=False)



class acc_group(models.Model):
    group_name = models.TextField(max_length=1000, null=False)
    acc_head_id = models.ForeignKey(to=acc_head, null=False, on_delete=models.CASCADE)
    group_code = models.TextField(max_length=4, null=False)
    company_master_id = models.ForeignKey(to=company_master, null=False, on_delete=models.CASCADE)
    child_of = models.TextField(max_length=1000, null=True)
    is_fixed = models.BooleanField(default=True, null=False)
    created_by = models.TextField(max_length=200, null=False)
    created_on = models.DateTimeField(default=timezone.now())
    class Meta:
        # testing : pending
        unique_together = ('group_code', 'company_master_id',)
        unique_together = ('group_name', 'company_master_id',)
    def __str__(self):
        return self.group_name


class acc_group_logs(models.Model):
    group_name = models.TextField(max_length=1000, null=False)
    acc_head_id = models.ForeignKey(to=acc_head, null=False)
    group_code = models.TextField(max_length=4, null=False)
    company_master_id = models.ForeignKey(to=company_master, null=False)
    child_of = models.TextField(max_length=1000, null=True)
    is_fixed = models.BooleanField(default=True, null=False)
    altered_by = models.TextField(null=False)
    altered_on = models.DateTimeField(default=timezone.now())
    entry = models.TextField(default="before", null=False)
    is_deleted = models.BooleanField(default=False)
    operation = models.TextField(null=False)



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
    created_on = models.DateTimeField(default=timezone.now())
    def __str__(self):
        return self.ledger_name


class ledger_master_logs(models.Model):
    acc_group_id = models.ForeignKey(to=acc_group, null=False)
    ledger_id = models.TextField(max_length=200, null=False)
    old_ledger_id = models.TextField(max_length=200, null=True)
    ledger_name = models.TextField(max_length=200, null=False)
    company_master_id = models.ForeignKey(to=company_master, null=False)
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
    altered_by = models.TextField(null=False)
    altered_on = models.DateTimeField(default=timezone.now())
    entry = models.TextField(default="before", null=False)
    is_deleted = models.BooleanField(default=False)
    operation = models.TextField(null=False)


class cost_category(models.Model):
    name = models.TextField(max_length=200, null=False)
    company_master_id = models.ForeignKey(to=company_master, null=False, on_delete=models.CASCADE)
    created_by = models.TextField(max_length=200, null=False)
    created_on = models.DateTimeField(default=timezone.now())
    def __str__(self):
        return self.name

class cost_category_logs(models.Model):
    name = models.TextField(max_length=200, null=False)
    company_master_id = models.ForeignKey(to=company_master, null=False)
    altered_by = models.TextField(null=False)
    altered_on = models.DateTimeField(default=timezone.now())
    entry = models.TextField(default="before", null=False)
    is_deleted = models.BooleanField(default=False)
    operation = models.TextField(null=False)


class cost_center(models.Model):
    cost_center_name = models.TextField(max_length=500, null=False)
    cost_category_id = models.ForeignKey(to=cost_category, null=False, on_delete=models.CASCADE)
    child_of = models.TextField(max_length=500, default="primary")
    company_master_id = models.ForeignKey(to=company_master, null=False, on_delete=models.CASCADE)
    created_by = models.TextField(max_length=200, null=False)
    created_on = models.DateTimeField(default=timezone.now())
    
    class Meta:
        unique_together = ('cost_category_id', 'company_master_id',)
    
    def __str__(self):
        return self.cost_center_name


class cost_center_logs(models.Model):
    cost_center_name = models.TextField(max_length=500, null=False)
    cost_category_id = models.ForeignKey(to=cost_category, null=False)
    child_of = models.TextField(max_length=500, default="primary")
    company_master_id = models.ForeignKey(to=company_master, null=False)
    altered_by = models.TextField(null=False)
    altered_on = models.DateTimeField(default=timezone.now())
    entry = models.TextField(default="before", null=False)
    is_deleted = models.BooleanField(default=False)
    operation = models.TextField(null=False)




# models for default data triggered while creating company

class fixed_vouchertype(models.Model):
    voucher_name = models.TextField(max_length=500, null=False)
    voucher_class = models.TextField(max_length=500, null=False)
    auto_numbering = models.BooleanField(default=False)
    is_fixed = models.BooleanField(default=True)
    created_by = models.TextField(max_length=200, null=False)
    created_on = models.DateTimeField(default=timezone.now())
    
    def __str__(self):
        return self.voucher_name


class fixed_account_head(models.Model):
    acc_head_name = models.TextField(max_length=200, null=False)
    title = models.TextField(max_length=200, null=False)
    bs = models.BooleanField(default=True, null=False)
    is_fixed = models.BooleanField(default=True)
    created_by = models.TextField(max_length=200, null=False)
    created_on = models.DateTimeField(default=timezone.now())
    def __str__(self):
        return self.acc_head_name


class fixed_account_group(models.Model):
    group_name = models.TextField(max_length=1000, null=False)
    acc_head_id = models.ForeignKey(to=fixed_account_head, null=False, on_delete=models.CASCADE)
    group_code = models.TextField(max_length=4, null=False)
    child_of = models.TextField(max_length=1000, null=True, blank=True)
    is_fixed = models.BooleanField(default=True, null=False)
    created_by = models.TextField(max_length=200, null=False)
    created_on = models.DateTimeField(default=timezone.now())
    def __str__(self):
        return self.group_name

class fixed_ledger_master(models.Model):
    acc_group_id = models.ForeignKey(to=fixed_account_group, null=False, on_delete=models.CASCADE)
    ledger_id = models.TextField(max_length=200, null=False)
    ledger_name = models.TextField(max_length=200, null=False)
    maintain_billwise = models.BooleanField(default=True, null=False)
    is_fixed = models.BooleanField(default=True)
    created_by = models.TextField(max_length=200, null=False)
    created_on = models.DateTimeField(default=timezone.now())
    def __str__(self):
        return self.ledger_name

    











