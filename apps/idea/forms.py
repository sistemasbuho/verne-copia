from ast import arg
from pickle import TRUE
from django import forms
from .models import Idea,QuestionPhase,Phase_Date, Objective,Phase, Task, TaskByIdea,ExternalIdea, Frente
from django.contrib.auth.models import User
from datetime import datetime


class MergeIdeaForm(forms.ModelForm):
	class Meta:
		model=Idea
		fields = ['id_merge','is_merge']


class UpdateQuestion(forms.Form):
	preguntas = QuestionPhase.objects.all()
	

class FormIdeaRegister(forms.ModelForm):
	class Meta:
		model = Idea
		fields=['title','description','collaborator','conditions','area','beneficio','descripcion_beneficio','innovation_type', 'innovation_estrategia','id_phase','current_phase']
		#fields = ['external_name', 'documento', 'grencia_nombre', 'subregion_nombre', 'title', 'description','frente_nombre', 'state', 'dimension_nombre', 'pilar_nombre']

		widgets = {
			'title':forms.TextInput(
				attrs={
					'required': True,
					'class':'form-control',
					'placeholder':'Dale un gran nombre a tu idea',
					'id':'title' }),
			'description':forms.Textarea(
				attrs={
					'required': True,
					'class':'form-control',
					'placeholder':'¿Cómo nació esta idea? ¿Qué problema o necesidad esta resolviendo?',
					'id':'description',
					'rows':4, 
					'cols':15,}),

			'innovation_type':forms.Select(
				attrs={
					'required': True,
					'placeholder':'Selecciona una opción',
					'class':'form-control',
					'id':'innovation_type', }),
			'innovation_estrategia':forms.Select(
				attrs={
					'required': True,
					'placeholder':'Selecciona una opción',
					'class':'form-control',
					'id':'innovation_estrategia', }),
			'area':forms.Select(
				attrs={
					'required': True,
					'placeholder':'Selecciona una opción',
					'class':'form-control',
					'id':'area', }),
			'beneficio':forms.Select(
				attrs={
					'required': True,
					'class':'form-control',
					'placeholder':'Selecciona una opción',
					'id':'beneficio', }),

			'descripcion_beneficio':forms.Textarea(
				attrs={
					'required': True,
					'class':'form-control',
					'placeholder':'Explica los beneficios que quieres obtener',
					'id':'descripcion_beneficio',
					'rows':4, 
					'cols':15,}),


			
			}
		

	
	def __init__(self,*args, **kwargs):
		super(FormIdeaRegister, self).__init__(*args, **kwargs)
		query_user_none= User.objects.none()
		#self.fields['collaborator'].queryset = query_user_none
		#self.fields['id_objective'].queryset = Objective.objects.filter(year=datetime.now().year)
		#self.fields['id_phase'].queryset = Phase.objects.none()
		#self.fields['conditions'].required = True
		

