from rest_framework import serializers
from . import models


class CreateStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Step
        fields = ['name', 'what_project', 'templates_schema']


class CreateTemplatesStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StepTemplates
        fields = ['name', 'schema', 'schema_for_create']


class CreateTextareaFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FieldTextarea
        fields = '__all__'


class ViewStageSerializer(serializers.ModelSerializer):
    what_project = serializers.CharField(source='what_project.name')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['text'] = {b.identify: b.text for b in instance.text.all()}
        rep['date'] = {b.identify: b.time for b in instance.date.all()}
        rep['SF_time'] = {b.identify: f'{b.start} : {b.finish}' for b in instance.SF_time.all()}
        rep['textarea'] = {b.identify: b.textarea for b in instance.textarea.all()}
        return rep

    class Meta:
        model = models.Step
        fields = ['id', 'what_project']


class MainKoSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        steps = instance.steps.all()
        rep['steps'] = ViewStageSerializer(instance=steps, many=True).data
        return rep

    class Meta:
        model = models.MainProject
        exclude = ['user']
