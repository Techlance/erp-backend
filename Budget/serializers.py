from django.db.models.fields import files
from Users.models import transaction_right
from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import budget,budget_details,revised_budget_details,budget_cashflow_details,revised_budget_cashflow_details,cashflow_heads
from Company.serializers import *
from Users.serializers import UserSerializer,UsernamesSerializer, UserGroupSerializer



class BudgetSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = budget
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

class GetBudgetSerializer(serializers.ModelSerializer):
    authoriser = UsernamesSerializer()
    year_id = YearSerializer()
    class Meta:
        model = budget
        fields = '__all__'
        extra_kwargs = {
            
            'id':{'read_only': True},
            'created_on':{'read_only': True}
        }

class BudgetDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = budget_details
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
    

class GetBudgetDetailsSerializer(serializers.ModelSerializer):
    ledger_id = serializers.SlugRelatedField(
        read_only=True,
        slug_field='ledger_name'
     )    
    class Meta:
        model = budget_details
        fields = '__all__'
        extra_kwargs = {
            
            'id':{'read_only': True},
            'created_on':{'read_only': True},
            'altered_by': {'write_only': True}
        }


class RevisedBudgetDetailsSerializer(serializers.ModelSerializer):
    ledger_id = serializers.SlugRelatedField(
        read_only=True,
        slug_field='ledger_name'
     )  
    class Meta:
        model = revised_budget_details
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

class CashflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = cashflow_heads
        fields = '__all__'
        extra_kwargs = {
            'id':{'read_only':True},
            'created_on':{'read_only': True},
            'altered_by':{'write_only': True}
        }

class BudgetCashflowSerializer(serializers.ModelSerializer):
    cashflow_head = CashflowSerializer()
    class Meta:
        model = budget_cashflow_details
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


class RevisedBudgetCashflowSerializer(serializers.ModelSerializer):
    cashflow_head = CashflowSerializer()
    class Meta:
        model = revised_budget_cashflow_details
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

