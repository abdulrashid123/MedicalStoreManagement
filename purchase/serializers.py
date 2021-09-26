from rest_framework import serializers
from .models import *


class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = "__all__"


class ManufactureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManuFacture
        fields = "__all__"