from django.contrib import admin
from . import models


# Register your models here.


@admin.register(models.MainKo)
class MainKO(admin.ModelAdmin):
    list_display = ['id', 'name', 'user', 'active']
    list_editable = ['active']
    list_display_links = ['id', 'name']
    search_fields = ['name']
    save_on_top = True
    list_per_page = 30


@admin.register(models.TemplateMainKo)
class MainKO(admin.ModelAdmin):
    list_display = ['id', 'name', 'creator', 'archive']
    list_editable = ['archive']
    list_display_links = ['id', 'name']
    search_fields = ['name']
    save_on_top = True
    list_per_page = 30


@admin.register(models.Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'project_id']
    list_display_links = ['id', 'name']
    search_fields = ['name']
    save_on_top = True
    list_per_page = 30


@admin.register(models.StepFields)
class StepFieldsAdmin(admin.ModelAdmin):
    list_display = ['id', 'step']
    list_display_links = ['id', 'step']
    search_fields = ['step__name']
    save_on_top = True
    list_per_page = 30


@admin.register(models.StepFiles)
class StepFilesAdmin(admin.ModelAdmin):
    list_display = ['id', 'link_step', 'link_field']
    list_display_links = ['id', 'link_step', 'link_field']
    search_fields = ['step__name']
    save_on_top = True


@admin.register(models.LinksStep)
class LinksStepAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'start_id', 'end_id', 'color']
    list_display_links = ['id', 'description']
    save_on_top = True
    list_per_page = 30


class StepTemplatesInline(admin.TabularInline):
    model = models.StepTemplates
    extra = 1


@admin.register(models.StepSchema)
class StepSchemaAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'template_project', 'original']
    list_display_links = ['id', 'name']
    search_fields = ['name']
    inlines = [StepTemplatesInline]
    save_on_top = True
    list_per_page = 30


@admin.register(models.StepTemplates)
class StepTemplatesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    search_fields = ['name']
    save_on_top = True
    list_per_page = 30


class BaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'identify', 'name_field']

# admin.site.register(models.FieldText, BaseAdmin)
# admin.site.register(models.FieldTextarea, BaseAdmin)
# admin.site.register(models.FieldDate, BaseAdmin)
# admin.site.register(models.FieldStartFinishTime, BaseAdmin)
