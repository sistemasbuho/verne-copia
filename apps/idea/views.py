import os
from django.contrib.auth.decorators import login_required,permission_required
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.views.generic import ListView , CreateView,  View, UpdateView
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect,JsonResponse
from django.urls import reverse,reverse_lazy
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .filters import IdeaFilter
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import F,Q
from django.db.models.functions.comparison import NullIf
from django.utils.timezone import now
from django.template.loader import get_template
from weasyprint import CSS, HTML
from datetime import datetime, timedelta,date
import json
from time import time
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.postgres.aggregates import ArrayAgg
from django.conf import settings
from .models import *
from .models import Idea,QuestionPhase,Phase_Date, Objective,Phase
from .forms import *
from apps.meeting.models import Meeting
from apps.activity.models import Activity
from django.contrib.auth.models import User
from apps.prize.models import Action,UserLeguas
from django.core.files.storage import FileSystemStorage

import datetime

fecha_actual = datetime.date.today()
fecha_formateada = fecha_actual.strftime('%d/%m/%Y')


# -----------START CLASES----------------------------------------------------------		

# Clase privada de la que heredan todas las vistas-----------------------------------		
class _FormValid(PermissionRequiredMixin):
	model = Idea
	permission_required = 'idea.add_idea'
	form_class = FormIdeaRegister
	template_name = 'idea/register.html'
	success_url = reverse_lazy('dashboard')
	success_message = 'Se ha creado con éxito'
	error_message = 'No se guardo con exito.'

	def form_valid(self, form):
		messages.success(self.request, self.success_message, extra_tags='God Job')
		return super().form_valid(form)

	def form_invalid(self, form):
		lista = ""
		for error in form.errors:
			lista+=str(error)

		#https://stackoverflow.com/questions/43588876/how-can-i-add-additional-data-to-django-messages
		messages.error(self.request, '%s debido a un error en el campo de: %s' % (self.error_message, lista), extra_tags='Error')
		return redirect(str(self.success_url))


	#Validación que limpia el los input de un espacio inicial y final con strip al guardar
	#https://www.peterbe.com/plog/automatically-strip-whitespace-in-django-forms
	def clean(self):
		for field in self.cleaned_data:
			if isinstance(self.cleaned_data[field], basestring):
				self.cleaned_data[field] = self.cleaned_data[field].strip()
		return self.cleaned_data


# Registro de Ideas----------------------------------------------------------		
class registerIdea(_FormValid,CreateView):
	model = Idea
	permission_required = 'idea.add_idea'
	form_class = FormIdeaRegister
	template_name = 'idea/register.html'
	success_url = reverse_lazy('dashboard')
	success_message = '¡La idea fue creada correctamente!'
	error_message = 'No se guardo con exito.'

	#n+1 solucionado
	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST) #cargo los datos del formulario
		form_header = dict(request.POST.lists())
		
		if 'collaborator' in form_header:
			collaborator_query = User.objects.filter(pk__in=form_header['collaborator'])  #[1,2,3]
			form.fields['collaborator'].queryset = collaborator_query

		phase_idea_query = Phase.objects.filter(pk=1)#__in=form_header['current_phase'])
		form.fields['id_phase'].queryset =phase_idea_query
		email_list = collaborator_query.values('email')
		lista_nueva = []

		for lista in email_list:
			lista_nueva.append(lista['email'])	
		
		host_email = [settings.EMAIL_HOST_USER]
		lista_nueva.extend(host_email)
		 
		if form.is_valid():
			guardado = form.save()

			info_guardado = Idea.objects.get(id=guardado.pk)

			user = request.user
			if Idea.objects.filter(collaborator=user.id).count() == 1:
				leguas, _ = UserLeguas.objects.get_or_create(id_user=user.id,category="1")
				leguas.quantity=leguas.quantity+50
				leguas.save()
			try:
				# Para el reenvio de email	
				body = render_to_string(
						'emails/idea_recibida.html', {
							'title': info_guardado.title,
							'fecha': info_guardado.creation_date,
							'autor': lista_nueva,
						},
					)
				email_message = EmailMessage(
				subject='Tu idea ha sido registrada en sistemas',
				body=body,
				from_email=host_email,
				to=lista_nueva,
				)
				email_message.content_subtype = 'html'
				email_message.send()
			except ObjectDoesNotExist as e:
					error = e

			return self.form_valid(form)

		#De lo contrario que muestre error
		else:
			self.form_invalid(form)
		return redirect(str(self.success_url))


# Cambio de fases----------------------------------------------------------		
class changePhase(PermissionRequiredMixin,View):
	model = Phase_Date
	permission_required = 'idea.view_dashboard'
	template_name = 'idea/change_phase.html'
	success_message = '¡La idea fue cambiada de fase correctamente!'
	error_message = 'No se actualizó la fase'

	#n+1 solucionado
	def get_queryset(self):
		queryset = self.model.objects.select_related('id_phase','id_idea').filter(
			id_idea_id=self.kwargs.get("pk",None)).values('id_phase_id').last()
		return queryset 

	def get_context_data(self,**kwargs):
		contexto = {}
		#contexto = super().get_context_data(**kwargs)
		consulta = self.get_queryset() #retornar elementos de una función por tupla (https://www.geeksforgeeks.org/g-fact-41-multiple-return-values-in-python/)
		contexto['consulta'] = consulta['id_phase_id']
		contexto['pk'] = self.kwargs.get("pk",None)
		return contexto

	def get(self, request, *args, **kwargs):
		return render(self.request,self.template_name,self.get_context_data())

	def post(self, request, *args, **kwargs):
		context_consulta = self.get_context_data()  #trae el contexto  {'consulta': 5, 'pk': 1}
		consulta = context_consulta.get('consulta') #5
		

		if (consulta >= 1 and consulta <= 4):
			sum_phase=consulta+1

			#Actualiza la idea con la fase actual
			Idea.objects.all().filter(id=self.kwargs.get("pk",None)).update(current_phase=sum_phase)
			#Crear el registro phase date
			self.model.objects.create(id_idea_id=self.kwargs['pk'],id_phase_id=sum_phase)
			#Acyualizamos el update de la fase anterior
			self.model.objects.filter(id_idea_id=self.kwargs['pk'],id_phase_id=consulta).update(phase_date_previous=now())

			try:
				info_guardado = Idea.objects.filter(id=self.kwargs.get("pk",None)).first()
				lista_nueva = []
				host_email = [settings.EMAIL_HOST_USER]

				emails_colaboradores = list(info_guardado.collaborator.values_list('email', flat=True))

				body = render_to_string(
						'emails/cambio_fase.html', {
							'title': info_guardado.title,
							'fecha': info_guardado.creation_date,
							'fasenew': Phase.objects.filter(id=info_guardado.current_phase).first().name,
						},
					)
				email_message = EmailMessage(
				subject='Tu idea ha cambiado de fase',
				body=body,
				from_email=host_email,
				to=emails_colaboradores,
				)
				email_message.content_subtype = 'html'
				email_message.send()

			except ObjectDoesNotExist as e:
					error = e

			# return self.form_valid(form)
			messages.success(self.request, self.success_message, extra_tags='God Job') #imprime el mensaje de aprobado
		else:
			messages.error(self.request, self.error_message, extra_tags='Error') #imprime el mensaje de aprobado

		return HttpResponseRedirect(reverse('idea:general_dashboard'))


