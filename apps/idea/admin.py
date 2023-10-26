from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.contrib.auth.models import User

class UserResource(resources.ModelResource):
    class Meta:
        model = User

class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource


class IdeaResource(resources.ModelResource):
    class Meta:
        model = Idea

class IdeaAdmin(ImportExportModelAdmin):
    resource_class = IdeaResource


class GerenciaResource(resources.ModelResource):
    class Meta:
        model = Area

class GerenciaAdmin(ImportExportModelAdmin):
    resource_class = GerenciaResource


class SubregionResource(resources.ModelResource):
    class Meta:
        model = Beneficio

class SubregionAdmin(ImportExportModelAdmin):
    resource_class = SubregionResource


class FrenteResource(resources.ModelResource):
    class Meta:
        model = Frente

class FrenteAdmin(ImportExportModelAdmin):
    resource_class = FrenteResource


class DimensionResource(resources.ModelResource):
    class Meta:
        model = Dimension

class DimensionAdmin(ImportExportModelAdmin):
    resource_class = DimensionResource


class ObjectiveResource(resources.ModelResource):
    class Meta:
        model = Objective

class ObjectiveAdmin(ImportExportModelAdmin):
    resource_class = ObjectiveResource



class PhaseDateResource(resources.ModelResource):
    class Meta:
        model = Phase_Date

class PhaseDateAdmin(ImportExportModelAdmin):
    resource_class = PhaseDateResource


class QuestionPhaseResource(resources.ModelResource):
    class Meta:
        model = QuestionPhase

class QuestionPhaseAdmin(ImportExportModelAdmin):
    resource_class = QuestionPhaseResource


class PhaseResource(resources.ModelResource):
    class Meta:
        model = Phase

class PhaseAdmin(ImportExportModelAdmin):
    resource_class = PhaseResource


class IdeaQuestionPhaseResource(resources.ModelResource):
    class Meta:
        model = IdeaQuestionPhase

class IdeaQuestionPhaseAdmin(ImportExportModelAdmin):
    resource_class = IdeaQuestionPhaseResource


class PriceScoreAdmin(admin.ModelAdmin):

	#limita el numero registros desde el admin
	def has_add_permission(self, request):
		num_objects = self.model.objects.count()
		if num_objects >= 1:
			return False
		else:
			return True
            

admin.site.register(Idea, IdeaAdmin)
admin.site.register(Area,GerenciaAdmin)
admin.site.register(Objective,ObjectiveAdmin)
admin.site.register(Dimension,DimensionAdmin)
admin.site.register(Frente,FrenteAdmin)
admin.site.register(Beneficio,SubregionAdmin)
admin.site.register(QuestionPhase,QuestionPhaseAdmin)
admin.site.register(Phase,PhaseAdmin)
admin.site.register(Phase_Date,PhaseDateAdmin)
admin.site.register(IdeaQuestionPhase,IdeaQuestionPhaseAdmin)
admin.site.register(Task)
admin.site.register(TaskByIdea)
admin.site.register(PriceScore,PriceScoreAdmin)
admin.site.register(ExternalIdea)
