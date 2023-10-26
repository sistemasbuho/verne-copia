from django.contrib import admin
from .models import *


class MenuLogoAdmin(admin.ModelAdmin):

	#limita el numero registros desde el admin
	def has_add_permission(self, request):
		num_objects = self.model.objects.count()
		if num_objects >= 1:
			return False
		else:
			return True


class MenuAdmin(admin.ModelAdmin):

	#limita el numero registros desde el admin
	def has_add_permission(self, request):
		num_objects = self.model.objects.count()
		if num_objects >= 6:
			return False
		else:
			return True


class BannerHeaderAdmin(admin.ModelAdmin):

	#limita el numero registros desde el admin
	def has_add_permission(self, request):
		num_objects = self.model.objects.count()
		if num_objects >= 1:
			return False
		else:
			return True


class HeaderExploreSectionAdmin(admin.ModelAdmin):

	#limita el numero registros desde el admin
	def has_add_permission(self, request):
		num_objects = self.model.objects.count()
		if num_objects >= 1:
			return False
		else:
			return True


class ExploreSectionAdmin(admin.ModelAdmin):

	#limita el numero registros desde el admin
	def has_add_permission(self, request):
		num_objects = self.model.objects.count()
		if num_objects >= 4:
			return False
		else:
			return True


class ProcessSectionAdmin(admin.ModelAdmin):

	#limita el numero registros desde el admin
	def has_add_permission(self, request):
		num_objects = self.model.objects.count()
		if num_objects >= 4:
			return False
		else:
			return True


class MetricsAdmin(admin.ModelAdmin):

	#limita el numero registros desde el admin
	def has_add_permission(self, request):
		num_objects = self.model.objects.count()
		if num_objects >= 3:
			return False
		else:
			return True


class HeaderTeamSectionAdmin(admin.ModelAdmin):

	#limita el numero registros desde el admin
	def has_add_permission(self, request):
		num_objects = self.model.objects.count()
		if num_objects >= 1:
			return False
		else:
			return True


class FooterAdmin(admin.ModelAdmin):

	#limita el numero registros desde el admin
	def has_add_permission(self, request):
		num_objects = self.model.objects.count()
		if num_objects >= 1:
			return False
		else:
			return True

class MovilizadoresSectionAdmin(admin.ModelAdmin):

	#limita el numero registros desde el admin
	def has_add_permission(self, request):
		num_objects = self.model.objects.count()
		if num_objects >= 1:
			return False
		else:
			return True

class HeaderMovilizadoresSectionAdmin(admin.ModelAdmin):

	#limita el numero registros desde el admin
	def has_add_permission(self, request):
		num_objects = self.model.objects.count()
		if num_objects >= 1:
			return False
		else:
			return True


class HeaderValoresSectionAdmin(admin.ModelAdmin):

	#limita el numero registros desde el admin
	def has_add_permission(self, request):
		num_objects = self.model.objects.count()
		if num_objects >= 1:
			return False
		else:
			return True


class ValoressSectionAdmin(admin.ModelAdmin):

	#limita el numero registros desde el admin
	def has_add_permission(self, request):
		num_objects = self.model.objects.count()
		if num_objects >= 1:
			return False
		else:
			return True


# class PlatformMenuAdmin(admin.ModelAdmin):

# 	#limita el numero registros desde el admin
# 	def has_add_permission(self, request):
# 		num_objects = self.model.objects.count()
# 		if num_objects >= 11:
# 			return False
# 		else:
# 			return True


admin.site.register(Menu,MenuAdmin)
admin.site.register(MenuLogo,MenuLogoAdmin)
admin.site.register(BannerHeader)
admin.site.register(HeaderExploreSection)
admin.site.register(ExploreSection)
admin.site.register(ProcessSection)
admin.site.register(Metrics,MetricsAdmin)
admin.site.register(HeaderTeamSection)
admin.site.register(TeamSection)
admin.site.register(Footer)
admin.site.register(MovilizadoresSection)
admin.site.register(HeaderValoresSection)
admin.site.register(ValoressSection)

# admin.site.register(PlatformMenu,PlatformMenuAdmin)



