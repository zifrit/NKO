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
        step = models.Step.objects.select_related('templates_schema').\
            only('templates_schema__schema', 'name').\
            get(id=pk_step)
        fields = step.templates_schema.schema
        print(fields)
        for type_field, identify in fields.items():
            if type_field.startswith('f_text'):
                field = models.FieldText.objects.create(link_step=step, identify=identify)
                step.text.add(field.id)
            if type_field.startswith('f_textarea'):
                field = models.FieldText.objects.create(link_step=step, identify=identify)
                step.text.add(field.id)
            if type_field.startswith('f_date'):
                field = models.FieldText.objects.create(link_step=step, identify=identify)
                step.text.add(field.id)
            if type_field.startswith('f_time_interval'):
                field = models.FieldText.objects.create(link_step=step, identify=identify)
                step.text.add(field.id)
        step.save()
