# coding=utf-8
from django.core.urlresolvers import reverse
from rest_framework import serializers
from .models import ExpressOrder


# Serializer for ExpressOrder
class ExpressOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpressOrder
