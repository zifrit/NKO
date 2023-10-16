from django.db.models import Q
from rest_framework import serializers
from django.contrib.auth.models import Group, User
from . import models
from my_user.models import UserProfile


class CreateStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Step
        fields = ['name', 'project', 'templates_schema']


class CreateTemplatesStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StepTemplates
        fields = ['id', 'name', 'schema', 'user']

    def validate_schema(self, value):
        if not value:
            raise serializers.ValidationError("Schema cannot be empty")
        return value


class CreateTextareaFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FieldTextarea
        fields = '__all__'


class ViewStepSerializer(serializers.ModelSerializer):
    project = serializers.CharField(source='project.name')
    project_id = serializers.IntegerField(source='project.id')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['fields'] = []
        for filed in instance.fields.all():
            filed.field['id'] = filed.id
            rep['fields'].append(filed.field)
        rep['files'] = []
        for file in instance.step_files.all():
            rep['files'].append({
                "file_name": file.file_name,
                "link_field": file.link_field_id,
                "path_file": str(file.path_file),
            })
        return rep

    class Meta:
        model = models.Step
        fields = ['id', 'name', 'project', 'project_id', 'noda_front', 'placement', 'responsible_persons_scheme']


class CreateStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Step
        fields = ['id', 'placement', 'name', 'project', 'templates_schema', 'noda_front']


class UpdateStepSerializer(serializers.ModelSerializer):
    fields = serializers.JSONField()

    class Meta:
        model = models.Step
        fields = ['id', 'name', 'fields']


class StepFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StepFields
        fields = ['id', 'field']


class RetrieveMainKoSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        steps = instance.steps.all()
        rep['steps'] = ViewStepSerializer(instance=steps, many=True).data
        links = models.LinksStep.objects.filter(Q(start_id__in=steps) | Q(end_id__in=steps))
        rep['links'] = LinkStepSerializer(instance=links, many=True).data
        return rep

    class Meta:
        model = models.MainProject
        fields = ['id', 'name']


class ListMainKoSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')

    def to_representation(self, instance):
        my_representation = super().to_representation(instance)
        my_representation['count_step'] = instance.count_step
        my_representation['finished_steps'] = instance.finished_steps
        return my_representation

    class Meta:
        model = models.MainProject
        exclude = ['active']


class CreateMainKoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MainProject
        exclude = ['user', ]


class LinkStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LinksStep
        fields = ['id', 'start_id', 'end_id', 'data']


class ExampleSerializer(serializers.Serializer):
    example = serializers.CharField()


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name', 'chief']

    def create(self, validated_data):
        group = super(DepartmentSerializer, self).create(validated_data)
        validated_data['chief'].chief_department = group
        validated_data['chief'].is_chief = True
        validated_data['chief'].user.groups.add(group)
        validated_data['chief'].user.save()
        validated_data['chief'].save()
        return group


class GetDepartmentSerializer(serializers.ModelSerializer):
    chief = serializers.CharField(source='chief.get_full_name')
    chief_id = serializers.CharField(source='chief.id')

    def to_representation(self, instance):
        my_representation = super(GetDepartmentSerializer, self).to_representation(instance)
        my_representation['count_users'] = instance.count_users
        my_representation['users'] = [{'id': user.id, 'username': user.username} for user in instance.user_set.all()]
        return my_representation

    class Meta:
        model = Group
        fields = ['id', 'name', 'chief', 'chief_id']


class DepartmentUserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='profile.get_full_name')
    job = serializers.CharField(source='profile.job')
    is_chief = serializers.CharField(source='profile.is_chief')

    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'job', 'is_chief']


class SetWhoResponsibleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Step
        fields = ['responsible_persons_scheme']

    def validate_responsible_persons_scheme(self, value: dict):
        keys = ['users_editor', 'users_inspecting', 'users_look']
        print(value)
        if keys != sorted(list(value.keys())):
            raise serializers.ValidationError("Incorrect scheme")
        return value


class SaveFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StepFiles
        fields = '__all__'
