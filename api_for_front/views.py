from django.contrib.auth.models import User
from django.db.models import Prefetch

# Create your views here.
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from . import models, serializers
from django.db import transaction


class test(APIView):
    def get(self, request):
        return Response({'ds': 'as'})


class CreateTextareaFieldAPI(generics.CreateAPIView):
    serializer_class = serializers.CreateTextareaFieldSerializer
    queryset = models.FieldTextarea


class ListRetrieveStep(ReadOnlyModelViewSet):
    serializer_class = serializers.ViewStageSerializer
    queryset = models.Step.objects. \
        select_related('what_project'). \
        prefetch_related(Prefetch('text', queryset=models.FieldText.objects.all().only('text', 'identify')),
                         Prefetch('date', queryset=models.FieldDate.objects.all().only('time', 'identify')),
                         Prefetch('SF_time', queryset=models.FieldStartFinishTime.objects.all().only('start', 'finish',
                                                                                                     'identify')),
                         Prefetch('textarea', queryset=models.FieldTextarea.objects.all().only('textarea', 'identify')),
                         ). \
        only('what_project__name')


class CRUDProjectViewSet(ModelViewSet):
    serializer_class = serializers.MainKoSerializer
    queryset = models.MainProject.objects.prefetch_related('steps',
                                                           'steps__textarea',
                                                           'steps__text',
                                                           'steps__date',
                                                           'steps__SF_time')


class ListCreateMainTableKo(generics.ListCreateAPIView):
    serializer_class = serializers.MainKoSerializer
    queryset = models.MainProject.objects.prefetch_related('steps',
                                                           'steps__textarea',
                                                           'steps__text',
                                                           'steps__date',
                                                           'steps__SF_time')

    def create(self, request, *args, **kwargs):
        super(ListCreateMainTableKo, self).create(request, *args, **kwargs)
        return Response({'status': 'ok'})

    def perform_create(self, serializer):
        return serializer.save(user_id=1)


class CreateTemplatesStep(generics.CreateAPIView):
    queryset = models.StepTemplates.objects.select_related('user')
    serializer_class = serializers.CreateTemplatesStepSerializer

    def perform_create(self, serializer):
        serializer.save(user=User.objects.get(pk=1))

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'status': 'ok'})


class CreateStep(generics.CreateAPIView):
    queryset = models.Step.objects.select_related('templates_schema').prefetch_related('text', 'textarea')
    serializer_class = serializers.CreateStepSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            step = serializer.save()
            schema = step.templates_schema.schema_for_create
            if schema.get('f_text', False):
                item_objects = [models.FieldText(link_step=step)] * schema['f_text']
                models.FieldText.objects.bulk_create(item_objects)
                field_id = models.FieldText.objects.filter(link_step=step).only('id')
                step.text.add(*field_id)
            if schema.get('f_textarea', False):
                item_objects = [models.FieldTextarea(link_step=step)] * schema['f_textarea']
                models.FieldTextarea.objects.bulk_create(item_objects)
                field_id = models.FieldTextarea.objects.filter(link_step=step).only('id')
                step.textarea.add(*field_id)
            if schema.get('f_date', False):
                item_objects = [models.FieldDate(link_step=step)] * schema['f_date']
                models.FieldDate.objects.bulk_create(item_objects)
                field_id = models.FieldDate.objects.filter(link_step=step).only('id')
                step.date.add(*field_id)
            if schema.get('f_s_f_time', False):
                item_objects = [models.FieldStartFinishTime(link_step=step)] * schema['f_s_f_time']
                models.FieldStartFinishTime.objects.bulk_create(item_objects)
                field_id = models.FieldStartFinishTime.objects.filter(link_step=step).only('id')
                step.date.add(*field_id)
            step.save()

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'status': 'ok'})


class AddInfoInStage(generics.RetrieveUpdateAPIView):
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
