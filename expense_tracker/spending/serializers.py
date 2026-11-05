from django.contrib.auth.models import User
from rest_framework import serializers
from spending.models import ExpenseModel

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username',
                'password',
                'email',
                'first_name',
                'last_name']



    def create(self,validated_data):
        u=User.objects.create_user(**validated_data)  
        u.save()
        return u

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model=ExpenseModel
        fields='__all__'
        read_only_fields=['id','created_at','updated_at','owner']