# Ver listado por fases----------------------------------------------------------		
class watchIdeaPhase(PermissionRequiredMixin,ListView):
	model = Idea
	template_name = 'idea/visualize_phase.html'
	permission_required = 'idea.add_idea'
	
	def get_queryset(self, **kwargs):
		qs = self.model.objects.filter(current_phase=self.kwargs['fase']).prefetch_related("collaborator")
		product_filtered_list = IdeaFilter(self.request.GET, queryset=qs)
		return product_filtered_list.qs,product_filtered_list, 

	def get_context_data(self, **kwargs):
		context={} 
		object_idea,filter_idea= self.get_queryset() 
		context['object_list']  = object_idea
		context['filter_idea'] 	= filter_idea
		context['phases'] = Phase.objects.all()
		return context

	def get(self,request,*args,**kwargs):
		return render(request,self.template_name,self.get_context_data())


# Visualizar Ideas en Stand By------------------------------------------------------------------------------
class IdeaBank(PermissionRequiredMixin,View):  

	template_name = 'idea/bank_idea.html'
	permission_required = 'idea.add_idea'
	form_class = DashboardFormBanco
  
	def get_context_data(self,**kwargs):
		contexto = {}
		contexto["phases"] = Phase.objects.filter(id__in=[5,6]).order_by('id')
		contexto["form"] = self.form_class(self.request.GET)
		return contexto

	def get(self, request, *args, **kwargs):

		return render(self.request,self.template_name,self.get_context_data())

	def clean(self):
		for field in self.cleaned_data:
			print('field', field)
			if isinstance(self.cleaned_data[field], basestring):
				self.cleaned_data[field] = self.cleaned_data[field].strip()
		return self.cleaned_data


#Generador de PDF --------------------------------
class IdeaGeneratorPdf(View,PermissionRequiredMixin):
	permission_required = 'idea.add_idea'
	def get(self, request, *args, **kwargs):
		template=get_template("prints/idea_ticket.html")
		idea= Idea.objects.filter(id=kwargs['pk'])
		meeting= Meeting.objects.filter(id_idea=kwargs['pk'])
		activity = Activity.objects.filter(id_idea=kwargs['pk'])
		phase = Phase_Date.objects.filter(id_idea=kwargs['pk'])
		context = {"id":kwargs['pk'],
			"ideas": idea,
			"meetings":meeting,
			"activity":activity,
			"phases":phase
		}

		html = template.render(context)
		css_url = os.path.join(settings.BASE_DIR, 'static/plugins/tempusdominus-bootstrap-4/css/tempusdominus-bootstrap-4.min.css')
		pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
		response = HttpResponse(pdf, content_type='application/pdf')
		file_name = 'Idea '+str(kwargs['pk'])+'.pdf' # Agrega fecha y hora al nombre del archivo
		response['Content-Disposition'] = 'attachment; filename=%s' % file_name
		# response.write(output.getvalue())	 # Al configurar el tipo de HttpResponse, si da un valor, no es necesario que escriba esta oración
		return response
	
 
