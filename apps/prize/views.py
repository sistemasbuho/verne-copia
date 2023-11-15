from django.contrib.auth.decorators import login_required,permission_required
from django.views.generic import ListView,CreateView
from django.urls import reverse,reverse_lazy
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,JsonResponse
from django.db.models import F
from .models import *
from .forms import *
from django.contrib.auth.mixins import PermissionRequiredMixin
from apps.idea.views import SearchUserAjax, SearchAjaxIdea, _FormValid
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.serializers.json import DjangoJSONEncoder
import json
import math       
import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


# Ver premios --------------------------------------------------------------

class visualizePrize(ListView,PermissionRequiredMixin):
	model = Prize
	template_name = 'prize/visualize.html'
	permission_required = 'prize.rol_user_view'
 
	def get_queryset(self):
		if User.objects.filter(id=self.request.user.id,userleguas__quantity=None):
			UserLeguas.objects.create(quantity=0,category=1, id_user_id=self.request.user.id,inscription_club=False)
		query= Prize.objects.all().values("id","name", "score", "image")
		datas=json.dumps(list(query), cls=DjangoJSONEncoder)
		return datas

	def get_context_data(self):
		contexto = {}
		contexto['datas'] = self.get_queryset() 
		contexto['score'] = UserLeguas.objects.filter(id_user_id=self.request.user.id).values_list('quantity',flat=True).first()
		contexto['percent']= math.floor((contexto['score'])*100/20000)
		if AssignedPrize.objects.filter(id_user=self.request.user.id, id_prize=6).exists():
			contexto['first'] = "true"
		else:
			contexto['first'] = "false"
		return contexto


# Asignar premio ----------------------------------------------------------	

class AssignedPrizeAjax(PermissionRequiredMixin,CreateView):
	model = AssignedPrize
	permission_required = 'prize.rol_admin_view'
	form_class = RegisterPrizeAjax
	template_name = 'prize/register_prize.html'
	success_url = 'prize:register_prize'
	success_message = 'Se ha redimido el premio con éxito'
	error_message = 'No cuentas con los puntos suficientes'

	def get_context_data(self,**kwargs):
		contexto = {}
		contexto['form'] = self.form_class
		contexto['verbose_name_model'] = self.model._meta.verbose_name_plural
		return contexto
	
	def post(self, request, *args, **kwargs):
		if request.is_ajax():
			form = self.form_class(request.POST)
			form_header = dict(request.POST.lists())

			if 'id_user' in form_header:
				user_id_query = User.objects.filter(pk__in=form_header['id_user'])
				form.fields['id_user'].queryset = user_id_query
			
			email_list = user_id_query.values('email')
			lista_nueva = []

			for lista in email_list:
				lista_nueva.append(lista['email'])	
			
			host_email = [settings.EMAIL_HOST_USER]
			lista_nueva.extend(host_email)
 	    
			if  form_header['id_user'] == ['']:
				id_user_query = User.objects.none()
			else:
			
				id_user_query = User.objects.filter(pk__in=form_header['id_user'])
				form.fields['id_user'].queryset = id_user_query

			if form.is_valid():

				# Para el reenvio de email	
				try:
					body = render_to_string(
							'emails/nuevo_premio.html', {
								'name': request.POST.get('name'),
								'date': request.POST.get('date'),
							},
						)
					email_message = EmailMessage(
					subject='¡Has redimido un premio en Verne!',
					body=body,
					from_email=host_email,
					to=lista_nueva,
					)
					email_message.content_subtype = 'html'
					email_message.send()
				except ObjectDoesNotExist as e:
					error = e
				#Trae el precio
				#score_prize=Prize.objects.filter(id__in=form_header['id_prize']).values_list('score', flat=True).get(id__in=form_header['id_prize'])
				score_prize=Prize.objects.values_list('score',flat=True).get(id__in=form_header['id_prize'])
				lista_sin_puntos = ""
				lista_con_puntos = ""

				for i, user in enumerate(form_header['id_user']):
			
					query_score=UserLeguas.objects.filter(id_user_id=user).values('id_user__email','quantity')		
					mensaje_sin_puntos = 'vacio'
					mensaje_con_puntos = 'vacio'
			
					if query_score[0]['quantity'] < score_prize:
						mensaje_sin_puntos = f"Usuario: {query_score[0]['id_user__email']} \n Total de puntos es: {query_score[0]['quantity']} <hr>"
						lista_sin_puntos+=mensaje_sin_puntos+" \n"

					else:
						UserLeguas.objects.filter(id_user_id=user).update(quantity=F('quantity')-int(score_prize))
						form.save()
						mensaje_con_puntos = f"Usuario: {query_score[0]['id_user__email']} \n Total de puntos es: {query_score[0]['quantity']} <hr>"
						lista_con_puntos+=mensaje_con_puntos+" \n"
				
				response = JsonResponse({'puntos_premio':score_prize,'mensaje_con_puntos': lista_con_puntos,'mensaje_sin_puntos': lista_sin_puntos,'error':'No hay error!'})
				response.status_code = 201
				return response

			else:
				mensaje = f'{self.model.__name__} {self.error_message}'
				error = form.errors
				response = JsonResponse({'mensaje': mensaje, 'error': error})
				response.status_code = 400
				return response
		else:
			return redirect(str(self.success_url))


