# coding=utf-8
from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    primary_address = serializers.CharField()

    class Meta:
        model = Customer
        fields = Customer.Config.list_display_fields + ('id',)
        read_only_fields = (
            'id', 'date_joined'
        )