# Visualizar Portafolio------------------------------------------------------------------------------
class watchIdea(PermissionRequiredMixin,View):
	model = Idea
	permission_required = 'idea.add_idea'
	form_class = FiltrosIdea
	template_name = 'idea/visualize.html'

	def get_queryset(self):
		order_by = f"{self.request.GET.get('order_by')}"

		if self.request.GET.get('asc_desc') == 'desc':
			order_by = f'-{order_by}'

		query = Q()
		
		# TODO: implementar unaccent
  
		if self.request.GET.get('filtro'):
			query.add(Q(title__icontains=self.request.GET.get('filtro')), Q.AND)
			#query.add(Q(title__unaccent__icontains=self.request.GET.get('filtro')), Q.AND)
		
		if self.request.GET.get('prioridad_get_ajax'):
			query.add(Q(priority=self.request.GET.get('prioridad_get_ajax')), Q.AND)

		if self.request.GET.get('innovation_type_get_ajax'):
			query.add(Q(innovation_type=self.request.GET.get('innovation_type_get_ajax')), Q.AND)

		if self.request.GET.get('innovation_estrategia_get_ajax'):
			query.add(Q(innovation_estrategia=self.request.GET.get('innovation_estrategia_get_ajax')), Q.AND)

		if self.request.GET.get('is_active_get_ajax'):
			query.add(Q(is_active=self.request.GET.get('is_active_get_ajax')), Q.AND)

		if self.request.GET.get('is_fastrack_get_ajax'):
			query.add(Q(is_fastrack=self.request.GET.get('is_fastrack_get_ajax')), Q.AND)

		if self.request.GET.getlist('collaborator_get_ajax[]'):
			query.add(Q(collaborator__pk__in=self.request.GET.getlist('collaborator_get_ajax[]')), Q.AND)

		if self.request.GET.get('rango_fecha_creacion_get_ajax'):
			try:
				rango_creacion = self.request.GET.get('rango_fecha_creacion_get_ajax').split(' - ')
				fecha_inicial = datetime.strptime(rango_creacion[0], '%Y-%m-%d')
				fecha_final = datetime.strptime(rango_creacion[1], '%Y-%m-%d')

				query.add(Q(creation_date__range=[fecha_inicial,fecha_final]), Q.AND)
			except Exception as error:
				print("error: ",error)
				
		#if self.request.GET.getlist('frente')[0] != '':
		#	print("self.request.GET.getlist('frente')",self.request.GET.getlist('frente'))
		#	query.add(Q(frente_id=int(self.request.GET.getlist('frente')[0])), Q.AND)


		queryset = self.model.objects.prefetch_related('collaborator').filter(query).values(
			'id', 
			'creation_date', 
			'title',
			'priority',
			#'',#Autor
			'innovation_type',
			'innovation_estrategia',
			'is_active',	
			'is_fastrack',
			'current_phase',
		).order_by(order_by).annotate(collaborator_list=ArrayAgg('collaborator__email')) 
		
  		# Apoyo para usar ArrayAgg
    	# https://docs.djangoproject.com/en/2.2/ref/contrib/postgres/aggregates/
    	# https://stackoverflow.com/questions/43203014/django-queryset-annotate-field-to-be-a-list-queryset

		return queryset

	def get_context_data(self,**kwargs):
		contexto = {}
		contexto['form'] = self.form_class(self.request.GET)  #importante para que al recarga complete el formulario
		contexto['verbose_name_model'] = self.model._meta.verbose_name_plural
		return contexto

	#def get(self, request, parametro_extra, *args, **kwargs):
	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			"""
				Variable capturadas por GET que ofrece el propio serverSide
			"""

			inicio = int(request.GET.get('inicio'))
			fin = int(request.GET.get('limite'))

			# Variable para inciar el tiempo_ejecución
			tiempo_inicial = time()
			
			data_query = self.get_queryset()

			list_data = []

			for indice, valor in enumerate(data_query[inicio:inicio+fin],inicio):
				#valor['num'] = indice+1  #creamos un columna con un zndice para mostrar en el datatable

				#parseamos los campos que sean de tipo DateTimeField
				#if 'creation_date' in valor:
				#	print("creation_date err ",valor['creation_date'])
				#	valor['creation_date'] = ConverterDateToJson(valor['creation_date'])
				
				list_data.append(valor)
						
			tiempo_final = time() - tiempo_inicial
			data = {
				'length': data_query.count(),
				'objects': list_data
			}

			return HttpResponse(json.dumps(data,cls=DjangoJSONEncoder),content_type='application/json')
		
		else:
			return render(self.request,self.template_name,self.get_context_data())


# Vista de dashboard  --------------------------------------------------------------------------------------------------
class visualizeDashboardAjax(PermissionRequiredMixin,View):
	permission_required = 'idea.add_idea'
	form_class = DashboardForm
	template_name = 'idea/dashboard_ajax.html'
	
	def get_context_data(self,**kwargs):
		contexto = {}
		contexto["phases"] = Phase.objects.all()
		contexto["form"] = self.form_class(self.request.GET)
		return contexto

	def get(self, request, *args, **kwargs):
		return render(self.request,self.template_name,self.get_context_data())

	def clean(self):
		for field in self.cleaned_data:
			if isinstance(self.cleaned_data[field], basestring):
				self.cleaned_data[field] = self.cleaned_data[field].strip()
		return self.cleaned_data


