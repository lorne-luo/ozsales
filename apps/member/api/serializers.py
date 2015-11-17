'''
Copyright (c) 2013 O7 Technologies Pty Ltd trading as Omniscreen. All Rights Reserved.

O7 Technologies Pty Ltd trading as Omniscreen ("Omniscreen") retains copyright
on all text, source and binary code contained in this software and documentation.
Omniscreen grants Licensee a limited license to use this software,
provided that this copyright notice and license appear on all copies of the software.
The software source code is provided for reference, compilation and porting purposes only
and may not be copied, modified or distributed in any manner and by any means
without prior written permission from Omniscreen.

THIS SOFTWARE AND DOCUMENTATION ARE PROVIDED "AS IS,"
WITHOUT ANY WARRANTY OF ANY KIND. ALL EXPRESS OR IMPLIED CONDITIONS,
REPRESENTATIONS AND WARRANTIES, INCLUDING ANY IMPLIED WARRANTY OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE OR NON-INFRINGEMENT, ARE HEREBY EXCLUDED.
OMNISCREEN SHALL NOT BE LIABLE FOR ANY DAMAGES SUFFERED BY LICENSEE
AS A RESULT OF USING OR MODIFYING THE SOFTWARE OR ITS DERIVATIVES.

IN NO EVENT WILL OMNISCREEN BE LIABLE FOR ANY LOST REVENUE, PROFIT OR DATA,
OR FOR DIRECT, INDIRECT, SPECIAL, CONSEQUENTIAL, INCIDENTAL OR PUNITIVE DAMAGES,
HOWEVER CAUSED AND REGARDLESS OF THE THEORY OF LIABILITY,
ARISING OUT OF THE USE OF OR INABILITY TO USE SOFTWARE,
EVEN IF OMNISCREEN HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
'''
from django.contrib.auth.models import Group, Permission
from rest_framework import serializers

from utils.api.fields import (MediaUrlField, DisplayNestedFKField,
    VariationImageAPIField, VariationUrlField, FormDataPrimaryKeyRelatedField)
from ..models import Seller


class PermissionSerializer(serializers.ModelSerializer):
    ''' Serializer for class Permission '''
    class Meta:
        model = Permission


class GroupSimpleSerializer(serializers.ModelSerializer):
    ''' Serializer for class Group only with name '''
    class Meta:
        fields = ['id', 'name',]
        model = Group


class GroupPermissionSerializer(serializers.ModelSerializer):
    ''' Serializer for class Group with nested permissions '''
    permissions_display = DisplayNestedFKField('permissions', serializer=PermissionSerializer)
    class Meta:
        model = Group


class SellerUserSerializer(serializers.ModelSerializer):
    ''' Serializer for class OmniscreenUser '''
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

    #Even though email is not required field in model, we make it required in here.
    #Will not be an issue when multitenancy is merged.
    def validate_email(self, source):
        if len(source) == 0:
            raise serializers.ValidationError("Email cannot be empty.")

        return source

    def validate_password2(self, attrs, source):
        password2 = attrs.pop(source)
        if attrs['password'] != password2:
            raise serializers.ValidationError('passwords mismatch')

        return attrs

    def to_native(self, obj):
        if 'password2' in self.fields:
            self.fields.pop('password2')
        return super(SellerUserSerializer, self).to_native(obj)

    def validate_password(self, attrs, source):
        if len(attrs[source]) < 4:
            raise serializers.ValidationError("Must be at least 4 characters.")

        return attrs


class OmniscreenUserSimpleSerializer(serializers.ModelSerializer):
    ''' Serializer for class OmniscreenUser without nested groups '''
    # avatar_display = MediaUrlField('avatar')
    # avatar_variations = VariationUrlField('avatar') # shows alls image variations
    class Meta:
        model = Seller
        exclude = ['password', 'groups']


class OmniscreenUserNameSerializer(serializers.ModelSerializer):
    ''' Serializer for class OmniscreenUser only with name '''
    class Meta:
        model = Seller
        fields = ['id', 'username']
