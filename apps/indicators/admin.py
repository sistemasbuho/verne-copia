from django.contrib import admin
from .models import *


class IndicatorsAdmin(admin.ModelAdmin):

	# limita el numero registros desde el admin
	def has_add_permission(self, request):
		num_objects = self.model.objects.count()
		if num_objects >= 1:
			return False
		else:
			return True
            
admin.site.register(Indicators,IndicatorsAdmin)
