from celery import shared_task


@shared_task
def replace_a_place(list_steps: dict):
    from api_for_front import models
    from django.db import transaction
    with transaction.atomic():
        for key, value in list_steps.items():
            models.Step.objects.select_for_update().filter(pk=int(key)).update(placement=value)


@shared_task
def create_fields_for_step(pk_step: int):
    from api_for_front import models
    from django.db import transaction

    with transaction.atomic():
        step = models.Step.objects.select_related('templates_schema'). \
            only('templates_schema__schema', 'name'). \
            get(id=pk_step)
        fields = step.templates_schema.schema
        step_fields = list()
        for filed in fields:
            step_fields += [models.StepFields(field=filed, step=step)]
        models.StepFields.objects.bulk_create(step_fields)
        step.save()
