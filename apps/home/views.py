from django.shortcuts import render, redirect
from .models import  *
from .forms import FormIdeaRegisterExternal
from django.contrib import messages

from django.contrib.auth import login, authenticate, logout #add this

from django.contrib.auth.forms import AuthenticationForm #add this


from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist

import datetime

fecha_actual = datetime.date.today()
fecha_formateada = fecha_actual.strftime('%d/%m/%Y')



def  ViewHome(request):
	form = None
	error = None

	lista_nueva = []

	host_email = [settings.EMAIL_HOST_USER]
	#lista_nueva.append(host_email)

	if request.method == 'GET':
		form = FormIdeaRegisterExternal()

	else:
		form = FormIdeaRegisterExternal(request.POST)
		if form.is_valid():
			form.save()
			try:
				form_header = dict(request.POST.lists())

				lista_nueva.append(form_header['external_email'])
				print('lista_nueva',lista_nueva[0])

				body = render_to_string(
						'emails/idea_recibida.html', {
							'title': request.POST.get('title'),
							'nombre': str(form_header['external_name']).replace("['","").replace("']",""),
							'fecha': fecha_formateada,
						},
					)
				email_message = EmailMessage(
				subject='Tu idea ha sido registrada en Verne',
				body=body,
				from_email=host_email,
				to=lista_nueva[0],
				)
				email_message.content_subtype = 'html'
				email_message.send()
				# Para el reenvio de email	
				body_proveedor = render_to_string(
						'emails/idea_recibida.html', {
							'title': request.POST.get('title'),
						},
					)
				
				
				email_message_proveedor = EmailMessage(
				subject='Se ha registrado una nueva idea en Verne',
				body=body_proveedor,
				from_email=host_email,
				to=['verne@gnilat.com',],
				)
				email_message_proveedor.content_subtype = 'html'
				email_message_proveedor.send()
				print('email_message_proveedor',email_message_proveedor)
			except ObjectDoesNotExist as e:
				error = e

			messages.success(request, "Tu idea se ha enviado con éxito", extra_tags='God Job')
			form = FormIdeaRegisterExternal()

	return render(request, 'index.html', 
		{'form': form,'error': error,
   		'menu_logo':MenuLogo.objects.all(),
 		'menu':Menu.objects.all(),
 		'banner_header': BannerHeader.objects.all(),
 		'header_section_explore':HeaderExploreSection.objects.all(),
 		'explore_section':ExploreSection.objects.all(),
 		'process_section':ProcessSection.objects.all(),
 		'metrics':Metrics.objects.all(),
 		'header_section_team':HeaderTeamSection.objects.all(),
 		'team_section':TeamSection.objects.all(),
		'movilizadores_team':MovilizadoresSection.objects.all(),
 		'footer':Footer.objects.all(),
		'header_section_movilizadores_team':HeaderMovilizadoresSection.objects.all(),
		'section_valores':HeaderValoresSection.objects.all(),
		'header_section_valores':ValoressSection.objects.all(),

		})


	

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				# messages.info(request, f"You are now logged in as {username}.")
				return redirect_url_next(request)
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="account/login.html", context={"login_form":form})


def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("login")

def LoginPage (request):
    
	return render(request, "account/login.html",)


def redirect_url_next(request):
	nxt = request.GET.get("next", None)
	path_redirect = request.get_full_path().split('?next=',1)

	if '?next=' in request.get_full_path():
		return redirect(path_redirect[1])

		
	else:
		return redirect(settings.LOGIN_REDIRECT_URL)