from cProfile import Profile
from re import template
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,permission_required
from django.views.generic import ListView, CreateView,View
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import *
from apps.idea.models import Idea,Phase_Date
from .forms import *
from apps.idea.views import SearchAjaxIdea,SearchUserAjax,_FormValid
from django.urls import reverse_lazy
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import get_template
from weasyprint import CSS, HTML
from django.http.response import HttpResponse
import os
from django.contrib.auth.mixins import PermissionRequiredMixin
from apps.users.models import Profile

# ----------------------------------------------------------------------------------
""" Creación de reunión: El administrador agenda la reuníón y al enviar los datos del formulario
automáticamente , se guarda en la tabla intermedia UserVotes"""

class RegisterMeeting(_FormValid,CreateView,PermissionRequiredMixin):
    
	model = Idea
	permission_required = 'meeting.add_meeting'
	form_class = RegisterMeetingForm
	template_name= 'meeting/register_meeting.html'
	sucess_url = reverse_lazy('meeting:visualize')
	success_message = '¡La reunión fue creada correctamente!'
	error_message = 'No se guardo con exito.'

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		form_header = dict(request.POST.lists())

		if 'user_comitte' in form_header:
			user_comitte_query = User.objects.filter(pk__in=form_header['user_comitte'])  #[1,2,3]
			form.fields['user_comitte'].queryset = user_comitte_query

		email_list = user_comitte_query.values('email')
		lista_nueva = []
		
		for lista in email_list:
			lista_nueva.append(lista['email'])

		host_email = [settings.EMAIL_HOST_USER]
		lista_nueva.extend(host_email)

		if form.is_valid():
			users_invited = form.cleaned_data['user_comitte']
			metting_save = form.save()
			idea_query = Idea.objects.filter(meeting__id=metting_save.pk )
			for user in users_invited:
				user_comite = user.id
				for idea in idea_query:
					UserVotes.objects.create(
						id_meeting_id = metting_save.pk,
						id_idea_id = int(idea.id), 
						id_user_comitte_id = int(user_comite),)

			try:
			    
				body = render_to_string(
					'emails/nueva_reunion.html', {
					   	'name': request.POST.get('name'),
						'date': request.POST.get('date'),
						'place': request.POST.get('place'),
      					'start_time': request.POST.get('start_time'),
           				'end_time': request.POST.get('end_time'),	},)
				email_message = EmailMessage(
					subject='¡Tienes una nueva reunión en Verne!',
					body=body,
					from_email=host_email,
					to=lista_nueva,
					)
				email_message.content_subtype = 'html'
				email_message.send()
			except ObjectDoesNotExist as e:
				error = e
			return self.form_valid(form)
		else:

			self.form_invalid(form)
		return redirect(str(self.success_url))


# Clases que heredan de la app de Idea para los campos con AJAX ----------------------------------------

class UserAjaxMeeting(SearchUserAjax):
	pass

class IdeaAjaxMeeting(SearchAjaxIdea):
	pass

# Editar Reunión-----------------------------------------------------------------------------------------

@login_required()
@permission_required('meeting.add_meeting', raise_exception=True)

def UpdateMeeting (request, id):
    form = None
    error = None
    try:
        meeting = Meeting.objects.get(id=id)
        if request.method == 'GET':
            form = MeetingUpdateForm(instance=meeting)
            form.fields['user_comitte'].queryset = User.objects.filter(pk__in=form.instance.user_comitte.all())
            form.fields['id_idea'].queryset = Idea.objects.filter(pk__in=form.instance.id_idea.all())

        else:
            form = MeetingUpdateForm(request.POST, instance=meeting)
            form_header = dict(request.POST.lists())
            
            if 'user_comitte' in form_header:
                collaborator_query = User.objects.filter(pk__in=form_header['user_comitte'])  #[1,2,3]
                form.fields['user_comitte'].queryset = collaborator_query

            if 'id_idea' in form_header:
                merge_idea_query = Idea.objects.filter(pk__in=form_header['id_idea'])
                form.fields['id_idea'].queryset = merge_idea_query

            if form.is_valid():	
                form.save()
                
            return HttpResponseRedirect(reverse('meeting:update',args=[id]))
    except ObjectDoesNotExist as e:
        error = e
        return render(request, '404.html', {'error':error})
  
    return render(request, 'meeting/update.html', 
    {'form': form,'error': error})