class IdeaUpdateForm(forms.ModelForm):
	class Meta:
		model=Idea
		fields = ['title','description', 'priority','innovation_type','innovation_estrategia', 'descripcion_beneficio','asigned','collaborator','id_merge','roi','score_idea','gain','price_score','total_investment','investment','link_documentation', 'area',  'beneficio', 'conditions','feedback']#, 'segundo_documento', 'tercer_documento']
		widgets = {
			'title':forms.TextInput(
				attrs={
					'class':'form-control',
					'id':'title',
					}),
			'description':forms.Textarea(
				attrs={
					'class':'form-control',
					'id':'description',
					'rows':8, 
					}),
			'feedback':forms.Textarea(
				attrs={
					'class':'form-control',
					'id':'feedback',
					'rows':8, 
					}),
			'solucion':forms.Textarea(
				attrs={
					'class':'form-control',
					'id':'solucion',
					'rows':8, 
					}),

			'descripcion_beneficio':forms.Textarea(
				attrs={
					'class':'form-control',
					'id':'descripcion_beneficio',
					'rows':5, 
					}),	
			'asigned':forms.Select(
				attrs={
					'class':'form-control',
					'id':'asigned', }),
					
			'priority':forms.Select(
				attrs={
					'class':'form-control',
					'id':'priority', }),

			'innovation_type':forms.Select(
				attrs={
					'class':'form-control',
					'id':'innovation_type',
				 }),
			'innovation_estrategia':forms.Select(
				attrs={
					'class':'form-control',
					'id':'innovation_estrategia',
				 }),

			'gain':forms.TextInput(
				attrs={
					'class':'form-control',
					'id':'gain',
					}),

			'roi':forms.TextInput(
				attrs={
					'class':'form-control',
					'id':'roi',
					}),

			'price_score':forms.TextInput(
				attrs={
					'class':'form-control',
					'id':'price_score',
					}),
			'total_investment':forms.TextInput(
				attrs={
					'class':'form-control',
					'id':'total_investment',
					}),


			'score_idea':forms.TextInput(
				attrs={
					'class':'form-control',
					'id':'score_idea',
					}),

			'investment':forms.TextInput(
				attrs={
					'class':'form-control',
					'id':'investment',
					}),
			'link_documentation':forms.TextInput(
				attrs={
					'class':'form-control',
					'id':'link_documentation',
					}),
			'documento':forms.TextInput(
				attrs={
					'required':True,
					'type':'number',
					'class':'form-control',
					'id':'documento',
				}
			),

			'gerencia':forms.Select(
				attrs={
					'class':'form-control',
					'id':'gerencia',
					}),
					
			'subregion':forms.Select(
				attrs={
					'class':'form-control',
					'id':'subregion',
					}),
			'frente':forms.Select(
				attrs={
					'class':'form-control',
					'id':'frente',
					}),
			'dimension':forms.Select(
				attrs={
					'class':'form-control',
					'id':'dimension',
					}),
			'pilar':forms.Select(
				attrs={
					'class':'form-control',
					'id':'pilar',
					}),
			'proposito':forms.Select(
				attrs={
					'class':'form-control',
					'id':'proposito',
					}),
			'external_email':forms.TextInput(
				attrs={
					'class':'form-control',
					'id':'external_email',
					}),
			'external_name':forms.TextInput(
				attrs={
					'class':'form-control',
					'id':'external_name',
					}),

			'primer_documento':forms.TextInput(
				attrs={
					'type':'file',
					'enctype': 'multipart/form-data',
					'id':'primer_documento',
				}
			),
			'segundo_documento':forms.TextInput(
				attrs={
					'type':'file',
					'enctype': 'multipart/form-data',
					'id':'segundo_documento',
				}
			),
			'tercer_documento':forms.TextInput(
				attrs={
					'type':'file',
					'enctype': 'multipart/form-data',
					'id':'tercer_documento',
					
				}
			),

			}

	def __init__(self,*args, **kwargs):
		super(IdeaUpdateForm, self).__init__(*args, **kwargs)
		self.fields['collaborator'].queryset =  User.objects.none()
		#self.fields['region'].queryset =  Subregion.objects.all()
		
		self.fields['id_merge'].queryset = Idea.objects.none()
		self.fields['roi'].disabled= True
		self.fields['score_idea'].disabled= True
		self.fields['price_score'].disabled= True
		self.fields['total_investment'].disabled= True


class FileForm(forms.ModelForm):
	class Meta:
		model = Phase_Date
		fields = ('document',)


class PhaseForm(forms.ModelForm):
	class Meta:
		model=Phase_Date
		fields = ['description','feedback','link_documentation',]

		widgets = {
			'feedback':forms.Textarea(
				attrs={
					'class':'form-control',
					'id':'description',
					'rows':6, 
					}),	
			'description':forms.Textarea(
				attrs={
					'class':'form-control',
					'id':'description',
					'rows':6, 
					}),		
			'link_documentation':forms.TextInput(
				attrs={
					'class':'form-control',
					'id':'link_documentation', }),

			}