# Eliminar premio en usuario ----------------------------------------------------------

@login_required()
@permission_required('prize.rol_admin_view', raise_exception=True)

def deletePrize(request,pk):
	if request.method == 'GET':
		return render(request,'prize/delete_prize.html',{'pk':pk})
	else:
		query=AssignedPrize.objects.filter(id=pk).values('id_prize__score','id_user')

		for user in query:
			UserLeguas.objects.filter(id_user_id=user['id_user']).update(quantity=F('quantity')+user['id_prize__score'])			
		AssignedPrize.objects.filter(id=pk).delete()
		return HttpResponseRedirect(reverse('prize:details_score',args=[pk]))


#Lista de usuarios----------------------------------------------------------
 
class visualizeUser(ListView,PermissionRequiredMixin):
	model = UserLeguas
	template_name = 'leguas/visualize_user.html'
	context_object_name = 'users'  
	queryset = UserLeguas.objects.filter(id_user_id__is_active=True).select_related('id_user')
	permission_required = 'prize.rol_admin_view'

	

# Detalles leguas usuario ----------------------------------------------------------

@login_required()
@permission_required('prize.rol_user_view', raise_exception=True)

def detailsScoreUser(request, id_user):
	if User.objects.filter(id=request.user.id,userleguas__quantity=None):
		UserLeguas.objects.create(quantity=0,category=1,id_user_id=request.user.id,inscription_club=False)
  
	score_user= Action.objects.filter(id_user=id_user).select_related('id_idea')
	detail_user= UserLeguas.objects.select_related('id_user').filter(id_user=id_user)
	redem_prize=AssignedPrize.objects.filter(id_user=id_user).select_related('id_prize')
	total_prize=redem_prize.count()
	return render(request,'leguas/details_score.html',
               {'id_user':id_user,'score_user':score_user, 'detail_user':detail_user, 'redem_prize':redem_prize, 'total_prize':total_prize})


#Asignacion de puntos---------------------------------------------------------

