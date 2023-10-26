from django.db.models.functions import Coalesce
from apps.idea.models import Idea, Phase_Date
from datetime import datetime
from django.db.models import Count,Sum
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import View
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.db.models import Q

from apps.prize.models import Action,UserLeguas
from .models import *
from time import time
from datetime import datetime
import json
from django.core.serializers.json import DjangoJSONEncoder


def ConverterDateToJson(value):
	if isinstance(value, datetime):
		#Limpia la fecha quitando la zona horaria, segundo y milisegundos
		#https://docs.python.org/3/library/datetime.html#datetime.datetime.replace
		value = str(value.replace(tzinfo=None,second=0, microsecond=0))
		return value

class ListTask(PermissionRequiredMixin,View):
	model = Action
	permission_required = 'idea.add_idea'
	template_name = "/indicators/indicators.html"
	# form_class = TaskCreateForm
	
	def get_context_data(self,**kwargs):
		contexto = {}
		# contexto['form'] = self.form_class
		contexto['verbose_name_model'] = self.model._meta.verbose_name_plural

		return contexto

	def get_queryset(self):

		query = Q()

		#select2
		usuario = self.request.GET.get('asignado_a')
		#inputs
		
		#select con data fija
		daterange = self.request.GET.get('fecha_rango')

		titulo_action = self.request.GET.get('filtro')

	
		if titulo_action:
			query.add(Q(name__icontains=titulo_action), Q.AND)
			#query.add(Q(name__unaccent__icontains=titulo_action), Q.AND)
		
		if usuario:
			query.add(Q(id_user=usuario), Q.AND)

		if  daterange:
			#print("daterange ",daterange)
			rango_creacion = daterange.split(' - ')
			fecha_inicial = datetime.strptime(rango_creacion[0], '%Y-%m-%d')
			fecha_final = datetime.strptime(rango_creacion[1], '%Y-%m-%d')
			query.add(Q(date__range=[fecha_inicial,fecha_final]), Q.AND)

		queryset = self.model.objects.select_related(
			'id_idea',
			'id_activity',
		).prefetch_related(
			'id_user',
		).filter(query).values(
			'id_user__email', #Usuario
			'name', #participación
			'date', #fecha
		)

		conteo = Action.objects.filter(query).aggregate(conteo_distintivo_usuario=Coalesce(Count('id_user', distinct=True),0),conteo_ideas=Coalesce(Count('pk'),0))
		total_usuarios = User.objects.filter(is_active=True).all()

		return queryset,conteo,total_usuarios.count()

	def get(self, request, *args, **kwargs):
		from django.core import serializers
		if request.is_ajax():
			"""
				Variable capturadas por GET que ofrece el propio serverSide
			"""

			inicio = int(request.GET.get('inicio')) #Es el primer dato que recibe del ajax 
			fin = int(request.GET.get('limite')) 

			# Variable para inciar el tiempo de ejecución
			tiempo_inicial = time()
			
			data_query,conteo,total_usuarios = self.get_queryset()

			list_data = []

			for indice, valor in enumerate(data_query[inicio:inicio+fin],inicio): #trae los primeros 10 registros 
				#valor['num'] = indice+1  #creamos un columna con un zndice para mostrar en el datatable
				if valor['id_user__email'] == '':

					valor['date'] = 'sin usuario'
				
				# if 'date' in valor:
				# 	valor['date'] = ConverterDateToJson(valor['date'])

				list_data.append(valor)
						
			import random
			number_random = random.randint(0,22)

			#group by
			#conteo = Action.objects.values('name').annotate(total_usuarios=Count('id_user'))
			#conteo = Action.objects.values('id_user').count('id_user', distinct=True)
			
			data = {
				'porcentaje': str(conteo['conteo_distintivo_usuario']) + " de " + str(total_usuarios),
				'participacion':  str(conteo['conteo_ideas']) + " de "+ str(conteo['conteo_distintivo_usuario'])+ " usuarios",
				'length': data_query.count(),
				'objects': list_data
			}

			return HttpResponse(json.dumps(data,cls=DjangoJSONEncoder),content_type='application/json')
		else:
			return render(self.request,self.template_name,self.get_context_data())


