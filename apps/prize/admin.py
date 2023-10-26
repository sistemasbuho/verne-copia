from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from import_export import resources


class PrizeResource(resources.ModelResource):
    class Meta:
        model = Prize

class PrizeAdmin(ImportExportModelAdmin):
    resource_class = PrizeResource


class ActionResource(resources.ModelResource):
    class Meta:
        model = Action

class ActionAdmin(ImportExportModelAdmin):
    resource_class = ActionResource


class UserLeguasResource(resources.ModelResource):
    class Meta:
        model = UserLeguas

class UserLeguasAdmin(ImportExportModelAdmin):
    resource_class = UserLeguasResource


class AssignedPrizeResource(resources.ModelResource):
    class Meta:
        model = AssignedPrize

class AssignedPrizeAdmin(ImportExportModelAdmin):
    resource_class = AssignedPrizeResource


admin.site.register(Prize,PrizeAdmin)
admin.site.register(Action,ActionAdmin)
admin.site.register(UserLeguas,UserLeguasAdmin)
admin.site.register(AssignedPrize,AssignedPrizeAdmin)