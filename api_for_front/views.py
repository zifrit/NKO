from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, serializers
from django.db import transaction


class test(APIView):
    def get(self, request):
        return Response({'ds': 'as'})


class CreateApiViewME(generics.CreateAPIView):
    serializer_class = serializers.CreateStageSerializer
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


class ViewMainTableKo(generics.RetrieveAPIView):
    serializer_class = serializers.MainKoSerializer
    queryset = models.MainTableKO.objects.prefetch_related('stages',
                                                           'stages__textarea',
                                                           'stages__text',
                                                           'stages__date',
                                                           'stages__SF_time')


class ListCreateMainTableKo(generics.ListCreateAPIView):
    serializer_class = serializers.MainKoSerializer
    queryset = models.MainTableKO.objects.prefetch_related('stages',
                                                           'stages__textarea',
                                                           'stages__text',
                                                           'stages__date',
                                                           'stages__SF_time')

    def create(self, request, *args, **kwargs):
        super(ListCreateMainTableKo, self).create(request, *args, **kwargs)
        return Response({'status': 'ok'})

    def perform_create(self, serializer):
        return serializer.save(user_id=1)


class CreateStage(generics.CreateAPIView):
    queryset = models.KoStage.objects.prefetch_related('text', 'textarea')
    serializer_class = serializers.CreateStageSerializer

    def create(self, request, *args, **kwargs):
        data = self.request.data
        mass_text_filed = []
        with transaction.atomic():
            if data['text']:
                for i in range(data['count']):
                    m = models.FieldText.objects.create(identify='None', text='None')
                    mass_text_filed.append(m.id)
            stage = models.KoStage.objects.create(
                date_create=datetime.today(),
                date_end=datetime.today(),
                date_start=datetime.today(),
            )
            stage.text.add(*mass_text_filed)
            stage.textarea.add(1)
            stage.save()
        return Response({'stage_id': stage.id})


class AddIngoInStage(generics.RetrieveUpdateAPIView):
    queryset = models.KoStage.objects.prefetch_related('text', 'textarea')
    serializer_class = serializers.ViewStageSerializer

    def update(self, request, *args, **kwargs):
        print(self.get_object().id)
        update = request.data['update']
        if update['text']:
            for key, value in update['text'].items():
                models.FieldText.objects.filter(identify=key).update(text=value)
        if update['textarea']:
            for key, value in update['textarea'].items():
                models.FieldTextarea.objects.filter(identify=key).update(textarea=value)
        return Response({'status': 'ok'})
