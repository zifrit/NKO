from celery import shared_task


@shared_task
def replace_a_place(list_steps: dict):
    from api_for_front import models
    from django.db import transaction
    with transaction.atomic():
        for key, value in list_steps.items():
            models.Step.objects.select_for_update().filter(pk=int(key)).update(metadata=value)


@shared_task
def create_fields_fro_step(pk_step: int):
    from api_for_front import models
    from django.db import transaction

    with transaction.atomic():
        step = models.Step.objects.get(pk=pk_step)
        schema = step.templates_schema.schema_for_create
        if schema.get('f_text', False):
            item_objects = [models.FieldText(link_step=step)] * schema['f_text']
            models.FieldText.objects.bulk_create(item_objects)
            field_id = models.FieldText.objects.filter(link_step=step).only('id')
            step.text.add(*field_id)
        if schema.get('f_textarea', False):
            item_objects = [models.FieldTextarea(link_step=step)] * schema['f_textarea']
            models.FieldTextarea.objects.bulk_create(item_objects)
            field_id = models.FieldTextarea.objects.filter(link_step=step).only('id')
            step.textarea.add(*field_id)
        if schema.get('f_date', False):
            item_objects = [models.FieldDate(link_step=step)] * schema['f_date']
            models.FieldDate.objects.bulk_create(item_objects)
            field_id = models.FieldDate.objects.filter(link_step=step).only('id')
            step.date.add(*field_id)
        if schema.get('f_s_f_time', False):
            item_objects = [models.FieldStartFinishTime(link_step=step)] * schema['f_s_f_time']
            models.FieldStartFinishTime.objects.bulk_create(item_objects)
            field_id = models.FieldStartFinishTime.objects.filter(link_step=step).only('id')
            step.date.add(*field_id)
        step.save()