# Vista de dashboard Detalles --------------------------------------------------------------------------------------------------
class EncabezadoDetalleNosotrosJsonListView(PermissionRequiredMixin,View):
	permission_required = 'idea.add_idea'

	def get(self, *args, **kwargs):

		query = Q()
		if ( self.request.GET.get('activado') == "false"):
			query.add(Q(is_active=False), Q.AND)
		else:
			query.add(Q(is_active=True), Q.AND)
			
		query.add(Q(current_phase=kwargs.get('fase')), Q.AND)

		#filtro por titulo
		if self.request.GET.get('titulo_nombre'):
			query.add(Q(title__icontains=self.request.GET.get('titulo_nombre')), Q.AND)

		#filtro por id_idea
		id_idea_nombre = self.request.GET.get('id_idea_nombre') # '["294","295"]' str
		id_idea_nombre = json.loads(id_idea_nombre) #['294', '295', '297'] list
		
		if id_idea_nombre:
			query.add(Q(id__in=id_idea_nombre), Q.AND)
   
		#daterange
		page = self.request.GET.get('daterange')

		print('frente', self.request.GET.getlist('frente'))

		if self.request.GET.get('daterange'):
			rango_creacion = page.split(' - ')
			fecha_inicial = datetime.strptime(rango_creacion[0], '%Y-%m-%d') #2022-01-20 00:00:00
			fecha_final = datetime.strptime(rango_creacion[1], '%Y-%m-%d')
			query.add(Q(creation_date__range=[fecha_inicial,fecha_final]), Q.AND)
		
		if self.request.GET.get('prioridad'):
			query.add(Q(priority=self.request.GET.get('prioridad')), Q.AND)

		if self.request.GET.get('tipo_innovacion'):
			query.add(Q(innovation_type=self.request.GET.get('tipo_innovacion')), Q.AND)
		
		if self.request.GET.get('tipo_estrategia'):
			query.add(Q(innovation_estrategia=self.request.GET.get('tipo_estrategia')), Q.AND)
   
		if self.request.GET.getlist('asigned[]'):
			query.add(Q(asigned__pk__in=self.request.GET.getlist('asigned[]')), Q.AND)

		if self.request.GET.get('frente'):
			print("self.request.GET.getlist('frente')",self.request.GET.getlist('frente'))
			query.add(Q(frente_id=int(self.request.GET.getlist('frente')[0])), Q.AND)
		#elif():
		#else:
		#	print("self.request.GET.getlist('frente')",self.request.GET.getlist('frente'))
		#	query.add(Q(frente_id__isnull=False), Q.AND)

		consulta = Idea.objects.filter(query).values(
			'id',
			'title',
			'current_phase',
			'creation_date',
			'asigned',
			'asigned__profile__avatar',
			'asigned__email',
		).order_by('id')

		print('consulta',consulta)

		upper = kwargs.get('num_posts')
		lower = upper - 4
		
		posts = []
		posts2 = []
		
		for dato in consulta[lower:upper]:
			print("wargs.get('fase')",kwargs.get('fase'))
			print("dato['id'],",dato['id'])
			#throught = Phase_Date.objects.filter(id_idea_id=dato['id'], id_phase_id=int(kwargs.get('fase'))).values('phase_date_previous','phase_date').order_by('-id')[0]
			throught = Phase_Date.objects.filter(id_idea=dato['id'], id_phase_id=kwargs.get('fase')).values('phase_date_previous','phase_date').order_by('-id')[0]

			phase_date = throught['phase_date']
			phase_date_previous = throught['phase_date_previous']

			if phase_date is None:
				phase_date = date.today()

			if phase_date_previous is None:
				phase_date_previous = date.today()
			
			#print("phase_date ",phase_date)
			#print("phase_date_previous ",phase_date_previous)

			#https://www.programiz.com/python-programming/datetime/current-datetime
			#dar formato a las dos variables para que la operación se ejecute

			numero_dias= (phase_date_previous-phase_date ) / timedelta(days=1)
			
			nombre_fase = Phase.objects.get(id=kwargs.get('fase'))
			posts.append({
				'id': dato['id'],
				'title': dato['title'],
				'phase_date_throught': numero_dias,
				'asigned__profile__avatar': dato['asigned__profile__avatar'],
				'asigned__email':dato['asigned__email'],
			})
		
			posts2.append({
				'id': dato['id'],
				'title': dato['title'],
				'phase_date_throught': numero_dias,
				'asigned__profile__avatar': dato['asigned__profile__avatar'],
				'asigned__email':dato['asigned__email'],
				'name_phase': nombre_fase.name,
				'id_phase':kwargs.get('fase'), 
			})


		#print('Posts2', posts2)
		#lista_miembros = Idea.objects.filter(current_phase=fase).values('id','description','title','owner_idea').order_by('id')
		#posts = list(consulta[lower:upper])
		posts_size = len(consulta)
		max_size = True if upper >= posts_size else False
		return JsonResponse({'data': posts, 'max': max_size, 'numero_ideas': posts_size}, safe=False)

# -----------END CLASES----------------------------------------------------------		




# -----------START Ajax para formularios----------------------------------------------------------		

class _SearchAjax(PermissionRequiredMixin,CreateView):
	model = User
	permission_required = 'idea.add_idea'
	
	def get(self, request, *args, **kwargs):
		data = request.GET.dict()
		query = self.model.objects.filter(email__icontains=data['term'],is_active=True).values('id','email').order_by('email')[:100]
		data_dict_result= []

		for i in query:
			data_list= {
				'id' : i['id'],
				'name' : i['email']
			}
			data_dict_result.append(data_list)
		return  JsonResponse(data_dict_result, safe=False)


class SearchAjaxIdea(PermissionRequiredMixin,CreateView):
	model = Idea
	permission_required = 'idea.add_idea'
	
	def get(self, request, *args, **kwargs):
		data = request.GET.dict()
		query = self.model.objects.filter(title__icontains=data['term'],is_active=True).values('id','title')
		data_dict_result= []

		for i in query:
			data_list= {
				'id' : i['id'],
				'name' : i['title']
			}
			data_dict_result.append(data_list)
		return  JsonResponse(data_dict_result, safe=False)


class SearchUserAjax(_SearchAjax):
	pass


class SearchColaborator(PermissionRequiredMixin,View):
	model = User
	permission_required = 'idea.view_idea'

	def get(self, request, *args, **kwargs):
		data_dict_result= []
		data = request.GET.dict()
		
		#TODO: Instalar en la base de datos el unaccent
  
		#al buscar listara los primero 20 registros que coincidan
		if 'term' in data:
			print("data['term'] ",data['term'])
			#query = self.model.objects.filter(email__unaccent__icontains=data['term']).values('id','email').order_by('email')[:10]
			query = self.model.objects.filter(email__icontains=data['term']).values('id','email').order_by('email')[:20]
			#print("if ",query.count())
		#Al cargar mostrara los primeros 40 usuarios
		else:
			query = self.model.objects.values('id','email').order_by('email')[:40]
			#print("else ",query.count())

		for i in query:
			data_list= {
				'id' : i['id'],
				'name' : i['email']
			}
			data_dict_result.append(data_list)
		return  JsonResponse(data_dict_result, safe=False)
	
class SearchSubregion(PermissionRequiredMixin,View):
	model = Area
	permission_required = 'idea.view_idea'

	def get(self, request, *args, **kwargs):
		data_dict_result= []
		data = request.GET.dict()
		
		#TODO: Instalar en la base de datos el unaccent
  
		#al buscar listara los primero 20 registros que coincidan
		if 'term' in data:
			print("data['term'] ",data['term'])
			#query = self.model.objects.filter(email__unaccent__icontains=data['term']).values('id','email').order_by('email')[:10]
			query = self.model.objects.filter(nombre__icontains=data['term']).values('id','nombre').order_by('nombre')[:20]
			#print("if ",query.count())
		#Al cargar mostrara los primeros 40 usuarios
		else:
			query = self.model.objects.values('id','nombre').order_by('nombre')[:40]
			#print("else ",query.count())

		for i in query:
			data_list= {
				'id' : i['id'],
				'name' : i['nombre']
			}
			data_dict_result.append(data_list)
		return  JsonResponse(data_dict_result, safe=False)


