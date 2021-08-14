from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from simple_history.models import HistoricalRecords


# Create your models here.
class User(AbstractUser):
    name = models.TextField(max_length=200, null=False)
    email = models.EmailField(unique=True, null=False)
    created_by = models.TextField(default="primary",max_length=200, null=False)
    created_on = models.DateTimeField(default=timezone.now())
    altered_by = models.TextField(max_length=200, null=True, blank=True)
    history = HistoricalRecords()
    
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email




class user_group(models.Model):
    user_group_name = models.TextField(max_length=200, null=False, unique=True) #should be unique??
    backdated_days = models.IntegerField(default=60,null=True)
    created_by = models.TextField(max_length=200, null=False)
    created_on = models.DateTimeField(default=timezone.now())
    altered_by = models.TextField(max_length=200, null=True, blank=True)
    history = HistoricalRecords()
    def __str__(self):
        return self.user_group_name




class transaction_right(models.Model):
    transactions = models.TextField(max_length=200, null=False)
    created_by = models.TextField(max_length=200, null=False)
    created_on = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.transactions


class user_right(models.Model):
    user_group_id = models.ForeignKey(to=user_group, null=False, on_delete=models.CASCADE)
    transaction_id = models.ForeignKey(to=transaction_right, null=False, on_delete=models.CASCADE)
    can_create = models.BooleanField(default=False)
    can_alter = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_view = models.BooleanField(default=False)
    created_by = models.TextField(max_length=200, null=False)
    created_on = models.DateTimeField(default=timezone.now())
    altered_by = models.TextField(max_length=200, null=True, blank=True)
    history = HistoricalRecords()
    class Meta:
        unique_together = ('user_group_id', 'transaction_id',)









    


