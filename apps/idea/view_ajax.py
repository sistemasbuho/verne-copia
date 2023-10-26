from .models import Phase_Date, TaskByIdea
from .forms import *
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import View, UpdateView, CreateView, DeleteView
from django.db.models import Q
from time import time
from datetime import datetime
import json
from django.shortcuts import render, redirect,  HttpResponse
from django.db import connection
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.core.serializers.json import DjangoJSONEncoder
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist

def ConverterDateToJson(value):
	if isinstance(value, datetime):
		#Limpia la fecha quitando la zona horaria, segundo y milisegundos
		#https://docs.python.org/3/library/datetime.html#datetime.datetime.replace
		value = str(value.replace(tzinfo=None,second=0, microsecond=0))
		return value



# Para vista de Fase por Idea--------------------------------------------------------

class _ListarAjax(PermissionRequiredMixin,View):
	model = Task
	permission_required = 'idea.view_dashboard'
	# form_class = TaskCreateForm
	template_name = 'ideas/phases.html'
	

	def get_context_data(self,**kwargs):
		contexto = {}
		# contexto['form'] = self.form_class
		contexto['verbose_name_model'] = self.model._meta.verbose_name_plural

		return contexto

	def get(self, request, *args, **kwargs):
		from django.core import serializers
		if request.is_ajax():
			"""
				Variable capturadas por GET que ofrece el propio serverSide
			"""

			inicio = int(request.GET.get('inicio'))
			fin = int(request.GET.get('limite'))

			# Variable para inciar el tiempo de ejecución
			tiempo_inicial = time()
			
			data_query = self.get_queryset()

			list_data = []

			for indice, valor in enumerate(data_query[inicio:inicio+fin],inicio):
				#valor['num'] = indice+1  #creamos un columna con un zndice para mostrar en el datatable
				if 'created' in valor:
					valor['created'] = ConverterDateToJson(valor['created'])
				if 'updated_at' in valor:
					valor['updated_at'] = ConverterDateToJson(valor['updated_at'])
				if 'fecha' in valor:
					valor['fecha'] = ConverterDateToJson(valor['fecha'])
				
				list_data.append(valor)
						
			tiempo_final = time() - tiempo_inicial

			data = {
				'length': data_query.count(),
				'objects': list_data

			}

			return HttpResponse(json.dumps(data,cls=DjangoJSONEncoder),content_type='application/json')
		else:
			return render(self.request,self.template_name,self.get_context_data())


class ListTask(_ListarAjax): 
	model = Phase_Date
	permission_required = 'idea.view_dashboard'
	template_name = 'idea/phases.html'

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
		query.add(Q(id_idea__in=self.request.GET.get('idea_get_ajax')), Q.AND)
		query.add(Q(id_phase__in=self.request.GET.get('fase_get_ajax')), Q.AND)

		if self.request.GET.get('filtro'):
			query.add(Q(task__title__icontains=self.request.GET.get('filtro')), Q.AND)

		if self.request.GET.get('search_estado'):
			query.add(Q(task__complete=self.request.GET.get('search_estado')), Q.AND)

			
		queryset = self.model.objects.select_related('task__user').filter(
			query,task__id__isnull=False).values(
				'task__id',
				'task__user__email',
				'task__title',
				'task__description',
				'task__complete',
				'task__created'
			).order_by(order_by)
		
		return queryset


class CreateTask(PermissionRequiredMixin,CreateView):
	model = Task
	permission_required = 'idea.view_dashboard'
	form_class = TaskCreateForm
	template_name = 'task/phase/create_task.html'
	success_url = reverse_lazy('idea:tasks')
	success_message = 'La tarea fue creada con éxito'
	error_message = 'No se guardo con éxito.'
	
	def post(self, request, *args, **kwargs):

		lista_nueva = []

		host_email = [settings.EMAIL_HOST_USER]

		if request.is_ajax():
			form_header = dict(request.POST.lists())
			form = self.form_class(request.POST)

			#Foreing key
			if  'user' in form_header:
				user_query = User.objects.filter(pk__in=form_header['user'])
				form.fields['user'].queryset = user_query 
			else:
				form.fields['user'].queryset = User.objects.none()

			if form.is_valid():
				task_save= form.save()

				user_query = User.objects.get(pk__in=form_header['user'])
				print('user_query.username',user_query.email)

				idea_datos = Idea.objects.get(id=int(form_header['fase_form_create'][0]))
				#Vincular tarea a la fase
				add_task=Phase_Date.objects.get(
					id_idea= form_header['fase_form_create'][0],
					id_phase=form_header['id_form_create'][0])

				add_task.task.add(task_save.pk)

				lista_nueva.append(user_query.email)
				mensaje = 'La tarea se ha creado correctamente!'
				error = 'Sin errores'
				response = JsonResponse({'mensaje':mensaje,'error':error})
				response.status_code = 201

				try:
					body = render_to_string(
						'emails/nueva_tarea.html', {
							'idea': idea_datos.title,
							'tarea': task_save.title,
			
						},
						)
					email_message = EmailMessage(
							subject='¡Necesitamos tu apoyo!',
							body=body,
							from_email=host_email,
							to=lista_nueva,
							)
					email_message.content_subtype = 'html'
					email_message.send()
				except ObjectDoesNotExist as e:
					error = e

				return response

			#De lo contratio que muestre error
			else:
				#f' obtienen el nombre del modelo
				mensaje = f'No se ha podido registrar!'
				error = form.errors #DICCIONARIO CON LOS ERRORES
				response = JsonResponse({'mensaje': mensaje, 'error': error})
				response.status_code = 400 #PETICIÓN NO VALIDA POR EL CLIENTE
				return response
		else:
			return redirect(str(self.success_url))