class TaskCreateForm(forms.ModelForm):

	class Meta:
		
		TRUE_FALSE_CHOICES = (
			('', 'Todos..'),
			(True, 'Completado'),
			(False, 'Por hacer')
		)

		model = Task
		fields=['user','title','description','complete']

		widgets = {
		
			'title':forms.TextInput(
				attrs={
					'class':'form-control',
					'id':'title_crear',
					}),
			'description':forms.Textarea(
				attrs={
					'class':'form-control',
					'id':'description_crear',
					'rows':8, 
					}),
			'complete':forms.Select(choices=TRUE_FALSE_CHOICES),
		
		}

	def __init__(self,*args, **kwargs):
		super(TaskCreateForm, self).__init__(*args, **kwargs)
		
		self.fields['user'].required = True
		self.fields['title'].required = True
		self.fields['description'].required = False
		self.fields['complete'].widget.attrs['id'] = "complete_crear"
		self.fields['user'].widget.attrs['class'] = "form-control"
		self.fields['user'].widget.attrs['id'] = "user_crear"
		self.fields['user'].queryset =  User.objects.none()


class TaskUpdateForm(forms.ModelForm):

	class Meta:
		
		TRUE_FALSE_CHOICES = (
			(False, 'Por hacer'),
			(True, 'Completado'),  
		)

		model = Task
		fields=['user','title','description','complete']

		widgets = {
		
			'title':forms.TextInput(
				attrs={
					'class':'form-control',
					'id':'title_editar',
					}),
			'description':forms.Textarea(
				attrs={
					'class':'form-control',
					'id':'description_editar',
					'rows':8, 
					}),
			'complete':forms.Select(choices=TRUE_FALSE_CHOICES),
		
		}

	def __init__(self,*args, **kwargs):
		super(TaskUpdateForm, self).__init__(*args, **kwargs)
		
		self.fields['user'].required = True
		self.fields['title'].required = True
		self.fields['description'].required = False
		self.fields['complete'].widget.attrs['id'] = "complete_editar"
		self.fields['user'].widget.attrs['class'] = "form-control"
		self.fields['user'].widget.attrs['id'] = "user_editar"
		self.fields['user'].queryset =  User.objects.none()


class TaskCreateFormIdea(forms.ModelForm):

	class Meta:
		
		TRUE_FALSE_CHOICES = (
			(False, 'Por hacer'),
			(True, 'Completado'),  
		)

		model = TaskByIdea
		fields=['user','title','description','complete']

		widgets = {
		
			'title':forms.TextInput(
				attrs={
					'class':'form-control',
					'id':'title_crear',
					}),
			'description':forms.Textarea(
				attrs={
					'class':'form-control',
					'id':'description_crear',
					'rows':8, 
					}),
			'complete':forms.Select(choices=TRUE_FALSE_CHOICES),
		
		}

	def __init__(self,*args, **kwargs):
		super(TaskCreateFormIdea, self).__init__(*args, **kwargs)
		
		self.fields['user'].required = True
		self.fields['title'].required = True
		
		self.fields['complete'].widget.attrs['id'] = "complete_crear"

		self.fields['user'].widget.attrs['class'] = "form-control"
		self.fields['user'].widget.attrs['id'] = "user_crear"
		self.fields['user'].queryset =  User.objects.none()


class TaskUpdateFormIdea(forms.ModelForm):

	class Meta:
		
		TRUE_FALSE_CHOICES = (
			(False, 'Por hacer'),
			(True, 'Completado'),  
		)

		model = TaskByIdea
		fields=['user','title','description','complete']

		widgets = {
		
			'title':forms.TextInput(
				attrs={
					'class':'form-control',
					'id':'title_editar',
					}),
			'description':forms.Textarea(
				attrs={
					'class':'form-control',
					'id':'description_editar',
					'rows':8, 
					}),
			'complete':forms.Select(choices=TRUE_FALSE_CHOICES),
		
		}

	def __init__(self,*args, **kwargs):
		super(TaskUpdateFormIdea, self).__init__(*args, **kwargs)
		
		self.fields['user'].required = True
		self.fields['title'].required = True
		self.fields['description'].required = False
		

		self.fields['complete'].widget.attrs['id'] = "complete_editar"

		self.fields['user'].widget.attrs['class'] = "form-control"
		self.fields['user'].widget.attrs['id'] = "user_editar"
		self.fields['user'].queryset =  User.objects.none()


