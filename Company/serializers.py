from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import company_master, currency


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
    base_currency = CurrencySerializer()
    class Meta:
        model = company_master
        fields = '__all__'
        # fields = ['id', 'company_name', 'address', 'country','state', ' email', 'website', 'contact_no', 'base_currency', 'cr_no', 'registration_no', 'tax_id_no', 'vat_id_no', 'year_start_date', 'year_end_date', ' logo', 'created_by', 'created_on']
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




    