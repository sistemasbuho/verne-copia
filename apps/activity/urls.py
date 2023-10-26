from django.urls import path
from .views import *
from .view_ajax import *


urlpatterns = [

    path('create/',RegisterActivity.as_view(), name='create_activity'),
    path('visualize/',watchActivity.as_view(),name='view_activity'),
    path('visualize_user/',watchActivityUser.as_view(),name='view_activity_user'),

    path('visualize/update/<int:id>/', UpdateActivity, name='update_activity'),
    path('visualize/update/upload/<int:pk>/',BasicUploadView, name='upload'),
    path('visualize/update/delete/<int:pk>/',delete_activity, name='delete_activity'),
    path('visualize/update/score/<int:pk>/',Assigned_leguas, name='assigned_leguas'),
    path('buscar_idea/', IdeaAjaxActivity.as_view(), name='buscar_idea'),
    path('buscar_usuario/', UserAjaxActivity.as_view(), name='buscar_usuario'),


	#Task List con AJAX por actividad
	path('list_task/',ListTaskActivity.as_view(), {'parametro_extra':"Listado Proyecto"}, name='list_task'), 
	path('task_create/', CreateTaskActivity.as_view(), name = 'task_create'),
	path('task_update/<int:pk>/', EditTaskActivity.as_view(), name='task_update'),
	path('task_delete/<int:pk>/', DeleteTaskActivity.as_view(), name='task_delete'),

]    