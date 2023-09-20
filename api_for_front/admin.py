from django.contrib import admin
from . import models


# Register your models here.


@admin.register(models.MainProject)
class MainKO(admin.ModelAdmin):
    list_display = ['id', 'name', 'user']
    list_display_links = ['id', 'name']
    search_fields = ['name']
    save_on_top = True
    list_per_page = 30


@admin.register(models.Step)
class MainKO(admin.ModelAdmin):
    list_display = ['id', 'name', 'project_id_id']
    list_display_links = ['id', 'name']
    search_fields = ['name']
    save_on_top = True
    list_per_page = 30


@admin.register(models.LinksStep)
class MainKO(admin.ModelAdmin):
    list_display = ['id', 'description', 'start_id', 'end_id', 'color']
    list_display_links = ['id', 'description']
    save_on_top = True
    list_per_page = 30


@admin.register(models.StepTemplates)
class MainKO(admin.ModelAdmin):
    list_display = ['id', 'name', 'user']
    list_display_links = ['id', 'name']
    search_fields = ['name']
    save_on_top = True
    list_per_page = 30


class BaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'identify', 'name_field']


admin.site.register(models.FieldText, BaseAdmin)
admin.site.register(models.FieldTextarea, BaseAdmin)
admin.site.register(models.FieldDate, BaseAdmin)
admin.site.register(models.FieldStartFinishTime, BaseAdmin)