class SearchAjaxIdIdeaFilters(PermissionRequiredMixin,CreateView):
	model = Idea
	permission_required = 'idea.add_idea'
	
	def get(self, request, *args, **kwargs):
		data = request.GET.dict()
		query = self.model.objects.filter(id__icontains=data['term'],is_active=True).values('id','title')
		data_dict_result= []

		for i in query:
			data_list= {
				'id' : i['id'],
			}
			data_dict_result.append(data_list)
		return  JsonResponse(data_dict_result, safe=False)
	
class SearchAjaxIdFrenteFilters(PermissionRequiredMixin,View):
	model = Frente
	permission_required = 'idea.view_idea'

	def get(self, request, *args, **kwargs):
		data_dict_result= []
		data = request.GET.dict()
		
		#TODO: Instalar en la base de datos el unaccent
  
		#al buscar listara los primero 20 registros que coincidan
		if 'term' in data:
			print("data['term'] ",data['term'])
			#query = self.model.objects.filter(email__unaccent__icontains=data['term']).values('id','email').order_by('email')[:10]
			query = self.model.objects.filter(nombre__icontains=data['term']).values('id','nombre').order_by('nombre')[:20]
			#print("if ",query.count())
		#Al cargar mostrara los primeros 40 usuarios
		else:
			query = self.model.objects.values('id','nombre').order_by('nombre')[:40]
			#print("else ",query.count())

		for i in query:
			data_list= {
				'id' : i['id'],
				'name' : i['nombre']
			}
			data_dict_result.append(data_list)
		return  JsonResponse(data_dict_result, safe=False)




class ExternalIdeaList (PermissionRequiredMixin, ListView):
	model = ExternalIdea
	template_name = 'idea/external_idea.html'
	context_object_name = 'external_idea'
	permission_required = 'idea.view_dashboard'
	queryset: ExternalIdea.objects.all
	ordering = '-id'


# -----------END Ajax para formularios----------------------------------------------------------		



# -----------START FUNCIONES ----------------------------------------------------------		

# Subir Archivo a cada fase---------------------------------------------------------------------------
@login_required()
@permission_required('idea.view_dashboard', raise_exception=True)

def BasicUploadView(request,pk):
	phase=Phase.objects.all()
	consulta = list(Phase_Date.objects.filter(id_idea_id=pk).values_list('id_phase_id', flat=True))
	form = FileForm()
	if request.method == 'POST':
		form = FileForm(request.POST, request.FILES)  
		if form.is_valid():
			if 'document' in request.FILES:
				query=Phase_Date.objects.filter(id_idea_id=pk,id_phase_id= request.POST.get('fase'))
				for obj in query:
					obj.document=request.FILES['document']
					obj.save()
			else: 
				pass
	else:
		form = FileForm()
	return render(request, 'idea/upload.html', {'form': form, 'consulta':consulta, 'pk':pk,'phases':phase})


# Enviar Idea  a Stand By---------------------------------------------------------------------------
@login_required()
@permission_required('idea.view_dashboard', raise_exception=True)

def inactive_idea (request,pk):
	consulta = Phase_Date.objects.filter(id_idea_id=pk).values('id_phase_id').last()
	consulta= consulta['id_phase_id']

	print('request.method',request.method)
	if request.method == 'GET':
		return render(request,'idea/inactive.html',{'consulta':consulta, 'pk':pk})
	else:   		
		Idea.objects.filter(id=pk).update(is_active=False, current_phase=6)
		Phase_Date.objects.create(id_idea_id=pk,id_phase_id=6,phase_date_previous=now())

		return HttpResponseRedirect(reverse('idea:update',args=[pk]))


# Reactivar Idea ----------------------------------------------------------------------------------------

@login_required()
@permission_required('idea.view_dashboard', raise_exception=True)

def reactive_idea (request,pk):
	consulta = list(Phase_Date.objects.filter(id_idea_id=pk).values_list('id_phase_id', flat=True))
	print('consulta',consulta)
	print('consulta[-1]',consulta[-1])
	previous_phase=consulta[-1]
	print('previous_phase',previous_phase)
	if request.method == 'GET':
		return render(request,'idea/reactive.html',{'previous_phase':previous_phase, 'pk':pk})
	else: 
		Idea.objects.filter(id=pk).update(is_active=True, current_phase=previous_phase)
		Phase_Date.objects.create(id_idea_id=pk,id_phase_id=previous_phase,phase_date_previous=now())
		return HttpResponseRedirect(reverse('idea:update',args=[pk]))


# Fastrack Idea ----------------------------------------------------------------------------------------

@login_required()
@permission_required('idea.view_dashboard', raise_exception=True)

def fastrackIdea(request,pk):	
	consulta = Phase_Date.objects.filter(id_idea_id=pk).values('id_phase_id').last()
	consulta= consulta['id_phase_id']
	if request.method == 'GET':
		return render(request,'idea/fastrack.html',{'pk':pk, 'consulta':consulta})
	else: 
		Idea.objects.filter(id=pk).update(current_phase=4)
		Phase_Date.objects.create(id_idea_id=pk,id_phase_id=4,phase_date_previous=now())
		return HttpResponseRedirect(reverse('idea:update',args=[pk]))


# Editar Idea-----------------------------------------------------------------------------------------

@login_required()
@permission_required('idea.view_dashboard', raise_exception=True)

