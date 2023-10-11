from django.contrib.auth.models import User

# Create your views here.
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from . import serializers


class MyToken(TokenObtainPairView):
    serializer_class = serializers.MyTokenSerializer


class UserModelViewSet(ModelViewSet):
    queryset = User.objects.select_related('profile').prefetch_related('groups'). \
        only(
        'username', 'first_name', 'last_name', 'profile__middle_name', 'profile__description', 'profile__job',
        'last_login'
    )
    serializer_class = serializers.CreateUserSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET' or self.request.method == 'PUT':
            return serializers.ViewUsersSerializer
        return serializers.CreateUserSerializer

    def create(self, request, *args, **kwargs):
        user = super(UserModelViewSet, self).create(request, *args, **kwargs)
        return Response(user.data)

    @extend_schema(examples=[OpenApiExample(
        "Set password",
        value={
            "password1": "string",
            "password2": "string"
        }
    )], responses={
        200: OpenApiResponse(response=serializers.PasswordSerializer,
                             examples=[OpenApiExample(
                                 "confirm set password",
                                 value={'status': 'password set'})]),
        400: OpenApiResponse(response=serializers.PasswordSerializer,
                             examples=[OpenApiExample(
                                 "error set password",
                                 value={'status': 'Passwords don\'t match'})]),
    })
    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = serializers.PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password1'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
