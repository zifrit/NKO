from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from six import text_type

from . import models


class CreateUserSerializer(serializers.ModelSerializer):
    middle_name = serializers.CharField(source='profile.middle_name')
    job = serializers.CharField(source='profile.job')
    description = serializers.CharField(source='profile.description')

    class Meta:
        model = User
        fields = ['username', 'id', 'password', 'middle_name', 'first_name', 'last_name', 'job',
                  'description']

    def validate_middle_name(self, value):
        if not value:
            raise serializers.ValidationError("middle_name cannot be empty")
        return value

    def create(self, validated_data):
        profile = validated_data.pop('profile')
        # groups = validated_data.pop('groups')
        user = User.objects.create(**validated_data)
        # user.groups.set(groups)
        user.save()
        models.UserProfile.objects.create(user=user, **profile)
        return user


class ViewUsersSerializer(serializers.ModelSerializer):
    middle_name = serializers.CharField(source='profile.middle_name')
    description = serializers.CharField(source='profile.description')
    job = serializers.CharField(source='profile.job')

    def to_representation(self, instance):
        my_rep = super(ViewUsersSerializer, self).to_representation(instance)
        my_rep['groups'] = [{'id': group.id, 'name': group.name} for group in instance.groups.all()]
        my_rep['last_login'] = instance.last_login
        return my_rep

    class Meta:
        model = User
        fields = ['id', 'username', 'middle_name', 'first_name', 'last_name', 'description', 'job']
        read_only_fields = ['groups', 'last_login']

    def update(self, instance, validated_data):
        profile = validated_data.get('profile')
        instance.profile.middle_name = profile.get('middle_name')
        instance.profile.description = profile.get('description')
        instance.profile.job = profile.get('job')
        instance.username = validated_data.get('username')
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.save()
        instance.profile.save()
        return instance


class PasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    def validate(self, attrs):
        print(attrs)
        if attrs['password1'] == attrs['password2']:
            return super(PasswordSerializer, self).validate(attrs)
        raise serializers.ValidationError("Passwords don't match")


class MyTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(TokenObtainPairSerializer, self).validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = text_type(refresh)
        roles = str(self.user.username)
        if self.user.is_superuser:
            new_token = refresh.access_token
            data['access'] = text_type(new_token)
            data['username'] = text_type(roles)
            data['is_admin'] = True
        else:
            data['access'] = text_type(refresh.access_token)
            data['username'] = text_type(roles)
            data['is_admin'] = False

        return data