#Lista de actividades ---------------------------------------------------------------------------------
	
class watchMeeting(ListView,PermissionRequiredMixin):
	model = Meeting
	template_name = 'meeting/visualize_meeting.html'
	context_object_name = 'meeting'
	permission_required = 'meeting.view_meeting'

	def get_queryset(self):
			queryset = { 'meeting_all':Meeting.objects.all().prefetch_related('id_idea','user_comitte')}
						 # 'meeting_user':Comitte.objects.filter(user_is_active=True).prefetch_related('user_comitte')}
			return queryset 

# ------------------------------------------------------------------------------------------------------------------
"""Para crear el sistema de votación,consultamos las ideas que están agendadas en una reunión y que aún no se
han calificado en su última fase. Una vez ingresa el Usuario Comité puede votar una sola vez por cada idea, hasta
que la reunión este 'cerrada'"""

@login_required
@permission_required('meeting.view_meeting', raise_exception=True)

def registerComment(request,pk,id_idea):
	list_comments = []
	idea_query = Idea.objects.filter(
		uservotes__id_meeting=pk,
		uservotes__is_evaluate=False,
		uservotes__id_user_comitte=request.user.id, )
	is_voted=idea_query.count()
	
	for idea in idea_query:
     
		# Forma de traer la fase por consulta
		# consulta = Phase_Date.objects.prefetch_related('id_idea','id_phase').filter(id_idea_id=idea.id).values('id_phase_id').last()
		# idea_fases= consulta['id_phase_id']
  
		if idea.id == id_idea:
			list_comments.append({'id_meeting':pk,
							'id_idea':idea.id,
							'user':request.user.email,
       						})

	if request.method== 'POST':

		form=RegisterComment(request.POST)
		if form.is_valid():	
			UserVotes.objects.filter(
				id_meeting_id=pk,
				id_idea_id=request.POST.get("idea_input"),
				id_user_comitte=request.user.id,

			).update(is_evaluate=True,
					vote=form.cleaned_data['vote'],
					vote_priority=form.cleaned_data['vote_priority'],
					message=form.cleaned_data['message'],
					phase_actual=request.POST.get('id_idea_phase') )
		else:
			print("No es validooo")
		return HttpResponseRedirect(reverse('meeting:detail_meeting',args=[pk]))			
	else:
		form = RegisterComment()
	return render(request,'meeting/register_comment.html',
			{'form':form,'meetings_idea':list_comments, 'is_voted':is_voted, 'id_idea':id_idea})


# ----------------------------------------------------------------------------------------------------------------------------
"""Visualizar los detalles de la reunión, cargar el acta de reunión y
ver el estado de los votos por idea y cambia de fase si todos fueron aprobados"""

@login_required
@permission_required('meeting.view_meeting', raise_exception=True)

