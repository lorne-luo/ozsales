# coding=utf-8
from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    # primary_address = serializers.CharField()
    # name = serializers.SerializerMethodField('get_link')

    class Meta:
        model = Product
        fields = Product.Config.list_display_fields + ('id',)
        # read_only_fields = (
        #     'id', 'date_joined'
        # )

