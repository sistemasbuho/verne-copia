from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from import_export import resources

class ActivityResource(resources.ModelResource):

    class Meta:
        model = Activity


class TaskResource(resources.ModelResource):

    class Meta:
        model = Task

class ActivityAdmin(ImportExportModelAdmin):
    resource_class = ActivityResource


class TaskAdmin(ImportExportModelAdmin):
    resource_class = TaskResource

admin.site.register(Activity,ActivityAdmin)
admin.site.register(Task,TaskAdmin)



