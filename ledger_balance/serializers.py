from django.db.models.fields import files
from Users.models import transaction_right
from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import ledger_balance, op_bal_brs, ledger_bal_billwise
from Users.serializers import UserSerializer,UsernamesSerializer, UserGroupSerializer

class LedgerBalanceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ledger_balance
        fields = '__all__'
        extra_kwargs = {
            
            'id':{'read_only': True},
            'created_on':{'read_only': True},
            'altered_by': {'write_only': True}
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

class LedgerBalanceBillwiseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ledger_bal_billwise
        fields = '__all__'
        extra_kwargs = {
            
            'id':{'read_only': True},
            'created_on':{'read_only': True},
            'altered_by': {'write_only': True}
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

class OpBalanceBrsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = op_bal_brs
        fields = '__all__'
        extra_kwargs = {
            
            'id':{'read_only': True},
            'created_on':{'read_only': True},
            'altered_by': {'write_only': True}
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
