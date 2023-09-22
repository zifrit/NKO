import json

from django.contrib.auth.models import User
from django.db.models import Prefetch

# Create your views here.
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from rest_framework import generics, status, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet

from . import models, serializers
from .tasks import create_fields_fro_step, replace_a_place
from django.db import transaction


class Steps(ModelViewSet):
    """
    CRUd для модели этап
    """
    serializer_class = serializers.ViewStepSerializer
    queryset = models.Step.objects. \
        select_related('project_id').prefetch_related('fields').only('project_id__name', 'name', 'placement')

    def perform_create(self, serializer):
        with transaction.atomic():
            step = serializer.save()
            create_fields_fro_step.delay(step.pk)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateStepSerializer
        return serializers.ViewStepSerializer

    def create(self, request, *args, **kwargs):
        super(Steps, self).create(request, *args, **kwargs)
        return Response({'status': 'asd'}, status=status.HTTP_200_OK)


class MainProjectViewSet(ModelViewSet):
    """
    CRUd для главной модели
    """
    serializer_class = serializers.RetrieveMainKoSerializer
    queryset = models.MainProject.objects.prefetch_related('steps')

    @extend_schema(examples=[OpenApiExample(
        "get example",
        value={
            "id": 1,
            "name": 'somename',
            "steps": {
                "id_step1": 'json metadata',
                "id_step2": 'json metadata',
                "id_step3": 'json metadata',
            },
            "links": [
                {
                    "id": 1,
                    "start_id": 2,
                    "end_id": 3,
                    "description": "string",
                    "color": "string"
                }
            ]
        },
    )])
    def retrieve(self, request, *args, **kwargs):
        query = models.MainProject.objects.prefetch_related(
            Prefetch('steps', queryset=models.Step.objects.all().only('id', 'placement', 'name', 'project_id__id')),
            Prefetch('steps__fields', queryset=models.StepFields.objects.all()),
        ).only('id', 'name').get(pk=kwargs['pk'])
        data = serializers.RetrieveMainKoSerializer(instance=query).data
        return Response(data)

    @extend_schema(examples=[OpenApiExample(
        "get example",
        value={
            "id": 1,
            "user": "admin",
            "name": "test",
            "date_create": "2023-08-04",
            "date_start": "2023-08-04",
            "date_end": "2023-09-21",
            "last_change": "2023-09-21"
        })])
    def list(self, request, *args, **kwargs):
        query = models.MainProject.objects.all().only(
            'name', 'date_create', 'date_start', 'date_end', 'last_change', 'user__username').select_related('user')
        data = serializers.ListMainKoSerializer(instance=query, many=True).data
        return Response(data)

    @extend_schema(examples=[OpenApiExample(
        "Post example",
        value={
            "name": "test"
        }
    )], description='successful post response {"status": "ok"}')
    def create(self, request, *args, **kwargs):
        super(MainProjectViewSet, self).create(request, *args, **kwargs)
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)

    @extend_schema(examples=[OpenApiExample(
        "put example",
        value={
            "name": "test",
            "structures": {
                "id_steps": 'json metadata'
            }
        },
    )], description='successful put response {"status": "ok"}')
    def update(self, request, *args, **kwargs):
        super(MainProjectViewSet, self).update(request, *args, **kwargs)
        if not request.data.get('placements', False):
            return Response({'Error': 'there are no placements'}, status=status.HTTP_400_BAD_REQUEST)
        replace_a_place.delay(request.data.get('placements'))

        return Response({'status': 'ok'}, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class LinkStepViewSet(ModelViewSet):
    """
    CRUD для связей между этапами
    """
    serializer_class = serializers.LinkStepSerializer
    queryset = models.LinksStep.objects.all()

    @extend_schema(
        description='Returns 404 if start_id == end_id'
    )
    def create(self, request, *args, **kwargs):
        if request.data['start_id'] == request.data['end_id']:
            return Response({'message': 'Начало и конец не могут быть одинаковыми'}, status=status.HTTP_400_BAD_REQUEST)
        super().create(request, *args, **kwargs)
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)


class CreateTemplatesStep(generics.CreateAPIView):
    """
    Создание шаблонов для создания этапов
    """
    queryset = models.StepTemplates.objects.select_related('user')
    serializer_class = serializers.CreateTemplatesStepSerializer

    def perform_create(self, serializer):
        serializer.save(user=User.objects.get(pk=1))

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)


class ListSchema(generics.ListAPIView):
    queryset = models.StepTemplates.objects.all()
    serializer_class = serializers.CreateTemplatesStepSerializer


class AddInfoInStage(APIView):
    """
    Заполнение информации в этапе
    """

    @extend_schema(
        responses={
            200: OpenApiResponse(description='{"type_field":{"id_field":"change_info"}\n'
                                             '{"type_field":{"id_field":"change_info"}'),
        }
    )
    def put(self, request):
        data = request.data
        if data.get('text', False):
            for id_filed, value in data['text'].items():
                models.FieldText.objects.filter(id=int(id_filed)).update(text=value)
        if data.get('textarea', False):
            for id_filed, value in data['textarea'].items():
                models.FieldTextarea.objects.filter(id=int(id_filed)).update(textarea=value)
        if data.get('date', False):
            for id_filed, value in data['date'].items():
                models.FieldDate.objects.filter(id=int(id_filed)).update(time=value)
        # todo нужно проверить как сохраняется дата
        # if update['textarea']:
        #     for id_filed, value in update['textarea'].items():
        #         models.FieldTextarea.objects.get(id=id_filed).update(textarea=value)
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)
