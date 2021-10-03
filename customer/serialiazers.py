from rest_framework import serializers
from customer.models import *
from purchase.serializers import *
from django.contrib.auth.models import User
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"

    # def to_representation(self, instance):
    #     response=super().to_representation(instance)
    #     response['medicine']=MedicineSerializer(instance.shop.all()).data
    #     return response

class MedicineTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineTag
        fields = '__all__'
        depth=1

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = "__all__"

    def to_representation(self, instance):
        response=super().to_representation(instance)
        try:
            response['company']=CompanySerializer(instance.company).data["id"]
        except:
            response['company'] = None
        try:
            response['buyer'] = BuyerSerializer(instance.buyer).data["id"]
        except:
            response['buyer'] = None
        try:
            response['manufacture'] = ManufactureSerializer(instance.manufacture).data["id"]
        except:
            response['manufacture'] = None
        return response




class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def to_representation(self, instance):
        response=super().to_representation(instance)
        try:
            response['company']=CompanySerializer(instance.company).data["id"]
        except:
            response['company'] = None
        return response