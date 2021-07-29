from rest_framework import serializers
from .models import User


# superAdmin serializer for saving, editing admin/superadmin
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'created_by', 'can_create_company', 'can_edit_company', 'can_delete_company', 'can_view_user_groups', 'can_view_company', 'can_create_user', 'can_edit_user', 'can_delete_user_groups', 'can_edit_user_groups', 'can_create_user_groups', 'can_view_user', 'can_delete_user']
        extra_kwargs = {
            'password': {'write_only': True},
            'id':{'read_only': True},
            'created_on':{'read_only': True}
        }

    def update(self, instance, validated_data):
        if(instance.password):
            for attr, value in validated_data.items():
                if attr == 'password' and value!="null":
                    instance.set_password(value)
                elif attr == 'password' and value=="null":
                    pass
                else:
                    setattr(instance, attr, value)
            instance.save()
            return instance
        else:
            instance.save()
            return instance

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    