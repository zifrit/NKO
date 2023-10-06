from django.contrib.auth.models import User

# Create your views here.
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from . import serializers


class UserModelViewSet(ModelViewSet):
    queryset = User.objects.select_related('profile').prefetch_related('groups'). \
        only(
        'username', 'first_name', 'last_name', 'profile__middle_name', 'profile__description', 'profile__job'
    )
    serializer_class = serializers.CreateUserSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET' or self.request.method == 'PUT':
            return serializers.ViewUsersSerializer
        return serializers.CreateUserSerializer

    def create(self, request, *args, **kwargs):
        user = super(UserModelViewSet, self).create(request, *args, **kwargs)
        return Response({'User': {
            'id': user.data['id'],
            'first_name': user.data.get('first_name', None),
            'last_name': user.data.get('last_name', None),
            'middle_name': user.data.get('middle_name', None),
            'description': user.data.get('description', None),
            'job': user.data.get('job', None),
        }})
