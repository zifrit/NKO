from rest_framework import serializers
from django.contrib.auth.models import User
from . import models


class CreateUserSerializer(serializers.ModelSerializer):
    middle_name = serializers.CharField(source='profile.middle_name')
    job = serializers.CharField(source='profile.job')

    class Meta:
        model = User
        fields = ['username', 'id', 'password', 'middle_name', 'first_name', 'last_name', 'job']

    def validate_middle_name(self, value):
        if not value:
            raise serializers.ValidationError("middle_name cannot be empty")
        return value

    def create(self, validated_data):
        profile = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        models.UserProfile.objects.create(user=user, **profile)
        return user


class ViewUsersSerializer(serializers.ModelSerializer):
    middle_name = serializers.CharField(source='profile.middle_name')
    description = serializers.CharField(source='profile.description')
    job = serializers.CharField(source='profile.job')

    def to_representation(self, instance):
        my_rep = super(ViewUsersSerializer, self).to_representation(instance)
        my_rep['groups'] = [group.name for group in instance.groups.all()]
        return my_rep

    class Meta:
        model = User
        fields = ['id', 'username', 'middle_name', 'first_name', 'last_name', 'description', 'groups', 'job']
        read_only_fields = ['groups']
