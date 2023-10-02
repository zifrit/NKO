from rest_framework import serializers
from django.contrib.auth.models import User
from . import models


class CreateUserSerializer(serializers.ModelSerializer):
    middle_name = serializers.CharField(source='profile.middle_name')

    class Meta:
        model = User
        fields = ['username', 'id', 'password', 'middle_name', 'first_name', 'last_name']

    def create(self, validated_data):
        profile = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        models.UserProfile.objects.create(middle_name=profile['middle_name'], user=user)
        return user


class ViewUsersSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='profile.get_full_name')

    class Meta:
        model = User
        fields = ['id', 'username', 'full_name']
