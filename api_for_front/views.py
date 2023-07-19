from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from . import models, serializers
from django.db import transaction


class test(APIView):
    def get(self, request):
        return Response({'ds': 'as'})


class CreateApiViewME(generics.CreateAPIView):
    serializer_class = serializers.CreateStageSerializer
    queryset = models.Step


class CreateTextFieldAPI(generics.CreateAPIView):
    serializer_class = serializers.CreateTextFieldSerializer
    queryset = models.FieldText


class CreateTextareaFieldAPI(generics.CreateAPIView):
    serializer_class = serializers.CreateTextareaFieldSerializer
    queryset = models.FieldTextarea


class ViewListStage(generics.ListAPIView):
    serializer_class = serializers.ViewStageSerializer
    queryset = models.Step.objects.prefetch_related('text', 'textarea')


class ProjectKOViewSet(ModelViewSet):
    serializer_class = serializers.MainKoSerializer
    queryset = models.MainProject.objects.prefetch_related('stages',
                                                           'stages__textarea',
                                                           'stages__text',
                                                           'stages__date',
                                                           'stages__SF_time')


class ListCreateMainTableKo(generics.ListCreateAPIView):
    serializer_class = serializers.MainKoSerializer
    queryset = models.MainProject.objects.prefetch_related('stages',
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
    queryset = models.Step.objects.prefetch_related('text', 'textarea')
    serializer_class = serializers.CreateStageSerializer

    def create(self, request, *args, **kwargs):
        data = self.request.data
        with transaction.atomic():
            stage = models.Step.objects.create(
                date_create=datetime.today(),
                date_end=datetime.today(),
                date_start=datetime.today(),
                # user=self.request.user,
                user_id=1,
                name=data.get('name', 'Example'),
                structure_step=data.get('structure', {})
            )
            if data.get('f_text', False):
                for _ in range(data['f_text']):
                    mass_id = []
                    ftt = models.FieldText.objects.create()
                    mass_id.append(ftt.id)
                    stage.text.add(*mass_id)
            if data.get('f_textarea', False):
                for _ in range(data['field_textarea']):
                    mass_id = []
                    ftt = models.FieldTextarea.objects.create()
                    mass_id.append(ftt.id)
                    stage.textarea.add(*mass_id)
            if data.get('f_date', False):
                for _ in range(data['field_date']):
                    mass_id = []
                    ftt = models.FieldDate.objects.create()
                    mass_id.append(ftt.id)
                    stage.date.add(*mass_id)
            if data.get('f_s_f_time', False):
                for _ in range(data['f_s_f_time']):
                    mass_id = []
                    ftt = models.FieldStartFinishTime.objects.create()
                    mass_id.append(ftt.id)
                    stage.SF_time.add(*mass_id)
            stage.save()
        return Response({'stage_id': stage.id})


class AddIngoInStage(generics.RetrieveUpdateAPIView):
    queryset = models.Step.objects.prefetch_related('text', 'textarea')
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
