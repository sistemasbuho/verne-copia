from .models import *
from .forms import *
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import CreateView
from django.db.models import Q
from django.shortcuts import redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from apps.idea.view_ajax import _ListarAjax ,EditTask, DeleteTask



class ListTaskActivity(_ListarAjax): 
	model = Activity
	template_name = 'activity/details.html'
	permission_required = 'idea.view_dashboard'


	def get_context_data(self,**kwargs):
		contexto = {}
		# contexto['form'] = self.form_class
		contexto['verbose_name_model'] = self.model._meta.verbose_name_plural
		
		return contexto

	def get_queryset(self):

		order_by = f"{self.request.GET.get('order_by')}"

		if self.request.GET.get('asc_desc') == 'desc':
			order_by = f'-{order_by}'

		query = Q()
		query.add(Q(id=self.request.GET.get('idea_get_ajax')), Q.AND)

		if self.request.GET.get('filtro'):
			query.add(Q(task__title__icontains=self.request.GET.get('filtro')), Q.AND)

		if self.request.GET.get('search_estado'):
			query.add(Q(task__complete=self.request.GET.get('search_estado')), Q.AND)


		queryset = self.model.objects.filter(
			query).values(
				'task__id',
				'task__user__email',
				'task__title',
				'task__description',
				'task__complete',
				'task__created'
			).exclude(task=None).order_by(order_by)
		
		print('query---------------',queryset)
				
		return queryset


class CreateTaskActivity(PermissionRequiredMixin,CreateView):
	model = Task
	permission_required = 'idea.view_dashboard'
	form_class = TaskCreateForm
	template_name = 'task/activity/create_task.html'
	success_url = reverse_lazy('activity:list_task')
	success_message = 'La tarea fue creada con éxito'
	error_message = 'No se guardó con éxito.'
	
	def post(self, request, *args, **kwargs):

		if request.is_ajax():
			form_header = dict(request.POST.lists())
			form = self.form_class(request.POST)
	
			#print("form_header['fase_form_create']: ", form_header['fase_form_create'])
			#print("form_header['id_form_create']: ", form_header['id_form_create'])

			#print("self.kwargs['fase_form_create'] ",self.kwargs['fase_form_create'])
			#print("self.kwargs['id_form_create'] ",self.kwargs['id_form_create'])



			#Foreing key
			if  'user' in form_header:
				user_query = User.objects.filter(pk__in=form_header['user'])
				form.fields['user'].queryset = user_query 
			else:
				form.fields['user'].queryset = User.objects.none()

			if form.is_valid():
				task_save= form.save()
				
				#Vincular tarea a la fase
				add_task=Activity.objects.get(
					id=form_header['id_form_create'][0])
				add_task.task.add(task_save.pk)


				mensaje = 'La tarea se ha registrado correctamente'
				error = 'Sin errores'
				response = JsonResponse({'mensaje':mensaje,'error':error})
				response.status_code = 201
				return response

			#De lo contratio que muestre error
			else:
				#f'{self.model.__name__} obtienen el nombre del modelo
				mensaje = f'{self.model.__name__} no se ha podido registrar!'
				error = form.errors #DICCIONARIO CON LOS ERRORES
				response = JsonResponse({'mensaje': mensaje, 'error': error})
				response.status_code = 400 #PETICIÓN NO VALIDA POR EL CLIENTE
				return response
		else:
			return redirect(str(self.success_url))


class EditTaskActivity(EditTask):
	model = Task
	form_class = TaskUpdateForm
	template_name = 'task/activity/update_task.html'
	success_url = reverse_lazy('activity:list_task')


class DeleteTaskActivity(DeleteTask):
	model = Task
	template_name = 'task/activity/delete_task.html'
	permission_required = 'idea.view_dashboard'
	success_url = reverse_lazy('activity:list_task')
	raise_exception = True 

	