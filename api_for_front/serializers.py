from rest_framework import serializers
from . import models


class CreateStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Step
        fields = ['name', 'project_id', 'templates_schema']


class CreateTemplatesStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StepTemplates
        fields = ['name', 'schema', 'schema_for_create']


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
        fields = ['id', 'project_id']


class RetrieveMainKoSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['steps'] = {field.id: field.metadata for field in
                        models.Step.objects.filter(pk=instance.pk).only('id', 'metadata')}
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
