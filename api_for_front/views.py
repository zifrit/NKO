from django.db.models import Prefetch, F, Count, Q

from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from rest_framework import generics, status, mixins
from django.contrib.auth.models import Group, User
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from my_user.models import UserProfile
from api_for_front.my_utils import check_errors
from . import models, serializers
from .tasks import create_fields_for_step
from django.db import transaction


class SchemaSteps(ModelViewSet):
    """
    CRUd для модели этап
    """
    serializer_class = serializers.CreateStepSchemaSerializer
    queryset = models.StepSchema.objects.all()

    def perform_create(self, serializer):
        with transaction.atomic():
            step = serializer.save()
            create_fields_for_step.delay(step.pk)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateStepSchemaSerializer
        elif self.request.method == 'PUT':
            return serializers.UpdateStepSchemaSerializer
        return serializers.CreateStepSchemaSerializer

    @extend_schema(
        examples=[OpenApiExample(
            "Create example",
            value={
                "id_template_main_project": 0,
                "new_name": 'string',
                "id_template": 0,
                "noda_front": 'string',
                "placement": {
                    "x": "x",
                    "y": "y",
                },
            }
        )]
    )
    def create(self, request, *args, **kwargs):
        data = request.data
        error = check_errors.check_error(
            tag_error={'id_template_main_project': int,
                       'new_name': str,
                       'id_template': int,
                       'noda_front': str,
                       'placement': dict},
            check_data=data)
        if error:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)
        try:
            copy_schema = models.StepTemplates.objects.get(pk=data['id_template']).schema
        except models.Step.DoesNotExist:
            return Response({"error": 'There is no such scheme'}, status=status.HTTP_400_BAD_REQUEST)
        copy_schema.pk = None
        copy_schema._state.adding = True
        copy_schema.name = data['new_name']
        copy_schema.original = False
        copy_schema.noda_front = data['noda_front']
        copy_schema.placement = data['placement']
        copy_schema.template_project_id = data['id_template_main_project']
        copy_schema.save()
        return Response(serializers.CreateStepSchemaSerializer(instance=copy_schema).data, status=status.HTTP_200_OK)

    @extend_schema(examples=[OpenApiExample(
        "put example",
        value={
            "name": 'step name',
            "step_fields_schema": [
                {
                    "type": "type_filed",
                    "label": "label",
                    "data": "{}"
                }
            ]
        }
    )])
    def update(self, request, *args, **kwargs):
        return super(SchemaSteps, self).update(request, *args, **kwargs)
        # return Response(serializers.UpdateStepSchemaSerializer(
        #     instance=models.StepSchema.objects.get(id=kwargs['pk'])).data)
        # if not request.data.get('fields', False):
        #     return Response({'Error': 'There are no fields'}, status=status.HTTP_400_BAD_REQUEST)
        # if not request.data.get('name', False):
        #     return Response({'Error': 'There are no name'}, status=status.HTTP_400_BAD_REQUEST)
        #
        # for field in request.data.get('fields'):
        #     try:
        #         models.StepFields.objects.filter(pk=field.pop('id')).update(field=field)
        #     except KeyError:
        #         models.StepFields.objects.create(field=field, step_id=kwargs['pk'])
        #     except AttributeError:
        #         return Response({'Error': 'Error'}, status=status.HTTP_400_BAD_REQUEST)
        # models.Step.objects.filter(pk=kwargs['pk']).update(name=request.data.get('name', F('name')))
        #
        # return Response(serializers.ViewStepSerializer(
        #     instance=models.Step.objects.select_related('project').prefetch_related('fields').only(
        #         'project__name', 'name', 'placement', 'noda_front').get(pk=kwargs['pk'])).data)

    @extend_schema(examples=[OpenApiExample(
        "Put example",
        value={
            'id_project': 0,
        }
    )])
    @action(methods=['put'], detail=True, url_path='set-start')
    def set_start(self, request, pk):
        errors = {}
        data = request.data
        if not data.get('id_project', False) or (not data['id_project'] and isinstance(data['id_project'], int)):
            errors['id_project'] = 'There is no field id_project or equals zero'
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        if models.StepSchema.objects.filter(template_project=data['id_project'], first_in_project=True).exists():
            return Response({'error': 'The initial stage has already been set'}, status=status.HTTP_400_BAD_REQUEST)
        models.StepSchema.objects.filter(pk=pk).update(first_in_project=True)
        return Response({'status': True}, status=status.HTTP_200_OK)

    @extend_schema(examples=[OpenApiExample(
        "Put example",
        value={
            'id_project': 0,
        }
    )])
    @action(methods=['put'], detail=True, url_path='remove-start')
    def remove_start(self, request, pk):
        errors = {}
        data = request.data
        if not data.get('id_project', False) or (not data['id_project'] and isinstance(data['id_project'], int)):
            errors['id_project'] = 'There is no field id_project or equals zero'
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        models.StepSchema.objects.filter(pk=pk).update(first_in_project=False)
        return Response({'status': True}, status=status.HTTP_200_OK)

    @extend_schema(examples=[OpenApiExample(
        "Put example",
        value={
            'id_project': 0,
        }
    )])
    @action(methods=['put'], detail=True, url_path='set-last')
    def set_last(self, request, pk):
        errors = {}
        data = request.data
        if not data.get('id_project', False) or (not data['id_project'] and isinstance(data['id_project'], int)):
            errors['id_project'] = 'There is no field id_project or equals zero'
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        if models.StepSchema.objects.filter(template_project=data['id_project'], last_in_project=True).exists():
            return Response({'error': 'The initial stage has already been set'}, status=status.HTTP_400_BAD_REQUEST)
        models.StepSchema.objects.filter(pk=pk).update(last_in_project=True)
        return Response({'status': True}, status=status.HTTP_200_OK)

    @extend_schema(examples=[OpenApiExample(
        "Put example",
        value={
            'id_project': 0,
        }
    )])
    @action(methods=['put'], detail=True, url_path='remove-last')
    def remove_last(self, request, pk):
        errors = {}
        data = request.data
        if not data.get('id_project', False) or (not data['id_project'] and isinstance(data['id_project'], int)):
            errors['id_project'] = 'There is no field id_project or equals zero'
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        models.StepSchema.objects.filter(pk=pk).update(last_in_project=False)
        return Response({'status': True}, status=status.HTTP_200_OK)