class idea_de_prueba(PermissionRequiredMixin, UpdateView):
	model = Idea
	permission_required = 'idea.view_dashboard'
	form_class = IdeaUpdateForm
	template_name = 'idea/update.html'


	def get_context_data(self, *args, **kwargs):
		context = super(idea_de_prueba,self).get_context_data(*args, **kwargs)
		id=self.object.id
		context['error'] =0
		context ['ideas'] = Idea.objects.filter(id=id).prefetch_related("collaborator")
		context['phase_doc']= Phase_Date.objects.filter(id_idea=id).values('id_phase','id_phase__name')
		context['tasks']= TaskByIdea.objects.all()
		

		return context

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

@login_required()
@permission_required('idea.view_dashboard', raise_exception=True)

def UpdateIdea(request, id):

	print(request.POST)
	form = None
	error = None
	try:
		idea = Idea.objects.get(id=id)
		if request.method == 'GET':
			form = IdeaUpdateForm(instance=idea)
			form.fields['collaborator'].queryset = User.objects.filter(pk__in=form.instance.collaborator.all())
			form.fields['id_merge'].queryset = Idea.objects.filter(pk__in=form.instance.id_merge.all())
			#form.fields['region'].queryset = Subregion.objects.filter(pk__in=form.instance.region.all())

		else:
			form = IdeaUpdateForm(request.POST, request.FILES, instance=idea)
			form_header = dict(request.POST.lists())

			print('form_header',form_header)
			print('form',request.FILES)
			
			if 'collaborator' in form_header:
				collaborator_query = User.objects.filter(pk__in=form_header['collaborator'])  #[1,2,3]
				form.fields['collaborator'].queryset = collaborator_query

			#if 'region' in form_header:
			#	region_query = Subregion.objects.filter(pk__in=form_header['region'])  #[1,2,3]
			#	form.fields['region'].queryset = region_query

			if 'id_merge' in form_header:
				merge_idea_query = Idea.objects.filter(pk__in=form_header['id_merge'])
				form.fields['id_merge'].queryset = merge_idea_query

			#if form_header['primer_documento'] != '':
			#	Idea.objects.filter(id=id).update(primer_documento='home/'+str(form_header['primer_documento'][0]))
			
			#if form_header['segundo_documento'] != '':
			#	Idea.objects.filter(id=id).update(tercer_documento='home/'+str(form_header['segundo_documento'][0]))

			
			#if form_header['tercer_documento'] != '':
			#	Idea.objects.filter(id=id).update(tercer_documento='home/'+str(form_header['tercer_documento'][0]))




			if form.is_valid():
				
				form.save()
			
			print('form.is_valid()',form.is_valid())
			#Para el indicador de leguas
			score_action= Action.objects.filter(id_idea=id).values("score")
			score_activity=Activity.objects.filter(id_idea=id).values("score")
			score=0
   
			# Pendiente a remover esta linea una vez se ejecute
			Activity.objects.filter(score=None).update(score=0)

			for i in score_activity:
				score= score+i['score']    

			for c in score_action:
				score= score+c['score']  
			

			query_price=PriceScore.objects.values('price')

			if query_price is None:
				query_price=0
			else:
				#price= query_price[0]['price']*score
				price=0

			Idea.objects.filter(id=id).update(
				score_idea=score,
				price_score=price, 
				total_investment=(F('price_score')+F('investment'))
				)

			Idea.objects.filter(id=id).update(roi=(F('gain') - F('total_investment'))/NullIf(F('total_investment'), 0))
			   
			return HttpResponseRedirect(reverse('idea:update',args=[id]))
	except ObjectDoesNotExist as e:
		error = e
		print('error',e)
		return render(request, '404.html', {'error':error})

	ideas = Idea.objects.filter(id=id).prefetch_related("collaborator")
	phase_doc= Phase_Date.objects.filter(id_idea=id).values('id_phase','id_phase__name')

	return render(request, 'idea/update.html', 
	{'form': form,'error': error,'ideas':ideas, 'phase_doc':phase_doc, 'tasks': TaskByIdea.objects.all()})




# Preguntas de validacion para fase 2 -----------------------------------------------------------------------------------
@login_required()
@permission_required('idea.view_dashboard', raise_exception=True)

def QuestionPain(request, pk):
	consulta = Phase_Date.objects.filter(id_idea_id=pk).values('id_phase_id').last()
	consulta= consulta['id_phase_id']
	questions = QuestionPhase.objects.values("id","name").order_by('name')
	form = UpdateQuestion(request.POST or None)
	get_data_user = request.POST.getlist("state")
	feedback = request.POST.getlist("feedback")
	list_questions = []
	for p in questions:
		#p es un diccionario y por esta razon se accede por el valor ['id']
		data_id = str((p['id']))
		list_questions.append(data_id)

	if (request.method == 'POST'):
		#Diferencia entre las preguntas de la BD y las seleccionadas por el usuario
		question_false=	list(set(list_questions).difference(get_data_user))
		#question_false ['1', '4', '2', '3']
		#Guardar las preguntas que están en False de la lista

		for i,c in enumerate(question_false):
			save_data=IdeaQuestionPhase(id_idea_id=pk,id_question_id=int(c))
			save_data.save()

		#Guarda las preguntas seleccionadas en True de la lista
		for i,t in enumerate(get_data_user):
			save_data=IdeaQuestionPhase(id_idea_id= pk,id_question_id=int(t))
			save_data.save()

		if question_false:		
			# Ingresa a fase 6 
			save_data=Phase_Date(id_idea_id=pk,id_phase_id=6,phase_date_previous=now())
			Idea.objects.filter(id=pk).update(is_active=False, current_phase=6, feedback=feedback)
			save_data.save()

		else:
			# Ingresa a fase 2
			Idea.objects.filter(id=pk).update(current_phase=2, feedback=feedback)
			#Consulta el ultimo registro de la tabla intermedia para traer la fecha inicial y posteriormente
			#guardarla en la misma tabla con un nuevo registro

			


			#Crear el registro			
			save_data=Phase_Date(id_idea_id=pk,id_phase_id=2)
			save_data.save()

			Phase_Date.objects.filter(id_idea_id=pk,id_phase_id=1).update(phase_date_previous=now())

		return HttpResponseRedirect(reverse('idea:update',args=[pk]))
	return render(request,'idea/question.html', {'form':form,'questions':questions,'consulta':consulta, 'pk': pk})



