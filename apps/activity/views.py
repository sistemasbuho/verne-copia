from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render,redirect
from django.views.generic import ListView 
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import *
from apps.prize.models import Action,UserLeguas
from django.db.models import F
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.views.generic import CreateView
from apps.idea.views import SearchAjaxIdea,SearchUserAjax,_FormValid
from django.contrib.auth.mixins import PermissionRequiredMixin


# Registro de Actividad----------------------------------------------------------		

class RegisterActivity(_FormValid,CreateView):
	model = Activity
	permission_required = 'activity.add_activity'
	form_class = RegisterActivityForm
	template_name = 'activity/register.html'
	success_url = reverse_lazy('activity:view_activity')
	success_message = '¡La actividad se ha creado con éxito!'
	error_message = 'No se guardó con éxito la actividad'

	#n+1 solucionado
	def post(self, request):
		form = self.form_class(request.POST) #cargo los datos del formulario
		form_header = dict(request.POST.lists())

	 
		if 'id_user' in form_header:
			users_invited = User.objects.filter(pk__in=form_header['id_user'])
			form.fields['id_user'].queryset = users_invited
   
		email_list = users_invited.values('email')
		lista_nueva = []

		for lista in email_list:
			lista_nueva.append(lista['email'])	
		
		host_email = [settings.EMAIL_HOST_USER]
		lista_nueva.extend(host_email)
 	    
		if form.is_valid():
			form.save()
   
			#Revision a cambiar una vez se finaliza actividad
			Activity.objects.filter(score=None).update(score=0)

			# Para el reenvio de email	
			try:
				
				body = render_to_string(
						'emails/nueva_actividad.html', {
							'nombre': request.POST.get('name'),
							'fecha': request.POST.get('date'),
							'description': request.POST.get('description'),
							'score': request.POST.get('score'),

						},)
	
				email_message = EmailMessage(
				subject='¡Tienes una nueva actividad en Verne!',
				body=body,
				from_email=host_email,
				to=lista_nueva, )
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

class UserAjaxActivity(SearchUserAjax):
	pass

class IdeaAjaxActivity(SearchAjaxIdea):
	pass


# Ver actividades------------------------------------------------------------------------

class watchActivity(ListView,PermissionRequiredMixin):
	model = Activity
	template_name = 'activity/visualize.html'
	context_object_name = 'activity'
	permission_required = 'activity.add_activity'

	def get_queryset(self):
		queryset = {'activity_all':Activity.objects.all().prefetch_related('id_user','id_idea'),}
		return queryset 


class watchActivityUser(ListView,PermissionRequiredMixin):
	model = Activity
	template_name = 'activity/visualize_user.html'
	context_object_name = 'activity'
	permission_required = 'activity.admin_activity'

	def get_queryset(self):
		queryset = {'activity_user':Activity.objects.filter(id_user=self.request.user).prefetch_related('id_user','id_idea')}
		return queryset 



# Editar actividad -------------------------------------------------------------------------

@login_required
@permission_required('activity.add_activity', raise_exception=True)

def UpdateActivity(request, id):
	form = None
	error = None
	try:
		activity = Activity.objects.get(id=id)
		activities = Activity.objects.filter(id=id)
		if request.method == 'GET':
			form = FormUpdateActivity(instance=activity)
		else:
			form = FormUpdateActivity(request.POST, instance=activity)
			if form.is_valid():
				form.save()
			return redirect('activity:view_activity')
	except ObjectDoesNotExist as e:
		error = e
		return render(request, '404.html', {'error':error})
	return render(request, 'activity/details.html', {'form': form,'id':id, 'activity':activities, 'tasks': Task.objects.all(),})


# Subir Archivo actividad------------------------------------------------------------------

@login_required
@permission_required('activity.add_activity', raise_exception=True)

def BasicUploadView(request,pk):
	form = FileForm()
	path=Activity.objects.get(id=pk)
	if request.method == 'POST':
		form = FileForm(request.POST, request.FILES) 
		if form.is_valid():
			if 'annexed' in request.FILES:
				query=Activity.objects.filter(id=pk)
				for obj in query:
					obj.annexed=request.FILES['annexed']
					obj.save()		
			else: 
				pass
	else:
		form = FileForm()
	return render(request, 'activity/upload.html', {'path': path,'form': form,'pk':pk, })


# Eliminar Actividad---------------------------------------------------------------------------

@login_required
@permission_required('activity.add_activity', raise_exception=True)

def delete_activity(request,pk):
	if request.method == 'GET':
		return render(request,'activity/delete.html',{'pk':pk})
	else:
		Activity.objects.filter(id=pk).delete()
		return HttpResponseRedirect(reverse('activity:view_activity'))


# Asignar Leguas Actividad---------------------------------------------------------------------------

@login_required
@permission_required('activity.add_activity', raise_exception=True)

def Assigned_leguas(request,pk):
	values=Activity.objects.filter(id=pk)
	if request.method == 'GET':
		return render(request,'activity/score.html',{'pk':pk ,'values':values})
	else:
		Activity.objects.filter(id=pk).update(redeemed_score=True)
		for activity in values:
			users = User.objects.filter(id__in=activity.id_user.all())
			instance = Action.objects.create(id_activity_id=activity.id,
											 score=activity.score,
											 name=activity.name,
											 description=activity.description,
											 date=activity.date,
											 )
			for user in users:
				instance.id_user.add(user)
				if not UserLeguas.objects.filter(id_user=user.id).exists():
					UserLeguas.objects.create(id_user_id=int(user.id), category="1", quantity=activity.score)
				else:
					UserLeguas.objects.filter(id_user_id=user).update(quantity=F('quantity')+ activity.score)	
		return HttpResponseRedirect(reverse('activity:view_activity'))
