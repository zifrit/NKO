from django.contrib import admin
from . import models


# Register your models here.


@admin.register(models.MainProject)
class MainKO(admin.ModelAdmin):
    list_display = ['id', 'name', 'user']
    list_display_links = ['id', 'name']


admin.site.register(models.FieldText)
admin.site.register(models.Step)
admin.site.register(models.FieldTextarea)
admin.site.register(models.FieldDate)
admin.site.register(models.FieldStartFinishTime)