class EditTask(PermissionRequiredMixin, UpdateView):
	model = Task
	permission_required = 'idea.view_dashboard'
	form_class = TaskUpdateForm
	template_name = 'task/phase/update_task.html'
	success_url = reverse_lazy('idea:tasks')
	success_message = 'Se ha editado con éxito'
	error_message = 'No se editado, valida los campos'

	def get_form(self,*args,**kwargs):
		instance = self.get_object() 
		form = self.form_class(instance=instance)

		#ForeingKey
		form.fields['user'].queryset = User.objects.filter(pk=instance.user.pk)

		#Manytomany
		#https://stackoverflow.com/questions/14920735/manyrelatedmanager-object-is-not-iterable/51501752
		#form.fields['colaborador'].queryset = User.objects.filter(pk__in=instance.colaborador.all())

		return form

	def post(self, request, *args, **kwargs):
		#Valido el formulario y si cumple que guarde y notifique con SweetAlert el guardado
		if request.is_ajax():

			#Llamo los datos recibidos en post y los convierto en lista para tenerlos datos del ajax de tags
			form_header = dict(request.POST.lists())
			form = self.form_class(request.POST, instance = self.get_object()) #get_object: hace una petición get para obtener el id para no usar una consulta

			if  'user' in form_header:
				user_query = User.objects.filter(pk__in=form_header['user'])# pk__in recibe una lista
				#cargo los datos del formulario
				form.fields['user'].queryset = user_query


			if form.is_valid():
				
				form.save()
				mensaje = f' {self.success_message}'
				response = JsonResponse({'mensaje':mensaje,'error':'No hay error!'})
				response.status_code = 201
				return response
	
			#De lo contratio que muestre error
			else:
				mensaje = f' {self.error_message}'
				error = form.errors
				response = JsonResponse({'mensaje': mensaje, 'error': error})
				response.status_code = 400
				return response
		else:
			return redirect(str(self.success_url))


class DeleteTask(PermissionRequiredMixin, DeleteView):
	model = Task
	template_name = 'task/phase/delete_task.html'
	permission_required = 'idea.view_dashboard'
	success_url = reverse_lazy('idea:tasks')
	raise_exception = True 

	def delete(self, request, pk, *args, **kwargs):
		if request.is_ajax():
			model = self.get_object()
			model.delete()
			mensaje = 'La tarea se ha eliminado correctamente'
			error = 'No hay error!'
			response = JsonResponse({'mensaje': mensaje, 'error': error})
			response.status_code = 201
			return response
		else:
			return redirect(str(self.success_url))



# Para vista de Idea--------------------------------------------------------

class ListTaskIdea(_ListarAjax): 
	model = Idea
	template_name = 'idea/update.html'
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
				
		return queryset


class CreateTaskIdea(PermissionRequiredMixin,CreateView):
	model = TaskByIdea
	permission_required = 'idea.view_dashboard'
	form_class = TaskCreateFormIdea
	template_name = 'task/idea/create_task.html'
	success_url = reverse_lazy('idea:list_task_idea')
	success_message = 'La tarea fue creada con éxito'
	error_message = 'No se guardó con éxito.'
	
	def post(self, request, *args, **kwargs):

		lista_nueva = []

		host_email = [settings.EMAIL_HOST_USER]

		if request.is_ajax():
			form_header = dict(request.POST.lists())
			form = self.form_class(request.POST)
	
			#Foreing key
			if  'user' in form_header:
				user_query = User.objects.filter(pk__in=form_header['user'])
				form.fields['user'].queryset = user_query 
			else:
				form.fields['user'].queryset = User.objects.none()

			if form.is_valid():
				task_save= form.save()
				
				#Vincular tarea a la fase
				add_task=Idea.objects.get(
					id=form_header['id_form_create'][0])
				add_task.task.add(task_save.pk)

				idea_datos = Idea.objects.get(id=int(form_header['id_form_create'][0]))
				user_querys = User.objects.get(pk__in=form_header['user'])

				lista_nueva.append(user_querys.email)
				try:
					body = render_to_string(
						'emails/nueva_tarea.html', {
							'idea': idea_datos.title,
							'tarea': task_save.title,
			
						},
						)
					email_message = EmailMessage(
							subject='¡Necesitamos tu apoyo!',
							body=body,
							from_email=host_email,
							to=lista_nueva,
							)
					email_message.content_subtype = 'html'
					email_message.send()
				except ObjectDoesNotExist as e:
					error = e

				mensaje = 'La tarea se ha registrado correctamente'
				error = 'Sin errores'
				response = JsonResponse({'mensaje':mensaje,'error':error})
				response.status_code = 201
				return response

			#De lo contratio que muestre error
			else:
				#f' obtienen el nombre del modelo
				mensaje = f' No se ha podido registrar!'
				error = form.errors #DICCIONARIO CON LOS ERRORES
				response = JsonResponse({'mensaje': mensaje, 'error': error})
				response.status_code = 400 #PETICIÓN NO VALIDA POR EL CLIENTE
				return response
		else:
			return redirect(str(self.success_url))


class EditTaskIdea(EditTask):
	model = TaskByIdea
	form_class = TaskUpdateFormIdea
	template_name = 'task/idea/update_task.html'
	success_url = reverse_lazy('idea:list_task_idea')
	permission_required = 'idea.view_dashboard'


class DeleteTaskIdea(DeleteTask):
	model = TaskByIdea
	template_name = 'task/idea/delete_task.html'
	permission_required = 'idea.view_dashboard'
	success_url = reverse_lazy('idea:list_task_idea')
	raise_exception = True 

	