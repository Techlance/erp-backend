from rest_framework import serializers
from .models import User


# superAdmin serializer for saving, editing admin/superadmin
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
        # fields = ['id', 'company_name', 'address', 'country','state', ' email', 'website', 'contact_no', 'base_currency', 'cr_no', 'registration_no', 'tax_id_no', 'vat_id_no', 'year_start_date', 'year_end_date', ' logo', 'created_by', 'created_on']
        extra_kwargs = {
            
            'id':{'read_only': True}
        }

    
    # def create(self, validated_data):
    #     password = validated_data.pop('password', None)
    #     instance = self.Meta.model(**validated_data)
    #     if password is not None:
    #         instance.set_password(password)
    #     instance.save()
    #     return instance

    