def ConverterDateToJson(value):
	if isinstance(value, datetime):
		#Limpia la fecha quitando la zona horaria, segundo y milisegundos
		#https://docs.python.org/3/library/datetime.html#datetime.datetime.replace
		value = str(value.replace(tzinfo=None,second=0, microsecond=0))
		print("value ",value)
		return value


@login_required()
@permission_required('idea.add_idea', raise_exception=True)
def visualizeDashboardUser(request):

	if Profile.objects.filter(user=request.user.id).exists():
		pass
	else:
		Profile.objects.filter(avatar__isnull=True).update_or_create(
 			user_id=request.user.id,
 			avatar = 'default-user.png',
 			biografy= "Por definir",)
    
	idea_query = Idea.objects.filter(collaborator = request.user.id).prefetch_related("collaborator")
	total_ideas = idea_query.filter(is_active=True).count()
	total_dead = idea_query.filter(is_active=False).count()


	return render(request,'idea/dashboard_user.html',{'total_ideas':total_ideas,'idea_query':idea_query,'total_dead':total_dead})
	
 
# Vista detalle de ideas --------------------------------------------------------------------------------------------------
@login_required()
@permission_required('idea.add_idea', raise_exception=True)

def detailsIdeaDashboard(request,id_idea):
	if request.method == 'GET':
		query=Idea.objects.filter(id=id_idea).prefetch_related("collaborator")
		meeting= Meeting.objects.filter(id_idea=id_idea).order_by('id')[:3]
		activity= Activity.objects.filter(id_idea=id_idea).order_by('id')[:3]
		document=Phase_Date.objects.filter(id_idea=id_idea)	
		phase= Phase.objects.all()
	else:
		pass
	return render(request,'idea/details_idea.html',{'query':query,'meeting':meeting, 'activity':activity, 'document':document, 'phases':phase})


# Editar Fase documentacion-----------------------------------------------------------------------------------------

@login_required()
@permission_required('idea.view_dashboard', raise_exception=True)

def PhaseDocumentation(request, id, fase):
	form = None
	error = None
	try:
		idea = Phase_Date.objects.get(id_idea=id, id_phase=fase)
		if request.method == 'GET':
			form = PhaseForm(instance=idea)
			
		else:
			form = PhaseForm(request.POST, instance=idea)
			if form.is_valid():	
				form.save()
				
			return HttpResponseRedirect(reverse('idea:update',args=[id]))
	except ObjectDoesNotExist as e:
		error = e
		return render(request, 'idea/no_phases.html', {'error':error})
	phase= Phase.objects.all()

	context={
		'form': form,
		'error': error,
		'phases':phase,
		'tasks': Task.objects.all(),
		'count': Task.objects.filter(complete=False).count(),
	}
	
	search_input = request.GET.get('search-area') or ''
	if search_input:
		context['tasks'] = context['tasks'].filter(
			title__contains=search_input)

	context['search_input'] = search_input

	return render(request, 'idea/phases.html', context)


# Detalles idea estado--------------------------------------------------------------------------
@login_required()
@permission_required('idea.view_dashboard', raise_exception=True)

def ExternalIdeaState (request,pk):
	query= ExternalIdea.objects.filter(pk=pk)
	questions = QuestionPhase.objects.values("id","name").order_by('name')
	return render(request,'idea/state_idea.html',{'pk':pk, 'query':query,'questions':questions})


# Aceptar  idea--------------------------------------------------------------------------

@login_required()
@permission_required('idea.view_dashboard', raise_exception=True)
def aceptar_idea_externa(request):

	lista_nueva = []

	host_email = [settings.EMAIL_HOST_USER]

	idea_externa_id = request.POST['idea_externa']
	feedback_text = request.POST['feedback']

	query= ExternalIdea.objects.filter(pk=idea_externa_id)

	for idea in query:
			print('idea',idea.gerencia_id)
			data= Idea.objects.create(
	
				title=idea.title,
				description=idea.description,
				solucion= idea.solucion,
				current_phase=1,
				conditions=True,
				idea_externa_id=idea_externa_id,
				proposito=idea.proposito,
				gerencia_id=idea.gerencia_id,
				subregion_id=idea.subregion_id,
				frente_id=idea.frente_id,
				dimension_id=idea.dimension_id,
				pilar_id=idea.pilar_id,
				documento=idea.documento,
				external_name= idea.external_name,
				external_email=idea.external_email,
				feedback=feedback_text,
				revision=idea.revision,
			)
			data.collaborator.add(1)
			#data.id_objective.add(1)
			data.id_phase.add(1)

			lista_nueva.append(idea.external_email)

			try:
				body = render_to_string(
						'emails/idea_aceptada.html', {
							'idea': idea.title,
							'autor': idea.external_name,
							'fecha': fecha_formateada,
							'feedback':feedback_text,
						},
					)
				email_message = EmailMessage(
						subject='¡Tu idea fue aceptada!',
						body=body,
						from_email=host_email,
						to=lista_nueva,
						)
				email_message.content_subtype = 'html'
				email_message.send()
			except ObjectDoesNotExist as e:
				error = e

	ExternalIdea.objects.filter(pk=idea_externa_id).update(state="Aprobado", feedback=feedback_text)

	
	
	print('Enviar a tareas')
	

	valido = True
	return HttpResponse(json.dumps({'valido': valido}), content_type='application/json')


@login_required()
@permission_required('idea.view_dashboard', raise_exception=True)

