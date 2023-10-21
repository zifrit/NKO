from django.db import transaction

from api_for_front import models


def copy_links(validated_data: dict):
    with transaction.atomic():
        template_ko = validated_data['template_ko']
        main_ko = models.MainKo.objects.create(name=validated_data.get('name', template_ko.name),
                                               user=validated_data['user'], template_ko=template_ko)
        links = models.LinksStep.objects.filter(project_id=template_ko.id, in_template=True)
        for link in links:
            link.pk = None
            link._state.adding = True
            link.project_id = main_ko.id
            link.template_ko = False
            link.save()
    return main_ko
