from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, serializers


class test(APIView):
    def get(self, request):
        return Response({'ds': 'as'})


class CreateApiViewME(generics.CreateAPIView):
    serializer_class = serializers.CreateStage
    queryset = models.KoStage


class CreateTextFieldAPI(generics.CreateAPIView):
    serializer_class = serializers.CreateTextFieldSerializer
    queryset = models.FieldText


class CreateTextareaFieldAPI(generics.CreateAPIView):
    serializer_class = serializers.CreateTextareaFieldSerializer
    queryset = models.FieldTextarea


class ViewListStage(generics.ListAPIView):
    serializer_class = serializers.ViewStageSerializer
    queryset = models.KoStage.objects.prefetch_related('text', 'textarea')
