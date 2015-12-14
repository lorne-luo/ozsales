# coding=utf-8
from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    primary_address_display = serializers.CharField(source='primary_address')

    class Meta:
        model = Customer
        fields = Customer.Config.list_display_fields + ('id', 'primary_address_display')
        read_only_fields = (
            'id', 'date_joined'
        )
