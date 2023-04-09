from rest_framework import serializers
from . import models


class CreateStage(serializers.ModelSerializer):
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
    ss = serializers.IntegerField()

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['text'] = {b.identify: b.text for b in instance.text.all()}
        rep['textarea'] = {b.identify: b.textarea for b in instance.textarea.all()}
        return rep

    class Meta:
        model = models.KoStage
        fields = ['text', 'textarea', 'ss']


class MainKoSerializer(serializers.ModelSerializer):
    pass
