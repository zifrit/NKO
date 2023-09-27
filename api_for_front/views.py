import json

from django.contrib.auth.models import User
from django.db.models import Prefetch, F

# Create your views here.
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from rest_framework import generics, status, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from . import models, serializers
from .tasks import create_fields_for_step, replace_a_place, set_data_step
from django.db import transaction


class Steps(ModelViewSet):
    """
    CRUd для модели этап
    """
    serializer_class = serializers.ViewStepSerializer
    queryset = models.Step.objects. \
        select_related('project_id').prefetch_related('fields').only('project_id__name', 'name', 'placement',
                                                                     'noda_front')

    def perform_create(self, serializer):
        with transaction.atomic():
            step = serializer.save()
            create_fields_for_step.delay(step.pk)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateStepSerializer
        elif self.request.method == 'PUT':
            return serializers.UpdateStepSerializer
        return serializers.ViewStepSerializer

    @extend_schema(examples=[OpenApiExample(
        "create example",
        value={
            "templates_schema": 14,
            "name": "room step",
            "project_id": 1,
            "placement": {
                "x": "x",
                "y": "y",
                "w": "with",
                "h": "height"
            },
            "noda_front": 'some front id'
        }
    )])
    def create(self, request, *args, **kwargs):
        return super(Steps, self).create(request, *args, **kwargs)

    @extend_schema(examples=[OpenApiExample(
        "put example",
        value={
            "name": 'step name',
            "fields": [
                {
                    "id": "id field",
                    "type": "type_filed",
                    "data": {
                        "identify": "type_filed"
                    }
                }
            ]
        }
    )])
    def update(self, request, *args, **kwargs):
        if not request.data.get('fields', False):
            return Response({'Error': 'there are no fields'}, status=status.HTTP_400_BAD_REQUEST)
        if not request.data.get('name', False):
            return Response({'Error': 'there are no name'}, status=status.HTTP_400_BAD_REQUEST)

        for field in request.data.get('fields'):
            try:
                models.StepFields.objects.filter(pk=field.pop('id')).update(field=field)
            except KeyError:
                models.StepFields.objects.create(field=field, step_id=kwargs['pk'])
        models.Step.objects.filter(pk=kwargs['pk']).update(name=request.data.get('name', F('name')))

        return Response(serializers.ViewStepSerializer(
            instance=models.Step.objects.select_related('project_id').prefetch_related('fields').only(
                'project_id__name', 'name', 'placement', 'noda_front').get(pk=kwargs['pk'])).data)


class DeleteStepFiled(generics.DestroyAPIView):
    queryset = models.StepFields.objects.select_related('step').all()
    serializer_class = serializers.StepFieldsSerializer


class MainProjectViewSet(ModelViewSet):
    """
    CRUd для главной модели
    """
    serializer_class = serializers.ListMainKoSerializer
    queryset = models.MainProject.objects.all().only(
        'name', 'date_create', 'date_start', 'date_end', 'last_change', 'user__username').select_related('user')
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter
    ]
    search_fields = [
        "name"
    ]
    filterset_fields = [
        'name',
        'user__username',
    ]
    ordering_fields = [
        'name',
        'date_create',
        'date_start',
    ]

    @extend_schema(examples=[OpenApiExample(
        "get example",
        value={
            "id": 1,
            "name": 'test name',
            "steps": [
                {
                    "id": 1,
                    "placement": {
                        "x": "x",
                        "y": "y",
                        "w": "with",
                        "h": "height"
                    },
                    "name": "test12",
                    "project_id": "test",
                    "fields": [
                        {
                            "type": "type_filed",
                            "data": {
                                "identify": "type_filed"
                            }
                        }
                    ]
                }
            ],
            "links": [
                {
                    "id": 1,
                    "start_id": 1,
                    "end_id": 2,
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
        return super(MainProjectViewSet, self).list(request, *args, **kwargs)

    @extend_schema(examples=[OpenApiExample("Post example", )], description='successful post response {"status": "ok"}')
    def create(self, request, *args, **kwargs):
        return super(MainProjectViewSet, self).create(request, *args, **kwargs)

    @extend_schema(examples=[OpenApiExample(
        "put example",
        value={
            "name": "test name",
            "placements": {
                "id step": {
                    "x": "x",
                    "y": "y",
                    "w": "with",
                    "h": "height"
                }
            }
        }
    )])
    def update(self, request, *args, **kwargs):
        if not request.data.get('placements', False):
            return Response({'Error': 'there are no placements'}, status=status.HTTP_400_BAD_REQUEST)
        replace_a_place.delay(request.data.get('placements'))
        return super(MainProjectViewSet, self).update(request, *args, **kwargs)

    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        serializer.save(user_id=1)


class LinkStepViewSet(ModelViewSet):
    """
    CRUD для связей между этапами
    """
    serializer_class = serializers.LinkStepSerializer
    queryset = models.LinksStep.objects.all()

    @extend_schema(
        description='Returns 404 if start_id == end_id',
        examples=[OpenApiExample(
            "put example",
            value={
                "start_id": 'parents step id',
                "end_id": 'child step ip',
                "data": {
                    "node_from_id": '',
                    "node_to_id": ''
                }
            }
        )]
    )
    def create(self, request, *args, **kwargs):
        if request.data['start_id'] == request.data['end_id']:
            return Response({'message': 'Начало и конец не могут быть одинаковыми'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)


class ListCreateTemplatesStep(generics.ListCreateAPIView):
    """
    Создание и получение списка шаблонов для создания этапов
    """
    queryset = models.StepTemplates.objects.select_related('user')
    serializer_class = serializers.CreateTemplatesStepSerializer

    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        serializer.save(user_id=1)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class DeleteSchema(generics.DestroyAPIView):
    queryset = models.StepTemplates.objects.all()
    serializer_class = serializers.CreateTemplatesStepSerializer


class UpdateSchema(generics.UpdateAPIView):
    queryset = models.StepTemplates.objects.all()
    serializer_class = serializers.CreateTemplatesStepSerializer


class ReplacementPlaceStep(generics.UpdateAPIView):
    """
    Заполнение информации в этапе
    """
    serializer_class = serializers.CustomResponseSerializer
    queryset = models.Step.objects.all()

    @extend_schema(examples=[OpenApiExample(
        "put example",
        value={
            "new_replacement": {
                "x": 0.0,
                "y": 0.0,
            }
        }
    )])
    def put(self, request, *args, **kwargs):
        if not request.data.get('new_replacement', False):
            return Response({'Error': 'there are no new_replacement'}, status=status.HTTP_400_BAD_REQUEST)
        models.Step.objects.filter(pk=kwargs['pk']).update(
            placement=request.data.get('new_replacement', F('placement')))
        return Response({'status': 'ok'})
