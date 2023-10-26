from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from apps.idea.views import visualizeDashboardUser
from django.views.generic import TemplateView
from apps.home.views import *


#Modulos del API
from rest_framework import routers
from apps.idea.api.api_rest import UserViewSet,IdeaViewSet,PhaseViewSet
from apps.meeting.api.api_rest import MeetingViewSet,UserVotesgViewSet
from apps.activity.api.api_rest import ActivityViewSet
from apps.prize.api.api_rest import PrizeViewSet,ActionViewSet,LeguasViewSet
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Documentación API')
router = routers.DefaultRouter()
router.register(r'usuario', UserViewSet, basename='usuario')
router.register(r'idea', IdeaViewSet, basename='idea')
router.register(r'reunion', MeetingViewSet, basename='reunion')
router.register(r'votacion', UserVotesgViewSet, basename='votacion')
router.register(r'actividad', ActivityViewSet, basename='actividad')
router.register(r'premios', PrizeViewSet, basename='premios')
router.register(r'acciones', ActionViewSet, basename='acciones')
router.register(r'leguas', LeguasViewSet, basename='leguas')
router.register(r'fases', PhaseViewSet, basename='fases')


urlpatterns = [
	path('admin/', admin.site.urls, name = 'admin_django'),

	#API
    path('api/v1/', include(router.urls)),
    path(r'documentacion/', schema_view), #Documentación Principal 

    #Autenticación Google
    #path('accounts/', include('allauth.urls')), # new

	#Autenticación Google
    path("login", login_request, name="login"),
    path("logout", logout_request, name= "logout"),
    path('microsoft/', include('microsoft_auth.urls', namespace='microsoft')),
	#Llamado a las apps para crear la ruta
	path('ideas/',include(('apps.idea.urls','idea'))),
	path('meeting/',include(('apps.meeting.urls','meeting'))),
	path('prize/',include(('apps.prize.urls','prize'))),
	path('activity/',include(('apps.activity.urls','activity'))),
	path('dashboard/', visualizeDashboardUser, name='dashboard'),
	path('users/',include(('apps.users.urls','users'))),
	path('indicador/',include(('apps.indicators.urls','indicator'))),

	#URL Landing Page
	path('', ViewHome, name='home'),
	path('sign_in', LoginPage, name='singin'),

    #Manejo de errores
	path('404/', TemplateView.as_view(template_name="404.html")),
    path('500/', TemplateView.as_view(template_name="500.html")),
    path('403/', TemplateView.as_view(template_name="403.html")),
  	path('ckeditor/', include('ckeditor_uploader.urls')),

]
 

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	import debug_toolbar
	urlpatterns = [
		path('__debug__/', include(debug_toolbar.urls)),
	] + urlpatterns    

admin.site.site_header = "Administrador de Verne 2.0"
admin.site.site_title = "Administración de Verne 2.0"
admin.site.index_title = "Administración de Verne 2.0"