class SearchIdeaAjax(PermissionRequiredMixin,View):
	model = Idea
	permission_required = 'idea.add_idea'

	def get(self, request, *args, **kwargs):
		data_dict_result= []
		data = request.GET.dict()
		query = self.model.objects.filter(title__icontains=data['term']).values('id','title').order_by('title')[:50]

		for i in query:
			data_list= {
				'id' : i['id'],
				'name' : i['title']
			}
			data_dict_result.append(data_list)
		return  JsonResponse(data_dict_result, safe=False)


class IndicatorTable(PermissionRequiredMixin,View):
	model = Idea
	permission_required = 'idea.add_idea'
	template_name = "/indicators/indicators.html"
	# form_class = TaskCreateForm
	
	def get_context_data(self,**kwargs):
		contexto = {}
		# contexto['form'] = self.form_class
		contexto['verbose_name_model'] = self.model._meta.verbose_name_plural

		return contexto

	def get_queryset(self):

		query = Q()

		type_innovation = self.request.GET.getlist('tipo[]')
		priority = self.request.GET.getlist('prioridad[]')

	
		if type_innovation:
			query.add(Q(innovation_type__in=type_innovation), Q.AND)
		
		if priority:
			query.add(Q(priority__in=priority), Q.AND)

		# priority="ALTA", innovation_type="PRODUCTO",
		queryset = Idea.objects.filter(query,is_active=True).values('priority','innovation_type','current_phase').annotate(Conteo=Count('id')).order_by('priority')[:10]

		return queryset


	def get(self, request, *args, **kwargs):
		from django.core import serializers
		if request.is_ajax():
			"""
				Variable capturadas por GET que ofrece el propio serverSide
			"""

			inicio = int(request.GET.get('inicio')) #Es el primer dato que recibe del ajax 
			fin = int(request.GET.get('limite')) 

			# Variable para inciar el tiempo de ejecución
			tiempo_inicial = time()
			
			data_query = self.get_queryset()

			list_data = []

			for indice, valor in enumerate(data_query[inicio:inicio+fin],inicio): #trae los primeros 10 registros 
				#valor['num'] = indice+1  #creamos un columna con un zndice para mostrar en el datatable
				fase_actual = valor['current_phase']
		
				if(fase_actual==1):
					fase_actual = "Recepción"
				elif (fase_actual==2):
					fase_actual = "Nuevas"
				elif (fase_actual==3):
					fase_actual = "En desarrollo"
				elif (fase_actual==4):
					fase_actual = "Implementadas"
				elif (fase_actual==5):
					fase_actual = "Ideas Implementadas"
				elif (fase_actual==6):
					fase_actual = "Ideas en Stand By"
				else:
					fase_actual = "Sin Fase"

				print("fases ", fase_actual)

				list_data.append({
					'Prioridad':valor['priority'],
					'Tipo de Innovacion':valor['innovation_type'],
					'Conteo':valor['Conteo'],
					'Fase':fase_actual,

				})

			#print("data_list-----------",list_data)		
			import random
			number_random = random.randint(0,22)

			#group by
			#conteo = Action.objects.values('name').annotate(total_usuarios=Count('id_user'))
			#conteo = Action.objects.values('id_user').count('id_user', distinct=True)
			
			data = {
				
				'length': data_query.count(),
				'objects': list_data
			}

			return HttpResponse(json.dumps(data,cls=DjangoJSONEncoder),content_type='application/json')
		else:
			return render(self.request,self.template_name,self.get_context_data())