def ExternalIdeaStateAproved(request,pk):
	query= ExternalIdea.objects.filter(pk=pk)

	if request.method == 'GET':
		return render(request,'idea/state_idea.html')
	else:
		for idea in query:
			print('idea',idea.gerencia_id)
			data= Idea.objects.create(
				
				title=idea.title,
				description=idea.description,
				current_phase=1,
				conditions=True,
				idea_externa_id=pk,
				proposito=idea.proposito,
				gerencia_id=idea.gerencia_id,
				subregion_id=idea.subregion_id,
				frente_id=idea.frente_id,
				dimension_id=idea.dimension_id,
				pilar_id=idea.pilar_id,
				documento=idea.documento,
				external_name= idea.external_name,
				external_email=idea.external_email
			)
			data.collaborator.add(1)
			#data.id_objective.add(1)
			data.id_phase.add(1)

		ExternalIdea.objects.filter(pk=pk).update(state="Aprobado")
		return redirect('idea:external_idea')

# Solicitar mas información de la idea ---------------------------------------------------



# Rechazar  idea--------------------------------------------------------------------------

def rechazar_idea_externa(request):
	lista_nueva = []

	host_email = [settings.EMAIL_HOST_USER]

	idea_externa_id = request.POST['idea_externa']
	feedback_text = request.POST['feedback']
	ExternalIdea.objects.filter(pk=idea_externa_id).update(state="Rechazado", feedback=feedback_text)
	datos_idea_externa = ExternalIdea.objects.get(pk=idea_externa_id)
	print('Enviar a tareas')

	lista_nueva.append(datos_idea_externa.external_email)

	try:
		body = render_to_string(
						'emails/idea_rechazada.html', {
							'idea': datos_idea_externa.title,
							'autor': datos_idea_externa.external_name,
							'fecha': fecha_formateada,
							'feedback':feedback_text,
						},
					)
		email_message = EmailMessage(
						subject='Tenemos noticias sobre tu idea',
						body=body,
						from_email=host_email,
						to=lista_nueva,
						)
		email_message.content_subtype = 'html'
		email_message.send()
	except ObjectDoesNotExist as e:
		error = e

	valido = True
	return HttpResponse(json.dumps({'valido': valido}), content_type='application/json')



@login_required()
@permission_required('idea.view_dashboard', raise_exception=True)

def ExternalIdeaStateReached (request,pk):
	if request.method == 'GET':
		return render(request,'idea/state_idea.html')
	else:
		ExternalIdea.objects.filter(pk=pk).update(state="Rechazado")
		return redirect('idea:external_idea')


# Historial Actividades y Reuniones de la idea--------------------------------------------------------------------------

@login_required()
@permission_required('idea.view_dashboard', raise_exception=True)

def RecordIdea(request,id_idea):
	if request.method == 'GET':
		meeting= Meeting.objects.filter(id_idea=id_idea).order_by('id')[:3]
		activity= Activity.objects.filter(id_idea=id_idea).order_by('id')[:3]
		document=Phase_Date.objects.filter(id_idea=id_idea)	
		phase= Phase.objects.all()
  
	else:
		pass
	return render(request,'idea/record_history.html',{'id_idea':id_idea,'meeting':meeting, 'activity':activity, 'document':document, 'phases':phase})




@permission_required('idea.view_dashboard', raise_exception=True)
def revisar_idea_externa(request):

	lista_nueva = []

	host_email = [settings.EMAIL_HOST_USER]

	idea_externa_id = int(request.POST['idea_externa_id'])
	feedback_text = request.POST['feedback']

	query= ExternalIdea.objects.filter(pk=idea_externa_id)
	query.update(feedback=feedback_text)

	for idea in query:
			
			print(idea.external_email)
			lista_nueva.append(idea.external_email)
			try:
				body = render_to_string(
						'emails/revisar_idea.html', {
							'titulo': idea.title,
							'autor': idea.external_name,
							'problema': idea.description,
							'frente': idea.frente,
							'prorposito': idea.proposito,
							'dimension': idea.dimension,
							'pilar': idea.pilar,
							'feedback':idea.feedback,
							'link':"{% url 'idea:review' "+str(idea.id)+" %}",
							'id_idea':idea.id,
							
						},
					)
				email_message = EmailMessage(
						subject='¡Ayúdanos a completar tu idea!',
						body=body,
						from_email=host_email,
						to=lista_nueva,
						)
				email_message.content_subtype = 'html'
				email_message.send()
			except ObjectDoesNotExist as e:
				error = e
		

	#ExternalIdea.objects.filter(pk=idea_externa_id).update(state="Aprobado", feedback=feedback_text)
	ExternalIdea.objects.filter(pk=idea_externa_id).update(state="En revisión")

	
	
	print('Enviar a revisar')
	

	valido = True
	return HttpResponse(json.dumps({'valido': valido}), content_type='application/json')





def revisar_idea(request,id_idea):
	form = None
	error = None

	lista_nueva = []

	host_email = [settings.EMAIL_HOST_USER]


	idea_externa = ExternalIdea.objects.get(id=id_idea)

	if request.method == 'GET':
		form = ExternalIdeaRevisionForm(instance=idea_externa)
	
	else:
		form = ExternalIdeaRevisionForm(request.POST, instance=idea_externa)
		if form.is_valid():	
			form.save()
			lista_nueva.append(idea_externa.external_email)
			try:
				body = render_to_string(
						'emails/idea_revisada.html', {
							'idea': idea_externa.title,
							'autor': idea_externa.external_name,
							'link':"{% url 'idea:external_idea' %}"
						},
					)
				email_message = EmailMessage(
								subject='La idea '+idea_externa.title+' ha sido revisada',
								body=body,
								from_email=host_email,
								to=['sistemaslab@buho.media',],
								)
				email_message.content_subtype = 'html'
				email_message.send()
			except ObjectDoesNotExist as e:
				error = e
				

	context={
		'form': form,
		'titulo': idea_externa.title,
		'autor': idea_externa.external_name,
		'problema': idea_externa.description,
		'frente': idea_externa.frente,
		'prorposito': idea_externa.proposito,
		'dimension': idea_externa.dimension,
		'pilar': idea_externa.pilar,
		'feedback':idea_externa.feedback,
	}


	return render(request, 'idea/revision_idea.html', context)

	