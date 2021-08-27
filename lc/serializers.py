from rest_framework import serializers
from .models import lc, lc_docs, lc_amend
from Company.models import cost_center, ledger_master
from Company.serializers import GetLedgerMasterField,GetCostCenterField, CurrencySerializer
class LCSerializer(serializers.ModelSerializer):
    #id = serializers.CharField(source='lc_no')
    id = serializers.SerializerMethodField('get_alternate_name', read_only=True)
    class Meta:
        model = lc
        fields = '__all__'
        extra_kwargs = {
            
            'id':{'read_only': True},
            'created_on':{'read_only': True},
            'lc_no': {'read_only': True},
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
    def get_alternate_name(self, obj):
        return obj.lc_no

class GetLCSerializer(serializers.ModelSerializer):
    #id = serializers.CharField(source='lc_no')
    id = serializers.SerializerMethodField('get_alternate_name', read_only=True)
    cost_center = GetCostCenterField()
    party_code = GetLedgerMasterField()
    bank_ac = GetLedgerMasterField()
    base_currency = CurrencySerializer()
    class Meta:
        model = lc
        fields = '__all__'
        extra_kwargs = {
            
            'id':{'read_only': True},
            'created_on':{'read_only': True},
            'lc_no': {'read_only': True},
            'altered_by': {'write_only': True}
        }
    def get_alternate_name(self, obj):
        return obj.lc_no

class LCDocsSerializer(serializers.ModelSerializer):
    class Meta:
        model = lc_docs
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

class GetLCDocsSerializer(serializers.ModelSerializer):
    lc_id = LCSerializer()  
    class Meta:
        model = lc_docs
        fields = '__all__'
        extra_kwargs = {
            'id':{'read_only': True},
            'created_on':{'read_only': True},
            'altered_by': {'write_only': True}
        }
class LCAmendSerializer(serializers.ModelSerializer):
    class Meta:
        model = lc_amend
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