def comments_list(request, id_reu, id_idea):
	comentarios=UserVotes.objects.filter(id_meeting=id_reu,id_idea=id_idea)
	comentarios_total=UserVotes.objects.filter(id_meeting=id_reu,id_idea=id_idea).count()
	
	#fase
	next_fase=UserVotes.objects.filter(id_meeting=id_reu,id_idea=id_idea,vote=1).count()
	kepp_fase=UserVotes.objects.filter(id_meeting=id_reu,id_idea=id_idea,vote=2).count()
	die_idea=UserVotes.objects.filter(id_meeting=id_reu,id_idea=id_idea,vote=3).count()

	#prioridad
	priority_up=UserVotes.objects.filter(id_meeting=id_reu,id_idea=id_idea,vote_priority=1).count()
	priority_down=UserVotes.objects.filter(id_meeting=id_reu,id_idea=id_idea,vote_priority=2).count()
	kepp_priority=UserVotes.objects.filter(id_meeting=id_reu,id_idea=id_idea,vote_priority=3).count()
	print('kepp_priority',kepp_priority)

	none_idea= comentarios_total -(next_fase + kepp_fase + priority_up + priority_down+die_idea + kepp_priority) 

	# members=Meeting.objects.filter(user_comitte).count() 
	return render(request,'meeting/comments_list.html',{'comments_meetings_idea':comentarios, 'kepp_priority':kepp_priority,'next_fase':next_fase, 'kepp_fase':kepp_fase, 
	          'priority_up':priority_up, 'priority_down':priority_down, 'die_idea':die_idea, 'comentarios_total':comentarios_total,'none_idea':none_idea, 'id_idea':id_idea })

# Subir archivo -------------------------------------------------------------------------------------------------------------

@login_required
@permission_required('meeting.view_meeting', raise_exception=True)

def BasicUploadView(request,pk):
	path=Meeting.objects.get(id=pk)
	form = FileForm()
	if request.method == 'POST':
		form = FileForm(request.POST, request.FILES)  
		if form.is_valid():
			if 'document_act' in request.FILES:
				query=Meeting.objects.filter(id=pk,)
				for obj in query:
					obj.document_act=request.FILES['document_act']
					obj.save()
	else:
		form = FileForm()
	return render(request, 'meeting/upload.html', {'path': path,'form': form, 'pk':pk})

# ---Cards_detalle reunion	----------------------------------------------------

@login_required
@permission_required('meeting.view_meeting', raise_exception=True)

def detailMeeting(request,pk):
	meeting_query= Meeting.objects.filter(id=pk)
	idea_query= UserVotes.objects.filter(id_meeting=pk).distinct('id_idea').select_related('id_idea')
	all_idea=Idea.objects.filter(meeting__id=pk).count()
	idea_like=Idea.objects.filter(meeting__id=pk,uservotes__vote=2).count()
	all_coments=UserVotes.objects.filter(id_meeting=pk).values('message').count()

	return render(request,'meeting/detail_meeting.html',{'idea_query':idea_query,'meetings':meeting_query,'reunion_pk':pk,
			'all_idea':all_idea,'idea_like':idea_like,'all_coments':all_coments
			})	


# ---Cards_cerrar reunion	----------------------------------------------------
@login_required()
@permission_required('idea.add_meeting', raise_exception=True)

def closeMeeting (request,pk):
	if request.method == 'GET':
		return render(request,'meeting/close_meeting.html',{'pk':pk})
	else:   		
		Meeting.objects.filter(id=pk).update(is_active=False,)
		return HttpResponseRedirect(reverse('meeting:detail_meeting',args=[pk]))


# Generador de PDF --------------------------------

class MeetingGeneratorPdf(View,PermissionRequiredMixin):
    permission_required = 'meeting.view_meeting'

    def get(self, request, *args, **kwargs):

        template=get_template("prints/act_meeting.html")

        meeting= Meeting.objects.filter(id=kwargs['pk'])
        votes = UserVotes.objects.filter(id_meeting=kwargs['pk']).order_by('id_idea')

        context = {"id":kwargs['pk'],
            "meetings":meeting,
            "votes":votes
        }
        
        html = template.render(context)
        css_url = os.path.join(settings.BASE_DIR, 'static/plugins/tempusdominus-bootstrap-4/css/tempusdominus-bootstrap-4.min.css')

        pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
        response = HttpResponse(pdf, content_type='application/pdf')

        file_name = 'Acta_reunion.pdf' # Agrega fecha y hora al nombre del archivo
        response['Content-Disposition'] = 'attachment; filename=%s' % file_name
        # response.write(output.getvalue())	 # Al configurar el tipo de HttpResponse, si da un valor, no es necesario que escriba esta oración
        return response