class MergeIdeaForm(forms.ModelForm):
	class Meta:
		model=Idea
		fields = ['id_merge','is_merge']




tipo_innovacion_choices=(
	("",'Todos'),
	("PROCESOS","Procesos"),
	("Horizonte 1","Horizonte 1"),
	("Horizonte 2","Horizonte 2"),
	("Horizonte 3","Horizonte 3"))


prioridad_choices =(
	("",'Todos'),
	("ALTA", "Alta"),
	("MEDIA", "Media"),
	("BAJA", "Baja"),
)

#https://ordinarycoders.com/blog/article/using-django-form-fields-and-widgets
class DashboardForm(forms.ModelForm):
	class Meta:
		model=Idea
		fields = ['collaborator']#,'frente']
  
	id_idea = forms.CharField(		
	label='ID idea',
	widget=forms.Select(
		attrs={
			'id':"id_idea",
			'class':'form-control',
			'placeholder':'Selecciona un valor',
			}
		)
	)
 
	titulo = forms.CharField(		
		label='Título idea',
		widget=forms.TextInput(
			attrs={
				'id':"titulo_idea",
				'name':'titulo_idea_name',
				'class':'form-control',
			}
		)
	)

	tipo_innovacion = forms.MultipleChoiceField(
		label='Tipo Innovación',
		choices=tipo_innovacion_choices,
		widget=forms.Select(
			attrs={
				'id':"tipo_innovacion",
				'name':'tipo_innovacion_name',
				'class':'form-control',
			}
		)
	)

	prioridad = forms.MultipleChoiceField(
		label='Prioridad',
		choices = prioridad_choices,
		widget=forms.Select(
			attrs={
				'id':"prioridad",
				'name':'prioridad_name',
				'class':'form-control',
			   }
		)
	)

	datarange = forms.CharField(
		label='Fecha de creación',
		widget=forms.TextInput(
			attrs={
				'id':"daterange",
				'name':'daterange_name',
				'class':'form-control',
				'autocomplete': 'off',
				'placeholder':'YYYY-MM-DD - YYYY-MM-DD',
				#'value':"2018-01-01 - 2021-01-01"
			}
		)
	)
	

	def __init__(self,*args, **kwargs):
		super(DashboardForm, self).__init__(*args, **kwargs)

		try:
			#Se recorre para quitar la tupla
			for collaborator in args:
				print('type(collaborator)',(args))
				print("key 12 ", collaborator.getlist('collaborator'))
				#https://programmerclick.com/article/10101808992/
				dato = collaborator.getlist('collaborator') #así se accede a un QueryDict
				frente = collaborator.getlist('frente')
			print('frente[0]',frente[0])
			qs = User.objects.filter(pk__in=dato)
			#frentes = Frente.objects.filter(pk=frente[0])
			#print(frentes)

		
			#print("qs ",qs)s
		except Exception as error:
			print("error ",error)
			qs = User.objects.none()
			#frentes = Frente.objects.none()
		print("qs ",qs)
  
		self.fields['collaborator'].queryset = qs
		self.fields['collaborator'].required = False
		self.fields['collaborator'].widget.attrs['id'] = "collaborator"
		self.fields['collaborator'].label = "Encargado"
		self.fields['collaborator'].widget.attrs['class'] = "form-control"

		#self.fields['frente'].queryset = frentes
		#self.fields['frente'].required = False
		#self.fields['frente'].widget.attrs['id'] = "frente"
		#self.fields['frente'].label = "Frente"
		#self.fields['frente'].widget.attrs['class'] = "form-control select2-selection select2-selection--multiple"


		self.fields['titulo'].required = False
		self.fields['tipo_innovacion'].required = False
		self.fields['prioridad'].required = False
		self.fields['datarange'].required = False
		self.fields['id_idea'].required = False
		
		