class ListUserStep(generics.ListAPIView):
    serializer_class = serializers.ViewStepSerializer

    def get_queryset(self):
        return models.Step.objects.filter(users_editor=self.request.user, active=True).only('name', 'id')

    @extend_schema(examples=[OpenApiExample(
        "get example",
        value={
            'id': 0,
            'name': "sting"
        }
    )])
    def get(self, request, *args, **kwargs):
        return super(ListUserStep, self).get(request, *args, **kwargs)


class RetrieveStep(generics.RetrieveAPIView):
    serializer_class = serializers.RetrieveStepSerializer
    queryset = models.Step.objects.select_related('project').prefetch_related('fields').only(
        'project__name', 'name', 'placement', 'noda_front')


class MainKoViewSet(mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    """
    CRUd для главной модели
    """
    serializer_class = serializers.ListMainKoSerializer
    queryset = models.MainKo.objects.all().only(
        'name', 'date_create', 'date_start', 'date_end', 'last_change', 'user__username').select_related('user'). \
        annotate(count_step=Count('steps'), finished_steps=Count('steps', filter=Q(steps__finished=True)), )
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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        # serializer.save(user_id=1)

    @extend_schema(examples=[OpenApiExample(
        "get example",
        value={
            "id": 0,
            "name": 'test name',
            "steps": [
                {
                    "id": 0,
                    "placement": {
                        "x": "x",
                        "y": "y",
                    },
                    "name": "test12",
                    "project": "test",
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
                    "id": 0,
                    "start_id": 0,
                    "end_id": 0,
                    "description": "string",
                    "color": "string"
                }
            ],
            "files": [
                {
                    "file_name": "string",
                    "link_field": 0,
                    "path_file": 'sting',
                }
            ],
        },
    )])
    def retrieve(self, request, *args, **kwargs):
        query = models.MainKo.objects.prefetch_related(
            Prefetch('steps', queryset=models.Step.objects.all().only('id', 'placement', 'name', 'project__id',
                                                                      'noda_front')),
            Prefetch('steps__fields', queryset=models.StepFields.objects.all()),
            Prefetch('steps__step_files', queryset=models.StepFiles.objects.all()),
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
            "last_change": "2023-09-21",
            "active": "True/False",
            "template_ko": 0,
            "count_step": 0,
            "finished_steps": 0
        })])
    def list(self, request, *args, **kwargs):
        return super(MainKoViewSet, self).list(request, *args, **kwargs)

    @action(detail=True, methods=['get'])
    def finished_steps(self, request, pk=None):
        steps = models.Step.objects.filter(project_id=pk, finished=True).prefetch_related(
            Prefetch('fields', queryset=models.StepFields.objects.all()),
            Prefetch('step_files', queryset=models.StepFiles.objects.only('file_name', 'path_file')),
        ).only('name')
        data = {}
        for step in steps:
            data[step.name] = {'fields': [], 'files': []}
            for field in step.fields.all():
                data[step.name]['fields'].append(field.field)
            for file in step.step_files.all():
                data[step.name]['files'].append({'name': file.file_name, 'path': str(file.path_file)})
        return Response(data)

    @extend_schema(examples=[OpenApiExample(
        "get example",
        value={
            "new_name": "string",
            "template_ko": 0,
        })])
    @action(detail=False, methods=['post'], url_path='start-project')
    def start_project(self, request, pk=None):
        main_ko = serializers.CreateMainKoSerializer(data=request.data)
        if main_ko.is_valid():
            main_ko = main_ko.save(user=self.request.user)
            schema = main_ko.template_ko.step_schema.get(first_in_project=True)
            link = models.LinksStep.objects.get(start_id=schema.id, project_id=main_ko.id)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(main_ko.errors, status=status.HTTP_400_BAD_REQUEST)


