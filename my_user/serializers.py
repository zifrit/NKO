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
    middle_name = serializers.CharField(source='profile.middle_name')
    description = serializers.CharField(source='profile.description')

    def to_representation(self, instance):
        my_rep = super(ViewUsersSerializer, self).to_representation(instance)
        my_rep['groups'] = [group.name for group in instance.groups.all()]
        return my_rep

    class Meta:
        model = User
        fields = ['id', 'username', 'middle_name', 'first_name', 'last_name', 'description', 'groups']
        read_only_fields = ['groups']
