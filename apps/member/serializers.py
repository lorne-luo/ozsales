from django.contrib.auth.models import Group, Permission
from rest_framework import serializers

from utils.api.fields import (MediaUrlField, DisplayNestedFKField,
                              VariationImageAPIField, VariationUrlField, FormDataPrimaryKeyRelatedField)
from .models import Seller


class PermissionSerializer(serializers.ModelSerializer):
    ''' Serializer for class Permission '''

    class Meta:
        model = Permission


class GroupSimpleSerializer(serializers.ModelSerializer):
    ''' Serializer for class Group only with name '''

    class Meta:
        fields = ['pk', 'name', ]
        model = Group


class GroupPermissionSerializer(serializers.ModelSerializer):
    ''' Serializer for class Group with nested permissions '''
    permissions_display = DisplayNestedFKField('permissions', serializer=PermissionSerializer)

    class Meta:
        model = Group


class SellerUserSerializer(serializers.ModelSerializer):
    ''' Serializer for class SellUser '''
    groups = FormDataPrimaryKeyRelatedField(many=True, read_only=True, required=False)
    groups_display = DisplayNestedFKField('groups', serializer=GroupPermissionSerializer)

    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Seller
        write_only_fields = ['password']

    def validate_groups(self, source):
        user = self.context['request'].user
        if not user.has_perm('member.add_seller'):
            raise serializers.ValidationError("This user cannot change group memberships.")
        return source

    def validate_username(self, source):
        user = self.context['request'].user
        username = source

        if (not user.has_perm('member.add_seller')) and user.username != username:
            raise serializers.ValidationError("This user cannot change usernames.")

        return source

    # Even though email is not required field in model, we make it required in here.
    # Will not be an issue when multitenancy is merged.
    def validate_email(self, source):
        if len(source) == 0:
            raise serializers.ValidationError("Email cannot be empty.")

        return source

    def validate_password2(self, source):
        password2 = source
        password = self.initial_data['password']
        if password != password2:
            raise serializers.ValidationError('passwords mismatch')

        return source

    def to_internal_value(self, obj):
        if 'password2' in self.fields:
            self.fields.pop('password2')
        return super(SellerUserSerializer, self).to_internal_value(obj)

    def validate_password(self, source):
        password = source
        if password < 4:
            raise serializers.ValidationError("Must be at least 4 characters.")

        return source


class MemberUserSimpleSerializer(serializers.ModelSerializer):
    ''' Serializer for class Seller without nested groups '''

    class Meta:
        model = Seller
        exclude = ['password', 'groups']


class MemberUserNameSerializer(serializers.ModelSerializer):
    ''' Serializer for class Seller only with name '''

    class Meta:
        model = Seller
        fields = ['pk', 'username']


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['name', 'email', 'mobile']
        read_only_fields = ['pk', 'username', 'is_active', 'date_joined']
        extra_kwargs = {'password': {'write_only': True}}
