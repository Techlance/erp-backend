from django.db import models
from Company.models import year_master, ledger_master, cost_center, company_master
from django.utils import timezone
# Create your models here.

class lc(models.Model):
    lc_no = models.AutoField(primary_key=True)
    trans_type = models.TextField(max_length=1000, null=False) # import/export as choice field
    lc_date = models.DateField(null=False)
    year_id = models.ForeignKey(to=year_master, null=False, on_delete=models.CASCADE)
    party_code = models.ForeignKey(to=ledger_master, null=False, on_delete=models.CASCADE)
    cost_center = models.ForeignKey(to=cost_center, null=False, on_delete=models.CASCADE)
    applicant_bank = models.TextField(max_length=1000, null=True)
    benificiary_bank = models.TextField(max_length=1000, null=True)
    benificiary_bank_lc_no = models.TextField(max_length=1000, null=False)
    applicant_bank_lc_no = models.TextField(max_length=1000, null=False)
    inspection = models.BooleanField(default=False, null=True)
    bank_ref = models.TextField(max_length=1000, null=False)
    days_for_submit_to_bank = models.IntegerField(max_length=10000000)
    payment_terms = models.TextField(max_length=50000, null=False)
    place_of_taking_incharge = models.TextField(max_length=1000, null=False)
    final_destination_of_delivery = models.TextField(max_length=10000, null=False)
    completed = models.BooleanField(default=False, null=False)
    shipment_terms = models.TextField(max_length=10000000, null=False)
    goods_description = models.TextField(max_length=10000000, null=False)
    other_lc_terms = models.TextField(max_length=10000000, null=False)
    # bank_ac =  models.ForeignKey(to=ledger_master, null=False, on_delete=models.CASCADE)
    expiry_date = models.DateField(null=False)
    lc_amount = models.FloatField(max_length=100000000, null=False)
    company_master_id = models.ForeignKey(to=company_master, null=False, on_delete=models.CASCADE)
    created_by = models.TextField(max_length=100, null=False)
    created_on = models.DateTimeField(default=timezone.now())
    class Meta:
        unique_together = ('lc_no', 'company_master_id',)

class lc_logs(models.Model):
    lc_no = models.TextField(max_length=1000, null=False)
    trans_type = models.TextField(max_length=1000, null=False) # import/export as choice field
    lc_date = models.DateField(null=False)
    year_id = models.TextField(max_length=1000, null=False)
    party_code = models.TextField(max_length=1000, null=False)
    cost_center = models.TextField(max_length=1000, null=False)
    applicant_bank = models.TextField(max_length=1000, null=True)
    benificiary_bank = models.TextField(max_length=1000, null=True)
    benificiary_bank_lc_no = models.TextField(max_length=1000, null=False)
    applicant_bank_lc_no = models.TextField(max_length=1000, null=False)
    inspection = models.BooleanField(default=False, null=True)
    bank_ref = models.TextField(max_length=1000, null=False)
    days_for_submit_to_bank = models.IntegerField(max_length=10000000)
    payment_terams = models.TextField(max_length=50000, null=False)
    place_of_taking_incharge = models.TextField(max_length=1000, null=False)
    final_destination_of_delivery = models.TextField(max_length=10000, null=False)
    completed = models.BooleanField(default=False, null=False)
    shipment_terms = models.TextField(max_length=10000000, null=False)
    goods_description = models.TextField(max_length=10000000, null=False)
    other_lc_terms = models.TextField(max_length=10000000, null=False)
    bank_ac =  models.TextField(max_length=1000, null=False)
    expiry_date = models.DateField(null=False)
    lc_amount = models.FloatField(max_length=100000000, null=False)
    company_master_id = models.TextField(max_length=1000, null=False)
    altered_by = models.TextField(null=False)
    altered_on = models.DateTimeField(default=timezone.now())
    entry = models.TextField(default="before", null=False)
    is_deleted = models.BooleanField(default=False)
    operation = models.TextField(null=False)


class lc_docs(models.Model):
    doc_name = models.TextField(max_length=500, null=False)
    file = models.FileField(upload_to="lc_files", null=False)
    lc_id = models.ForeignKey(to=lc, null=False, on_delete=models.CASCADE)
    created_by = models.TextField(max_length=200, null=False)
    created_on = models.DateTimeField(default=timezone.now())
    def __str__(self):
        return self.doc_name


class lc_docs_logs(models.Model):
    doc_name = models.TextField(max_length=500, null=False)
    file = models.FileField(upload_to="lc_files", null=False)
    lc_id = models.TextField(max_length=10000, null=False)
    altered_by = models.TextField(null=False)
    altered_on = models.DateTimeField(default=timezone.now())
    entry = models.TextField(default="before", null=False)
    is_deleted = models.BooleanField(default=False)
    operation = models.TextField(null=False)


class lc_amend(models.Model):
    lc_id = models.ForeignKey(to=lc, null=False, on_delete=models.CASCADE)
    amendment_no = models.BigIntegerField(null=False)
    issue_date = models.DateField(null=False)
    LDS = models.DateField(null=False)
    expiry_date = models.DateField(null=False)
    lc_amount = models.FloatField()
    remarks = models.TextField(null=False)
    created_by = models.TextField(max_length=200, null=False)
    created_on = models.DateTimeField(default=timezone.now())


class lc_amend_logs(models.Model):
    lc_id = models.TextField(null=False)
    amendment_no = models.BigIntegerField(null=False)
    issue_date = models.DateField(null=False)
    LDS = models.DateField(null=False)
    expiry_date = models.DateField(null=False)
    lc_amount = models.FloatField()
    remarks = models.TextField(null=False)
    altered_by = models.TextField(null=False)
    altered_on = models.DateTimeField(default=timezone.now())
    entry = models.TextField(default="before", null=False)
    is_deleted = models.BooleanField(default=False)
    operation = models.TextField(null=False)








