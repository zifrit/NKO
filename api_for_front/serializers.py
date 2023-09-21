from django.db.models import Q
from rest_framework import serializers
from . import models


class CreateStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Step
        fields = ['name', 'project_id', 'templates_schema', 'metadata']


class CreateTemplatesStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StepTemplates
        fields = ['id', 'name', 'schema', 'example_metadata']


class CreateTextareaFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FieldTextarea
        fields = '__all__'


class ViewStepSerializer(serializers.ModelSerializer):
    project_id = serializers.CharField(source='project_id.name')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['text'] = {field.identify: field.text for field in instance.text.all()}
        rep['date'] = {field.identify: field.time for field in instance.date.all()}
        rep['SF_time'] = {field.identify: f'{field.start} : {field.finish}' for field in instance.SF_time.all()}
        rep['textarea'] = {field.identify: field.textarea for field in instance.textarea.all()}
        return rep

    class Meta:
        model = models.Step
        fields = ['id', 'project_id', 'metadata']


class RetrieveMainKoSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        steps = models.Step.objects.filter(project_id=instance.pk).only('id', 'metadata')
        rep['steps'] = {field.id: field.metadata for field in steps}
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
        exclude = ['structure_project']


class LinkStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LinksStep
        fields = '__all__'
