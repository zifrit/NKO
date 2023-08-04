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
    queryset = models.Step.objects.prefetch_related('text', 'textarea')
    serializer_class = serializers.CreateStepSerializer

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            step = self.perform_create(serializer)
            data = request.data
            if data.get('f_text', False):
                for _ in range(data['f_text']):
                    mass_id = []
                    ftt = models.FieldText.objects.create(link_step=step)
                    mass_id.append(ftt.id)
                    step.text.add(*mass_id)
            if data.get('f_textarea', False):
                for _ in range(data['field_textarea']):
                    mass_id = []
                    ftt = models.FieldTextarea.objects.create(link_step=step)
                    mass_id.append(ftt.id)
                    step.textarea.add(*mass_id)
            if data.get('f_date', False):
                for _ in range(data['field_date']):
                    mass_id = []
                    ftt = models.FieldDate.objects.create(link_step=step)
                    mass_id.append(ftt.id)
                    step.date.add(*mass_id)
            if data.get('f_s_f_time', False):
                for _ in range(data['f_s_f_time']):
                    mass_id = []
                    ftt = models.FieldStartFinishTime.objects.create(link_step=step)
                    mass_id.append(ftt.id)
                    step.SF_time.add(*mass_id)
            step.save()
            headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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
