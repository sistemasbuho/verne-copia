from django.urls import path
from .views import *
from .view_ajax import *


urlpatterns = [

	#Vistas de Ideas
	path('register/', registerIdea.as_view(), name='register'),
	path('evaluate/',watchIdea.as_view(), name='evaluate'),
 	path('search_colaborator/',SearchColaborator.as_view(), name='search_colaborator'),
    path('search_subregion/',SearchSubregion.as_view(), name='search_subregion'),
 
 
	path('evaluate/<int:fase>/',watchIdeaPhase.as_view(), name='phase_list'),
	path('bank_idea/', IdeaBank.as_view(), name='bank'),
	path('evaluate/update/<int:id>', UpdateIdea, name='update'),
    #path('evaluate/updates/<int:id>', idea_de_prueba.as_view(), name='updates'),
    path('dashboard_innovation/', visualizeDashboardAjax.as_view(), name='general_dashboard'),
  	path('dashboard/ideas_details/<int:id_idea>/', detailsIdeaDashboard, name='idea_details'),
	path('phases/<int:id>/<int:fase>/', PhaseDocumentation, name='phase_documentation'),
	path('evaluate/record/<int:id_idea>', RecordIdea, name='record'),
    path('evaluate/review/<int:id_idea>', revisar_idea, name='review'),
    path('evaluate/revisar_idea_externa', revisar_idea_externa, name='revisar_idea_externa'),


	#Para el Loader more en dashboard y Ideas en Stand By
	path('posts-json/<int:num_posts>/<int:fase>/', EncabezadoDetalleNosotrosJsonListView.as_view(), name='posts-json-view'),

	#Busqueda por AJAX de idea y usuario
	path('buscar_merge/', SearchAjaxIdea.as_view(), name='buscar_merge'),
	path('buscar_colaborador/', SearchUserAjax.as_view(), name='buscar_colaborador'),
	path('buscar_id_idea/', SearchAjaxIdIdeaFilters.as_view(), name='buscar_id_idea'),
    path('buscar_frente/', SearchAjaxIdFrenteFilters.as_view(), name='buscar_frente'),

 	#Lista de externas ideas
 	path('external_idea/',ExternalIdeaList.as_view(), name='external_idea'),
 	path('external_idea_state/<int:pk>',ExternalIdeaState, name='external_idea_state'),
    
	path('aceptar_idea_externa/',aceptar_idea_externa, name='aceptar_idea_externa'),
    path('rechazar_idea_externa/',rechazar_idea_externa, name='rechazar_idea_externa'),
 	
	path('external_idea_state_aproved/<int:pk>',ExternalIdeaStateAproved, name='external_idea_state_aproved'),
 	path('external_idea_state_reached/<int:pk>',ExternalIdeaStateReached, name='external_idea_state_reached'),


	#Lista de opciones de Editar Idea
	path('evaluate/update/inactive/<int:pk>', inactive_idea, name='inactive'),
	path('evaluate/update/question_pain/<int:pk>', QuestionPain, name='question'),
	path('evaluate/update/change_phase/<int:pk>', changePhase.as_view(), name='change'),
	path('evaluate/update/restore/<int:pk>', reactive_idea, name='restore'),
	path('evaluate/update/upload/<int:pk>',BasicUploadView, name='upload'),
	path('evaluate/update/fastrack/<int:pk>', fastrackIdea, name='fastrack'),

	#Task List con AJAX por fase
	path('list_task/',ListTask.as_view(), {'parametro_extra':"Listado Proyecto"}, name='list_task'), 
	path('task_create/', CreateTask.as_view(), name = 'task_create'),
	path('task_update/<int:pk>/', EditTask.as_view(), name='task_update'),
	path('task_delete/<int:pk>/', DeleteTask.as_view(), name='task_delete'),

	#Generar pdf
	path('ticket/<int:pk>/', IdeaGeneratorPdf.as_view(), name='ticket'),

	#Task List con AJAX por idea
	path('list_task_idea/',ListTaskIdea.as_view(), {'parametro_extra':"Listado Proyecto"}, name='list_task_idea'), 
	path('task_create_idea/', CreateTaskIdea.as_view(), name = 'task_create_idea'),
	path('task_update_idea/<int:pk>/', EditTaskIdea.as_view(), name='task_update_idea'),
	path('task_delete_idea/<int:pk>/', DeleteTaskIdea.as_view(), name='task_delete_idea'),

	#Visualizar imagenes y archivos
	
]