class TemplateMainKo(ModelViewSet):
    queryset = models.TemplateMainKo.objects.select_related('creator').only('name', 'creator_id',
                                                                            'date_create', 'archive',
                                                                            'creator__first_name', 'creator__last_name',
                                                                            'finished')
    serializer_class = serializers.CreateTemplateMainKoSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @extend_schema(examples=[OpenApiExample(
        "Post example",
        value={
            "name": "string",
        })])
    def create(self, request, *args, **kwargs):
        return super(TemplateMainKo, self).create(request, *args, **kwargs)

    @extend_schema(examples=[OpenApiExample(
        "Post example",
        value={
            "id": 0,
            "creator": "string",
            "name": "string",
            "date_create": "date sting",
            "archive": "True/False",
            "finished": "True/False"
        })])
    def list(self, request, *args, **kwargs):
        self.serializer_class = serializers.ListTemplateMainKoSerializer
        return super(TemplateMainKo, self).list(request, *args, **kwargs)


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


class TemplatesStep(ModelViewSet):
    """
    CRUD для схем этапов
    """
    queryset = models.StepTemplates.objects.select_related('schema').only('schema__step_fields_schema',
                                                                          'name', 'schema__name')
    serializer_class = serializers.CreateTemplatesStepSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
        # serializer.save(user_id=1)

    def perform_destroy(self, instance):
        instance.schema.delete()
        instance.delete()

    @extend_schema(examples=[OpenApiExample(
        "Post example",
        value={
            "name": 'step name',
            "step_fields_schema": [
                {
                    "type": "type_filed",
                    "label": "label",
                    "data": "{}"
                }
            ]
        }
    )])
    def create(self, request, *args, **kwargs):
        return super(TemplatesStep, self).create(request, *args, **kwargs)


class ReplacementPlaceStep(generics.UpdateAPIView):
    """
    Заполнение информации в этапе
    """
    serializer_class = serializers.ExampleSerializer
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
        return Response({'status': True})


