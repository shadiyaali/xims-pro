from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password



from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'id', 
            'company_name', 
            'company_admin_name', 
            'user_id', 
            'email_address', 
            'password', 
            'phone_no1', 
            'phone_no2', 
            'company_logo'
        ]

    def create(self, validated_data):
        password = validated_data.get('password')
        if password:
            validated_data['password'] = make_password(password)
        return Company.objects.create(**validated_data)


    
class CompanyGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        
        
        
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['name']   

class CompanySingleSerializer(serializers.ModelSerializer):
   
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = '__all__'

class CompanyUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Company
        fields = ['id', 'company_name', 'company_admin_name', 'user_id', 'email_address', 'password', 
                  'phone_no1', 'phone_no2', 'company_logo' ]
    
    def update(self, instance, validated_data):
        password = validated_data.get('password')
        if password:
            validated_data['password'] = make_password(password)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
    
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name']