from rest_framework import serializers
from .models import *


class MobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mobile
        fields = ("id","brand","model","colour","price")