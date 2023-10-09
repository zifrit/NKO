from rest_framework import serializers
from django.contrib.auth.models import User
from . import models


class CreateUserSerializer(serializers.ModelSerializer):
    middle_name = serializers.CharField(source='profile.middle_name')
    job = serializers.CharField(source='profile.job')
    description = serializers.CharField(source='profile.description')

    class Meta:
        model = User
        fields = ['username', 'id', 'password', 'middle_name', 'first_name', 'last_name', 'job', 'groups',
                  'description']

    def validate_middle_name(self, value):
        if not value:
            raise serializers.ValidationError("middle_name cannot be empty")
        return value

    def create(self, validated_data):
        profile = validated_data.pop('profile')
        groups = validated_data.pop('groups')
        user = User.objects.create(**validated_data)
        user.groups.set(groups)
        user.save()
        models.UserProfile.objects.create(user=user, **profile)
        return user


class ViewUsersSerializer(serializers.ModelSerializer):
    middle_name = serializers.CharField(source='profile.middle_name')
    description = serializers.CharField(source='profile.description')
    job = serializers.CharField(source='profile.job')

    def to_representation(self, instance):
        my_rep = super(ViewUsersSerializer, self).to_representation(instance)
        my_rep['groups'] = [group.name for group in instance.groups.all()]
        my_rep['last_login'] = instance.last_login
        return my_rep

    class Meta:
        model = User
        fields = ['id', 'username', 'middle_name', 'first_name', 'last_name', 'description', 'groups', 'job']
        read_only_fields = ['groups', 'last_login']


class PasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    def validate(self, attrs):
        print(attrs)
        if attrs['password1'] == attrs['password2']:
            return super(PasswordSerializer, self).validate(attrs)
        raise serializers.ValidationError("Passwords don't match")