class Departments(mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    serializer_class = serializers.DepartmentSerializer
    queryset = Group.objects.prefetch_related('chief', 'chief__user').all()

    @extend_schema(examples=[OpenApiExample(
        "get list example",
        value={
            "id": 0,
            "name": "name department",
            "chief": "chief name",
            "chief_id": "chief identify",
            "count_users": 0,
            "users": []
        }
    )])
    def list(self, request, *args, **kwargs):
        self.queryset = Group.objects.prefetch_related(
            Prefetch('chief', queryset=UserProfile.objects.only('middle_name', 'chief_department_id', 'user_id', 'id')),
            Prefetch('chief__user', queryset=User.objects.only('first_name', 'last_name')),
            Prefetch('user_set', queryset=User.objects.only('id', 'username'))). \
            only(
            'name', 'chief__user__first_name', 'chief__user__last_name', 'chief__middle_name',
        ).annotate(count_users=Count('user'))
        self.serializer_class = serializers.GetDepartmentSerializer
        return super(Departments, self).list(request, *args, **kwargs)

    @extend_schema(description='Пользователь может руководить только одним отделом')
    def create(self, request, *args, **kwargs):
        return super(Departments, self).create(request, *args, **kwargs)

    @extend_schema(examples=[OpenApiExample(
        "get list",
        value=[{
            "id": 0,
            "username": "user1",
            "full_name": "Игорь Иванов Павлович",
            "job": "Frontend",
            "is_chief": 0
        }]
    )])
    @action(detail=True, methods=['get'])
    def users(self, request, pk=None):
        users = User.objects.select_related('profile'). \
            only(
            'username', 'first_name', 'last_name', 'profile__middle_name', 'profile__job', 'profile__is_chief'
        ).filter(groups__in=[pk])
        data = serializers.DepartmentUserSerializer(instance=users, many=True).data
        return Response(data)

    @extend_schema(examples=[OpenApiExample(
        "put example",
        value={
            "id_department": 0,
            "id_users": [],
        }
    )], responses={
        200: OpenApiResponse(response=serializers.ExampleSerializer,
                             examples=[OpenApiExample(
                                 "response",
                                 value={
                                     "status": True,
                                 })])

    })
    @action(detail=False, methods=['put'])
    def add_users(self, request, pk=None):
        errors = {}
        data = request.data
        if not data.get('id_users', False) or (not data['id_users'] and isinstance(data['id_users'], str)):
            errors['id_users'] = 'There is no field id_users or field is empty'
        if not data.get('id_department', False) or (not data['id_users'] and isinstance(data['id_department'], str)):
            errors['id_department'] = 'There is no field id_department or equals zero'
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        users = User.objects.filter(pk__in=data['id_users']).prefetch_related('groups').only('groups')
        for user in users:
            user.groups.add(data['id_department'])
            return Response({"status": True})

    @extend_schema(examples=[OpenApiExample(
        "put example",
        value={
            "id_department": 0,
            "id_users": [],
        }
    )], responses={
        200: OpenApiResponse(response=serializers.ExampleSerializer,
                             examples=[OpenApiExample(
                                 "response",
                                 value={
                                     "status": True,
                                 })])

    })
    @action(detail=False, methods=['put'])
    def remove_users(self, request, pk=None):
        errors = {}
        data = request.data
        if not data.get('id_users', False) or (not data['id_users'] and isinstance(data['id_users'], str)):
            errors['id_users'] = 'There is no field id_users or field is empty'
        if not data.get('id_department', False) or (not data['id_users'] and isinstance(data['id_department'], str)):
            errors['id_department'] = 'There is no field id_department or equals zero'
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        users = User.objects.filter(pk__in=data['id_users']).prefetch_related('groups').only('groups')
        for user in users:
            user.groups.remove(data['id_department'])
            return Response({"status": True})


class CreateDepartmentView(generics.CreateAPIView):
    """
    Созидание отделов
    """
    serializer_class = serializers.DepartmentSerializer
    queryset = Group.objects.prefetch_related('chief')


class DeleteDepartmentView(generics.DestroyAPIView):
    """
    Удаление отдела
    """
    serializer_class = serializers.DepartmentSerializer
    queryset = Group.objects.all()


class GetDepartmentView(generics.ListAPIView):
    """
    Список отделов с руководителями отделов
    """
    queryset = Group.objects.prefetch_related(
        Prefetch('chief', queryset=UserProfile.objects.only('middle_name', 'chief_department_id', 'user_id', 'id')),
        Prefetch('chief__user', queryset=User.objects.only('first_name', 'last_name')),
        Prefetch('user_set', queryset=User.objects.only('id', 'username'))). \
        only(
        'name', 'chief__user__first_name', 'chief__user__last_name', 'chief__middle_name',
    ).annotate(count_users=Count('user'))
    serializer_class = serializers.GetDepartmentSerializer


class DepartmentUserView(generics.ListAPIView):
    """
    Список сотрудников отдела
    """
    serializer_class = serializers.DepartmentUserSerializer

    def get_queryset(self):
        return User.objects.select_related('profile'). \
            only(
            'username', 'first_name', 'last_name', 'profile__middle_name', 'profile__job', 'profile__is_chief'
        ).filter(groups__in=[self.kwargs['pk']])


class AddToDepartmentUserView(generics.GenericAPIView):
    """
    Добавление или удаления сотрудника из отдела
    """
    serializer_class = serializers.ExampleSerializer

    @extend_schema(examples=[OpenApiExample(
        "put example",
        value={
            "id_department": 0,
            "id_users": [],
            "action": 'add or remove'
        }
    )], responses={
        200: OpenApiResponse(response=serializers.ExampleSerializer,
                             examples=[OpenApiExample(
                                 "put example",
                                 value={
                                     "status": True,
                                 })])

    })
    def put(self, request):
        errors = {}
        data = request.data
        if not data.get('action', False) or (not data['action'] and isinstance(data['action'], str)):
            errors['action'] = 'There is no field action or field is empty'
        if not data.get('id_users', False) or (not data['id_users'] and isinstance(data['id_users'], str)):
            errors['id_users'] = 'There is no field id_users or field is empty'
        if not data.get('id_department', False) or (not data['id_users'] and isinstance(data['id_department'], str)):
            errors['id_department'] = 'There is no field id_department or equals zero'
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        users = User.objects.filter(pk__in=data['id_users']).prefetch_related('groups').only('groups')
        if data['action'] == 'add':
            for user in users:
                user.groups.add(data['id_department'])
            return Response({"status": True})
        elif data['action'] == 'remove':
            for user in users:
                user.groups.remove(data['id_department'])
            return Response({"status": True})
        else:
            return Response({"Error": 'Not correct action'}, status=status.HTTP_400_BAD_REQUEST)


class SetGetWhoResponsibleStep(generics.UpdateAPIView, generics.RetrieveAPIView):
    """
    Назначение ответственного, наблюдателя и проверяющего для этапа
    """
    queryset = models.Step.objects.all()
    serializer_class = serializers.ExampleSerializer

    @extend_schema(examples=[OpenApiExample(
        "put example",
        value={
            "responsible_persons_scheme": {
                "users_editor": 0,
                "users_look": [],
                "users_inspecting": 0
            }
        })])
    def put(self, request, *args, **kwargs):
        return super(SetGetWhoResponsibleStep, self).put(request, *args, **kwargs)

    @extend_schema(examples=[OpenApiExample(
        "put example",
        value={}
    )], responses={
        200: OpenApiResponse(response=serializers.ExampleSerializer,
                             examples=[OpenApiExample(
                                 "put example",
                                 value={
                                     "responsible_persons_scheme": {
                                         "users_editor": 0,
                                         "users_look": [],
                                         "users_inspecting": 0
                                     }
                                 })])

    })
    def get(self, request, *args, **kwargs):
        return super(SetGetWhoResponsibleStep, self).get(request, *args, **kwargs)


# todo перенести на воркер
class StepByStep(generics.GenericAPIView):
    @extend_schema(description='Нужно ввести id этапа "step" и он перейдет на следующий этапа')
    def post(self, request, pk):
        with transaction.atomic():
            if not models.LinksStep.objects.filter(start_id=pk).exists():
                last_step = models.Step.objects. \
                    only('id', 'users_editor__id', 'users_look__id',
                         'users_inspecting__id'). \
                    get(pk=pk)
                last_step.users_look.clear()
                last_step.users_look.add(1)
                last_step.users_editor_id = 1
                last_step.users_inspecting_id = 1
                last_step.finished = True
                last_step.active = False
                last_step.save()
                return Response({"Error": 'step has no any links. Set default responsible_persons_scheme'},
                                status=status.HTTP_400_BAD_REQUEST)

            id_nex_step = models.LinksStep.objects.only('end_id').get(start_id=pk).end_id
            old_step = models.Step.objects. \
                only('id', 'responsible_persons_scheme', 'users_editor__id', 'users_look__id', 'users_inspecting__id'). \
                get(pk=pk)
            next_step = models.Step.objects. \
                only('id', 'responsible_persons_scheme', 'users_editor__id', 'users_look__id', 'users_inspecting__id'). \
                get(pk=id_nex_step)
            responsible_persons_scheme = next_step.responsible_persons_scheme
            if not responsible_persons_scheme:
                return Response({"Error": 'nex step has no responsible persons scheme'},
                                status=status.HTTP_400_BAD_REQUEST)

            old_step.users_look.clear()
            old_step.users_look.add(1)
            old_step.users_editor_id = 1
            old_step.users_inspecting_id = 1
            old_step.finished = True
            old_step.active = False
            old_step.save()

            next_step.users_look.add(*responsible_persons_scheme['users_look'])
            next_step.users_editor_id = responsible_persons_scheme['users_editor']
            next_step.users_inspecting_id = responsible_persons_scheme['users_inspecting']
            next_step.active = True
            next_step.save()
        return Response({"Status": True}, status=status.HTTP_200_OK)


class FilesView(generics.ListAPIView):
    serializer_class = serializers.SaveFileSerializer

    def get_queryset(self):
        return models.StepFiles.objects.filter(link_step_id=self.kwargs['pk'])


class FilesCreate(generics.CreateAPIView):
    queryset = models.StepFiles.objects.select_related('link_step')
    serializer_class = serializers.SaveFileSerializer
