from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from import_export import resources

class MeetingResource(resources.ModelResource):
    class Meta:
        model = Meeting

class MeetingAdmin(ImportExportModelAdmin):
    resource_class = MeetingResource


class UserVotesResource(resources.ModelResource):
    class Meta:
        model = UserVotes

class UserVotesAdmin(ImportExportModelAdmin):
    resource_class = UserVotesResource


admin.site.register(Meeting,MeetingAdmin)
admin.site.register(UserVotes,UserVotesAdmin)
