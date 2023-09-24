from django.db.models import Q
from drf_spectacular.utils import OpenApiExample
from rest_framework import serializers
from . import models


class CreateStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Step
        fields = ['name', 'project_id', 'templates_schema']


class CreateTemplatesStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StepTemplates
        fields = ['id', 'name', 'schema', 'user']


class CreateTextareaFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FieldTextarea
        fields = '__all__'


class ViewStepSerializer(serializers.ModelSerializer):
    project_id = serializers.CharField(source='project_id.name')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['fields'] = [{'id': filed.id, 'component': filed.field['component'], 'data': filed.field['data']}
                         for filed in instance.fields.all()]
        return rep

    class Meta:
        model = models.Step
        fields = ['id', 'placement', 'name', 'project_id']


class CreateStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Step
        fields = ['id', 'placement', 'name', 'project_id', 'templates_schema']

    def update(self, instance, validated_data):
        print(validated_data)
        return models.Step.objects.all().first()


class UpdateStepSerializer(serializers.ModelSerializer):
    fields = serializers.JSONField()

    class Meta:
        model = models.Step
        fields = ['id', 'name', 'fields']

    def update(self, instance, validated_data):
        print(validated_data)
        return models.Step.objects.all().first()


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

    class Meta:
        model = models.MainProject
        fields = '__all__'


class LinkStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LinksStep
        fields = '__all__'


class CustomResponseSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {"status": "ok"}