class GraficaMedidorAjax(PermissionRequiredMixin,View):	

	model = Phase_Date
	permission_required = 'idea.add_idea'
	template_name = 'indicators/indicators.html'
	
	def get_queryset(self):

		idea_get = self.request.GET.get('idea_seleccionada_template')
		query = Q()
		query.add(Q(id_idea_id=idea_get), Q.AND)
		#query.add(Q(id_idea_id=4), Q.AND)
		#query.add(Q(id_phase_id=1), Q.AND)

		queryset = self.model.objects.filter(
			query).values(
				'id_phase_id',
				'id_phase__name',
				'phase_date',
				'phase_date_previous'
			).order_by('id_phase_id')

		return queryset


	def get(self, request, *args, **kwargs):
		if request.is_ajax():

			data_day_phase = []
			for i in self.get_queryset():
				if  i['phase_date_previous'] is None:
					i['phase_date_previous']=datetime.now().date()
					previous = i['phase_date_previous']-i['phase_date']
					day=previous.days
					semana=previous.days/7
					semana=round(semana,0)
					data_day_phase.append({"phase_name":i["id_phase__name"],"day":day,"semana":semana, "dia_inicio":i['phase_date'],"dia_fin":i['phase_date_previous']})
				else:
					previous = i['phase_date_previous']-i['phase_date']
					day=previous.days
					semana=previous.days/7
					semana=round(semana,0)
					data_day_phase.append({"phase_name":i["id_phase__name"],"day":day,"semana":semana,"dia_inicio":i['phase_date'],"dia_fin":i['phase_date_previous']})

			#https://dev.to/sharmapacific/how-to-return-json-encoded-response-for-non-dict-object-2237
			response = JsonResponse(data_day_phase,safe=False)

			return response
		else:
			return JsonResponse({'day':0})


