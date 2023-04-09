from rest_framework import serializers
from . import models


class CreateStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KoStage
        fields = '__all__'


class CreateTextFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FieldText
        fields = '__all__'


class CreateTextareaFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FieldTextarea
        fields = '__all__'


class ViewStageSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['id_stage'] = instance.id
        rep['text'] = {b.identify: b.text for b in instance.text.all()}
        rep['textarea'] = {b.identify: b.textarea for b in instance.textarea.all()}
        return rep

    class Meta:
        model = models.KoStage
        fields = ['text', 'textarea']


class MainKoSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        stages = instance.stages.all()
        rep['stages'] = ViewStageSerializer(instance=stages, many=True).data
        return rep

    class Meta:
        model = models.MainTableKO
        exclude = ['user']
