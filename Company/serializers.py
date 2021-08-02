from Users.models import transaction_right
from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import company_master, company_master_docs, currency, ledger_master,voucher_type, acc_group, acc_head, cost_category
from Users.serializers import UserSerializer,UsernamesSerializer


# superAdmin serializer for saving, editing admin/superadmin
class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = currency
        fields = '__all__'
        extra_kwargs = {
            'id':{'read_only': True},
            'created_on':{'read_only': True}
        }
        
        
class CompanySerializer(serializers.ModelSerializer):
    # base_currency = CurrencySerializer()
    class Meta:
        model = company_master
        fields = '__all__'
        extra_kwargs = {
            
            'id':{'read_only': True},
            'created_on':{'read_only': True}
        }

    def create(self, validated_data): 
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class GetCompanySerializer(serializers.ModelSerializer):
    base_currency = CurrencySerializer()
    class Meta:
        model = company_master
        fields = '__all__'
        extra_kwargs = {
            
            'id':{'read_only': True},
            'created_on':{'read_only': True}
        }


class CompanyDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = company_master_docs
        fields = '__all__'
        extra_kwargs = {
            'id':{'read_only': True},
            'created_on':{'read_only': True}
        }
    
    def create(self, validated_data): 
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance



class GetCompanyDocumentSerializer(serializers.ModelSerializer):
    company_master_id = GetCompanySerializer()  
    class Meta:
        model = company_master_docs
        fields = '__all__'
        extra_kwargs = {
            'id':{'read_only': True},
            'created_on':{'read_only': True}
        }


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = currency
        fields = '__all__'
        extra_kwargs = {
            'id':{'read_only': True},
            'created_on':{'read_only': True}
        }

class GetVoucherTypeSerializer(serializers.ModelSerializer):
    authorization_id = UsernamesSerializer()
    class Meta:
        model = voucher_type
        fields = '__all__'
        extra_kwargs = {
            
            'id':{'read_only': True},
            'created_on':{'read_only': True}
        }

class VoucherTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = voucher_type
        fields = '__all__'
        extra_kwargs = {
            
            'id':{'read_only': True},
            'created_on':{'read_only': True}
        }

         
    def create(self, validated_data): 
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class AccGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = acc_group
        fields = '__all__'
        extra_kwargs = {
            
            'id':{'read_only': True},
            'created_on':{'read_only': True},
            'is_fixed': {'write_only': True}
        }

         
    def create(self, validated_data): 
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class AccountHeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = acc_head
        fields = '__all__'
        extra_kwargs = {
            'id':{'read_only': True},
            'created_on':{'read_only': True},
            'schedule_no':{'read_only': True},
        }

         
    def create(self, validated_data): 
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class LedgerMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ledger_master
        fields = '__all__'
        extra_kwargs = {
            
            'id':{'read_only': True},
            'created_on':{'read_only': True}
        }

         
    def create(self, validated_data): 
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
        

class CostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = cost_category
        fields = '__all__'
        extra_kwargs = {
            
            'id':{'read_only': True},
            'created_on':{'read_only': True}
        }

         
    def create(self, validated_data): 
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class GetTransactionSerializer(serializers.ModelSerializer):
     class Meta:
        model = transaction_right
        fields = '__all__'
        extra_kwargs = {
            
            'id':{'read_only': True},
            'created_on':{'read_only': True}
        }