class DashboardFormBanco(forms.ModelForm):

	class Meta:
		model=Idea
		fields = ['area']
	
	id_idea = forms.CharField(		
	label='ID idea',
	widget=forms.Select(
		attrs={
			'id':"id_idea",
			'class':'form-control',
			'placeholder':'Selecciona un valor',
			}
		)
	)
	
	
	titulo = forms.CharField(		
		label='Título idea',
		widget=forms.TextInput(
			attrs={
				'id':"titulo_idea",
				'name':'titulo_idea_name',
				'class':'form-control',
			}
		)
	)

	tipo_innovacion = forms.ChoiceField(
		label='Tipo Innovación',
		choices=tipo_innovacion_choices,
		widget=forms.Select(
			attrs={
				'id':"tipo_innovacion",
				'name':'tipo_innovacion_name',
				'class':'form-control',
			}
		)
	)

	prioridad = forms.ChoiceField(
		label='Prioridad',
		choices = prioridad_choices,
		widget=forms.Select(
			attrs={
				'id':"prioridad",
				'name':'prioridad_name',
				'class':'form-control',
			   }
		)
	)

	datarange = forms.CharField(
		label='Fecha de creación',
		widget=forms.TextInput(
			attrs={
				'id':"daterange",
				'name':'daterange_name',
				'class':'form-control',
				'autocomplete': 'off',
				'placeholder':'YYYY-MM-DD - YYYY-MM-DD',
				#'value':"2018-01-01 - 2021-01-01"
			}
		)
	)

	def __init__(self,*args, **kwargs):
		super(DashboardFormBanco, self).__init__(*args, **kwargs)

		self.fields['titulo'].required = False
		self.fields['tipo_innovacion'].required = False
		self.fields['prioridad'].required = False
		self.fields['datarange'].required = False
		self.fields['id_idea'].required = False

		#self.fields['frente'].required = False
		#self.fields['frente'].widget.attrs['id'] = "frente"
		#self.fields['frente'].label = "Frente"
		#self.fields['frente'].widget.attrs['class'] = "form-control select2-selection select2-selection--multiple"
		
class CustomWidget(forms.Textarea):
	template_name = 'widget.html'	