class ScoreUser(_FormValid,CreateView):
	model = Idea
	permission_required = 'prize.rol_admin_view'
	form_class = AssignedLeguas
	template_name = 'leguas/score_user_register.html'
	success_url = reverse_lazy('prize:visualize_user')
	success_message = '¡Los puntos fueron asignados correctamente!'
	error_message = 'No se guardo con exito.'

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST) #cargo los datos del formulario
		form_header = dict(request.POST.lists())

		if 'id_user' in form_header:
			user_id_query = User.objects.filter(pk__in=form_header['id_user'])
			form.fields['id_user'].queryset = user_id_query
   
		email_list = user_id_query.values('email')
		lista_nueva = []

		for lista in email_list:
			lista_nueva.append(lista['email'])	
		host_email = [settings.EMAIL_HOST_USER]
		lista_nueva.extend(host_email)
 	    
		if form.is_valid():
			form.save()
			users=form.cleaned_data['id_user']
			score=form.cleaned_data['score']
			for user in users:
				if not UserLeguas.objects.filter(id_user=user.id).exists():
					UserLeguas.objects.create(id_user_id=int(user.id), category="1", quantity=score)
				else:
					UserLeguas.objects.filter(id_user_id=user).update(quantity=F('quantity')+ score)	
		
			# Para el reenvio de email	
			try:
				body = render_to_string(
						'emails/nuevos_puntos.html', {
							'name': request.POST.get('name'),
							'date': request.POST.get('date'),
							'description': request.POST.get('description'),
							'score': request.POST.get('score'),

						},
					)
				email_message = EmailMessage(
				subject='¡Tienes nuevos puntos en Verne!',
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


# Clases que heredan de la app de Idea para los campos con AJAX ----------------------------------------

class UserAjaxScore(SearchUserAjax):
	pass

class IdeaAjaxScore(SearchAjaxIdea):
	pass


# Eliminar accion en usuario ----------------------------------------------------------

@login_required()
@permission_required('prize.rol_admin_view', raise_exception=True)

def deleteAction(request,pk):
	users = Action.objects.filter(id=pk)

	if request.method == 'GET':
		return render(request,'leguas/delete_action.html',{'pk':pk, 'users':users})
	else:
		query= Action.objects.filter(id=pk).values('id_user','score')

		for user in query:
			UserLeguas.objects.filter(id_user_id=user['id_user']).update(quantity=F('quantity')-user['score'])	
		remove=Action.objects.filter(id=pk).delete()
		return HttpResponseRedirect(reverse('prize:visualize_user')) 


# Inactivar usuario ----------------------------------------------------------

@login_required()
@permission_required('prize.rol_admin_view', raise_exception=True)
def inactiveUser(request,pk):
	if request.method == 'GET':
		return render(request,'leguas/inactive_user.html',{'pk':pk})
	else:
		User.objects.filter(id=pk).update(is_active=False)
		return HttpResponseRedirect(reverse('prize:visualize_user')) 

		
# Inscribir al club Verne ----------------------------------------------------------

@login_required()
@permission_required('prize.rol_admin_view', raise_exception=True)
def InscriptionClub(request,pk):
	if request.method == 'GET':
		return render(request,'leguas/club_user.html',{'pk':pk})
	else:
		UserLeguas.objects.filter(id_user=pk).update(inscription_club=True)
		return HttpResponseRedirect(reverse('prize:visualize_user')) 


@login_required()
@permission_required('prize.rol_user_view', raise_exception=True)
def PremioRedimido(request):

	if User.objects.filter(id=request.user.id,userleguas__quantity=None):
		UserLeguas.objects.create(quantity=0,category=1,id_user=request.user.id,inscription_club=False)
  
	if request.method == 'GET':
		result = request.GET.get('result', None)
		# Any process that you want
	
	else:
		dato = request.POST['premio_name']
		json_acceptable_string = dato.replace("'", "\"")
		d = json.loads(json_acceptable_string)
	
		#Trae el precio
		data_prize=[]
		total_score_redem= 0
  
		for key in d:
			score_prize=Prize.objects.values_list('score',flat=True).get(id=int(key))
			total_score_redem += score_prize
			data_prize.append(Prize.objects.values_list('score','name').get(id=int(key)))
   
		lista_sin_puntos = ""
		lista_con_puntos = ""
  
		query_score=UserLeguas.objects.filter(id_user_id=request.user.id).values('id_user__email','quantity')		
		mensaje_sin_puntos = 'vacio'
		mensaje_con_puntos = 'vacio'
			
		if query_score[0]['quantity'] < total_score_redem:
			mensaje_sin_puntos = f"Usuario: {query_score[0]['id_user__email']} \n no alcanzas a redimir los premios, el total de puntos es: {query_score[0]['quantity']} <hr>"
			lista_sin_puntos+=mensaje_sin_puntos+" \n"
			print("No se asignaron")

		else:
			for key in d:
				instance = AssignedPrize.objects.create(id_prize_id = int(key)) 
				instance.id_user.add(int(request.user.id)),
    
			UserLeguas.objects.filter(id_user_id=request.user.id).update(quantity=F('quantity')-int(total_score_redem))
			mensaje_con_puntos = f"Usuario: {query_score[0]['id_user__email']} \n Felicidades, el total de puntos es: {query_score[0]['quantity']} <hr>"
			lista_con_puntos+=mensaje_con_puntos+" \n"
			print("Se asignaron super ok", request.user.email)
  
			lista_nueva = [str(request.user.email),]
			host_email = [settings.EMAIL_HOST_USER]
			lista_nueva.extend(host_email)
   

			# Para el reenvio de email	
			try:
				body = render_to_string(
						'emails/prize_by_user.html', {
							'user':request.user.email,
							'date': datetime.datetime.now() ,
							'name': data_prize,
		
						},
					)
				email_message = EmailMessage(
				subject='¡Se ha solicitado un premio en Verne!',
				body=body,
				from_email=host_email,
				to=lista_nueva,
				)
				email_message.content_subtype = 'html'
				email_message.send()
			except ObjectDoesNotExist as e:
				error = e
   
		response = JsonResponse({'puntos_premio':total_score_redem,'mensaje_con_puntos': lista_con_puntos,'mensaje_sin_puntos': lista_sin_puntos,'error':'No hay error!'})
		response.status_code = 201
	
		return HttpResponseRedirect(reverse('prize:visualize_prize')) 