class IdeaAnual(PermissionRequiredMixin,View):
	
	template_name = 'indicators/indicators.html'
	model = Idea
	permission_required = 'idea.add_idea'


	def get_graph_idea_year_moth(self):
		data = []
		try:
			year=datetime.now().year
			for m in range(1, 13):
				total = Idea.objects.filter(creation_date__year=year,creation_date__month=m).aggregate(r=Coalesce(Count('id'),0)).get('r')
				data.append(int(total))			
		except:
			pass
		return data


	def get_graph_idea_priority(self):
		try:		
			query = list(Idea.objects.filter(priority__isnull=False,is_active=True).values_list('priority').annotate(r=Count('id')))
			data_priority= [list(i)for i in query]
		except:
			pass
		return data_priority


	def get_graph_idea_type_innovation(self):
		try:
			queryset = list(Idea.objects.filter(innovation_type__isnull=False,is_active=True).values_list('innovation_type').annotate(r=Count('id')))
			data_type_innovation= [list(i)for i in queryset]
		except:
			pass
		return data_type_innovation


	def get_general_roi(self):
		try:
			general_roi=0
			gain=0
			investement=0

			query_idea = Idea.objects.all()
			gain = int(query_idea.aggregate(gain=Coalesce(Sum('gain'),0)).get('gain'))
			investement= int(query_idea.aggregate(investment=Coalesce(Sum('total_investment'),0)).get('total_investment'))

			general_roi=(gain - investement)/ investement
			general_roi=round(general_roi,4)
			gain = f"{gain:,}".replace(",",".")
			investement = f"{investement:,}".replace(",",".")
		except:
			pass	
		return general_roi, gain,investement


	def get_ranking_innovation(self):
	
		from dateutil.relativedelta import relativedelta
		from datetime import date
		import calendar

		fecha_final = date.today()
		future_day = fecha_final.day
		future_month = (fecha_final.month - 3) % 12
		future_year = fecha_final.year + ((fecha_final.month - 3) // 12)
	
		fecha_inicial = date(future_year, future_month +1, future_day)

		year = str(fecha_final.strftime("%Y"))
		month = str(fecha_final.strftime("%m"))

		series_data = {}
		lista_years = []
		lista_avatar=[]
		avatars = [
			'https://rgprincipal.com/es/wp-content/uploads/2020/11/avatar-02-512.png',
			'https://www.pngkit.com/png/full/115-1150342_user-avatar-icon-iconos-de-mujeres-a-color.png',
			'https://electronicssoftware.net/wp-content/uploads/user.png',
			'https://www.shareicon.net/data/512x512/2016/09/15/829453_user_512x512.png',

		] #Se debe traer la imagen desde la base de datos

		fecha_lista = []
		
		for i in range(4):
			
			mes = str(fecha_inicial.strftime("%b"))+'_'+str(fecha_inicial.year)
			month_restado = fecha_inicial.strftime("%m")
			ano_inicial = fecha_inicial.strftime("%Y")
			ano_final = fecha_final.strftime("%Y")
			id_fecha = int(fecha_inicial.year)+int(fecha_inicial.strftime("%m"))
			series_data[id_fecha]=[]
			lista_years.append(id_fecha)
			ultimo_dia = calendar.monthrange(int(ano_inicial),fecha_inicial.month)
			fecha_inicial += relativedelta(months=1)

			fecha_rango_inicial = str(ano_inicial)+"-"+str(month_restado)+"-"+"01"
			fecha_rango_final = str(ano_final) +"-"+str(month_restado)+"-"+str(ultimo_dia[1])
			
			fecha_lista.append({
				'id': id_fecha,
				'mes': mes
			})

			queryset = Action.objects.filter(date__range=[fecha_rango_inicial, fecha_rango_final]).values('id_user__email').prefetch_related('id_user').annotate(total_score=Sum('score')).order_by('-total_score')[:3]

			for a in queryset:
				
				series_data[id_fecha].append([a['id_user__email'],a['total_score']])
				lista_avatar.append({
					'correo':a['id_user__email'],
					'imagen':avatars[i] #Se debe trar de la BD y llamarla como se llama en correo, eliminando la lista de avatars
				})

		return fecha_lista,series_data,lista_years,lista_avatar
	

	""" 
	def get_table_indicator(self):
		data = []
		phases = [2,3,4]

		queryset = Idea.objects.filter(
			
				#priority=('ALTA'),
				#innovation_type=('PRODUCTO'),
				is_active=True
				).values('priority','innovation_type','current_phase').annotate(Conteo=Count('id')).order_by('priority')[:10]

		data_list=[]
		for query in queryset:
			print("--- ",query)
			
			fase_actual =query['current_phase']
	
			if(fase_actual==1):
				fase_actual = "Pain"
			elif (fase_actual==2):
				fase_actual = "Observación"
			elif (fase_actual==3):
				fase_actual = "Ideación"
			elif (fase_actual==4):
				fase_actual = "Prototipado"
			elif (fase_actual==5):
				fase_actual = "Implementación"
			elif (fase_actual==6):
				fase_actual = "Ideas en Stand By"
			else:
				fase_actual = "Sin Fase"


			# data_list.append({
			# 	'Prioridad':query['priority'],
			# 	'Tipo de Innovación':query['innovation_type'],
			# 	fase_actual:query['Conteo'],
			# })
		
			data_list.append({
				'Prioridad':query['priority'],
				'Tipo de Innovación':query['innovation_type'],
				'':query['Conteo'],
			})

		print("data_list-----------",data_list)
		return queryset
	"""

	def get_link_plantilla(self):
		link = Indicators.objects.all()
		return link


	def get(self, request, *args, **kwargs):
		context = {}
		context['graph_idea_year_moth'] = self.get_graph_idea_year_moth()
		context['graph_idea_prority_data'] = self.get_graph_idea_priority()
		context['graph_idea_type_innovation'] = self.get_graph_idea_type_innovation()
		context['general_roi'] = self.get_general_roi()
		context['link'] = self.get_link_plantilla()
		context['innovator'] = self.get_ranking_innovation()


		return render(request, self.template_name, context)