class FiltrosIdea(forms.ModelForm):

	# INNOVATION_TYPE=(
	# 	('','Ninguno'),
	# 	("INCREMENTAL","Incremental"),
	# 	("PROCESOS","Procesos"),
	# 	("PRODUCTO","Producto"),
	# )
 
	# creation_date_range = forms.DateTimeField(
	# 	input_formats=['%Y-%m-%d %H:%M'],
	# 		widget=forms.DateTimeInput(
	# 			attrs={
	# 				'class': 'form-control',
	# 				'id':'datetimepicker7'
	# 			}
	# 		)
	# 	)

	#Sobre escribimos el diseño de boleano a lista
	#is_active = forms.BooleanField(widget=forms.CheckboxInput, default=False)
 
	IS_ACTIVE_LIST=[
		('','Ninguno'),
		(True,"Si"),
		(False,"No"),
  	]
	
	
	is_active= forms.BooleanField(
		label="¿Activa?", 
		widget=forms.Select(
			choices=IS_ACTIVE_LIST,
			attrs={
				'class': 'form-control',
				'id':'is_active',
    			'name':'is_active_name'
			}
		)
  	)
 
	is_fastrack= forms.BooleanField(
		label="¿Es fastrack?", 
		widget=forms.Select(
			choices=IS_ACTIVE_LIST,
			attrs={
				'class': 'form-control',
				'id':'is_fastrack',
				'name':'is_fastrack_name'
			}
		)
	)
  
	#is_active = forms.TypedChoiceField(coerce=lambda x: x =='True', choices=((False, 'No'), (True, 'Yes')))

	class Meta:
		model = Idea
		fields = ['title','priority','innovation_type', 'innovation_estrategia','is_active','is_fastrack','collaborator',]#,'frente']
		widgets = {
			# 'actor':forms.Select(
			# 	attrs={
			# 		'class':'form-control',
			# 		'placeholder':'Ingrese la salida de la Regla',
			# 		'id':'actor_crear'
			# 	}
			# ),
	  
			'title':forms.TextInput(
				attrs={
					'class':'form-control',
					'placeholder':'Nombre Idea',
     				'name':'title_name',
					'id':'title'
				}
			),
			'priority':forms.Select(
				attrs={
					'class':'form-control',
					'name':'priority_name',
					'id':'priority'
				}
			),
			'innovation_type':forms.Select(
				attrs={
					'class':'form-control',
					'name':'innovation_type_name',
					'id':'innovation_type'
				}
			),
			'innovation_estrategia':forms.Select(
				attrs={
					'class':'form-control',
					'name':'innovation_estrategia_name',
					'id':'innovation_estrategia'
				}
			),
      
		}
  
	# Los campos personalizados van fuera de la clase Meta para se reconocidos
	creation_date_range=forms.CharField(
		required=False,
		label='Rango de Creación:',
		widget=forms.TextInput(
			attrs={
				'class':'form-control',
				'placeholder':'YYYY-MM-DD - YYYY-MM-DD',
				'id':'rango_input',
				'name': 'daterange',
				'autocomplete':'off',
				'style':"cursor:pointer; background-color: #FFFFFF",
			}
		)
	)
	#extra_field = forms.CharField(label='Name of Institution', initial="harvard")


	def __init__(self, *args, **kwargs):
		"""Está función es el constructor en donde alimentamos el campo de colaborador por un query y establecer las propiedades del formulario
  
		"""
		super().__init__(*args, **kwargs)


		try:
			#Se recorre para quitar la tupla
			for collaborator in args:
				print(type(collaborator))
				#print("key 12 ", collaborator.getlist('collaborator'))
				#https://programmerclick.com/article/10101808992/
				dato = collaborator.getlist('collaborator') #así se accede a un QueryDict 
			qs = User.objects.filter(pk__in=dato)
			#frentes = Frente.objects.all()#filter(pk__in=frente)
			#print("qs ",qs)
		except Exception as error:
			print("error ",error)
			qs = User.objects.none()
			#frentes = Frente.objects.all()#filter(pk__in=frente)
   
		self.fields['collaborator'].queryset = qs
  
		#Los campos ManyToMany no se recomienda sobre escribirlos en el Meta para eso se hace en el __init__

		self.fields['collaborator'].required = False
		self.fields['collaborator'].widget.attrs['id'] = "collaborator_id"
		#self.fields['collaborator'].widget.attrs['name'] = "collaborator_name" #no funciona
		self.fields['collaborator'].widget.attrs['class'] = "form-control"

		#self.fields['frente'].queryset = frentes
		#self.fields['frente'].required = False
		#self.fields['frente'].widget.attrs['id'] = "frente"
		#self.fields['frente'].label = "Frente"
		#self.fields['frente'].widget.attrs['class'] = "form-control select2-selection select2-selection--multiple"

		#Inhabilitamos lo obligatorio para poder buscar en todos los campos
		self.fields['title'].required = False
		self.fields['priority'].required = False
		self.fields['innovation_type'].required = False
		self.fields['innovation_type'].required = False
		self.fields['is_active'].required = False
		self.fields['is_fastrack'].required = False


class ExternalIdeaFeedbackForm(forms.ModelForm):
	class Meta:
		model = ExternalIdea
		fields=['feedback']

		widgets = {
			'feedback':forms.TextInput(
				attrs={
					'class':'form-control',
					'placeholder':'Cuentanos tus comentarios de esta idea',
					'id':'feedback_crear' }),
			}



class ExternalIdeaRevisionForm(forms.ModelForm):
	class Meta:
		model = ExternalIdea
		fields=['revision']

		widgets = {
			'revision':forms.TextInput(
				attrs={
					'class':'form-control',
					'placeholder':'Ayudanos a complementar tu idea',
					'id':'revision_crear',
					  'rows':4, 
					'cols':15,}),

					
			}
		
		