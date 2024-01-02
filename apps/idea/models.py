from unicodedata import name
from unittest.mock import DEFAULT
from urllib import request
from django.db import models
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User
from django.db.models.fields import URLField
from apps.users.models import Profile


# Para el disparador que asigna automáticamente al grupo Users
#------------------------------------------
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import Group

@receiver(models.signals.post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		instance.groups.add(Group.objects.get(name='Users'))
		instance.save()		   
#------------------------------------------


STATES=(
	("Aprobado","Aprobado"),
	("Rechazado","Rechazado"),
	("En revisión","En revisión"),
	("Por definir","Por definir"),)

PROPOSITOS=(
	("Sí","Sí"),
	("No","No"),)

class Area(models.Model):
	nombre=models.CharField(max_length=300,verbose_name=u'Descripción')
	history = HistoricalRecords()

	def __str__(self):
		return self.nombre
	
	class Meta:
		verbose_name = "Area"
		verbose_name_plural = "Areas"


class Beneficio(models.Model):
	nombre=models.CharField(max_length=300,verbose_name=u'Descripción')
	history = HistoricalRecords()

	def __str__(self):
		return self.nombre
	
	class Meta:
		verbose_name = "Beneficio"
		verbose_name_plural = "Beneficios"


class Frente(models.Model):
	nombre=models.CharField(max_length=300,verbose_name=u'Descripción')
	history = HistoricalRecords()

	def __str__(self):
		return self.nombre
	
	class Meta:
		verbose_name = "Frente"
		verbose_name_plural = "Frentes"

class Dimension(models.Model):
	nombre=models.CharField(max_length=300,verbose_name=u'Descripción')
	history = HistoricalRecords()

	def __str__(self):
		return self.nombre
	
	class Meta:
		verbose_name = "Dimension"
		verbose_name_plural = "Dimensiones"


class Objective(models.Model):
	nombre=models.CharField(max_length=300,verbose_name=u'Descripción')
	year=models.IntegerField(verbose_name=u'Año')
	history = HistoricalRecords()

	def __str__(self):
		return self.nombre
	
	class Meta:
		verbose_name = "Objectivo"
		verbose_name_plural = "Objectivos"

 
class ExternalIdea(models.Model):
	creation_date=models.DateField(auto_now_add=True,verbose_name=u'Fecha de creación')#auto_now_add=True,
	description=models.TextField('Descripción',max_length=5000)
	solucion=models.TextField('Solución',max_length=5000)
	title=models.CharField('Título',max_length=150)
	state=models.CharField(max_length=20, choices=STATES, default="Por definir", blank=True,null=True,verbose_name=u'Estado')
	proposito=models.CharField(max_length=20, choices=PROPOSITOS, default="Sí", blank=True,null=True,verbose_name=u'Proposito')
	external_name = models.CharField('Nombre externo',max_length=150)
	external_email= models.CharField('Email externo',max_length=150)
	conditions=models.BooleanField(default=True,verbose_name=u'Términos y condiciones' ,null=False, blank=False)
	feedback=models.TextField('Comentarios',max_length=5000, default=" ")
	gerencia=models.ForeignKey(Area,on_delete=models.CASCADE, verbose_name=u'Gerencia', blank=True,null=True)
	subregion = models.ForeignKey(Beneficio,on_delete=models.CASCADE,verbose_name=u'Subregión', blank=True,null=True)
	frente=models.ForeignKey(Frente,on_delete=models.CASCADE,verbose_name=u'Frente', blank=True,null=True)
	dimension = models.ForeignKey(Dimension,on_delete=models.CASCADE,verbose_name=u'Dimensión', blank=True,null=True)
	pilar = models.ForeignKey(Objective,on_delete=models.CASCADE,verbose_name=u'Objetivos', blank=True,null=True)
	documento=models.IntegerField(verbose_name=u'Cedula', default=0, blank=True,null=True)
	revision=models.TextField('Revision del problema',max_length=5000, blank=True,null=True)

	#Add more fields here
 
	class Meta:
		verbose_name = "Ideas Externas"
		verbose_name_plural = "Ideas Externas"
  
  
class PriceScore (models.Model):
	price=models.IntegerField(verbose_name=u'Valor Legua', default=0)

	class Meta:
		verbose_name = "Valor Legua"
		verbose_name_plural = "Valor Legua"





class QuestionPhase(models.Model):
	name=models.CharField(null=False ,blank=False, max_length=200,verbose_name=u'Pregunta')
	date=models.DateField(null=True,auto_now_add=True,verbose_name=u'Fecha')
	history = HistoricalRecords()

	def __str__(self):
		return self.name
	
	class Meta:
		verbose_name = "Pregunta Pain"
		verbose_name_plural = "Preguntas Pain"


class Phase(models.Model):
	name=models.CharField(max_length=50,verbose_name=u'Nombre Fase')
	history = HistoricalRecords()

	def __str__(self):
		return self.name
	
	class Meta:
		verbose_name = "Fase"
		verbose_name_plural = "Fases"


class Task(models.Model):

	STATES=(
	("Por hacer","Por hacer"),
	("En ejecución","En ejecución"),
	("Completado","Completado"),)


	
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,verbose_name=u'Encargado')
	title = models.CharField(max_length=200,verbose_name=u'Título')
	description = models.TextField(null=True, blank=True,verbose_name=u'Notas')
	complete = models.BooleanField(default=False,verbose_name=u'Estado')
	created = models.DateTimeField(auto_now_add=True,verbose_name=u'Fecha creación')

	def __str__(self):
		return self.title

	class Meta:
		order_with_respect_to = 'user'
		verbose_name = "Tareas por fase"
		verbose_name_plural = "Tareas por fase"


class TaskByIdea(models.Model):

	STATES=(
	("Por hacer","Por hacer"),
	("En ejecución","En ejecución"),
	("Completado","Completado"),)
	user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='UsersIdea', null=True, blank=True,verbose_name=u'Encargado')
	title = models.CharField(max_length=200,verbose_name=u'Título')
	description = models.TextField(null=True, blank=True,verbose_name=u'Notas')
	#complete = models.BooleanField(default=False,verbose_name=u'Estado')
	complete=models.CharField(max_length=20, choices=STATES, default="Por hacer", blank=True,null=True,verbose_name=u'Estado')

	created = models.DateTimeField(auto_now_add=True,verbose_name=u'Fecha creación')

	def __str__(self):
		return self.title

	class Meta:
		order_with_respect_to = 'user'
		verbose_name = "Tareas por Idea"
		verbose_name_plural = "Tareas por Idea"


class Idea(models.Model):

	INNOVATION_TYPE=(
		("Incremental","Incremental"),
		("Producto","Producto"),
		("Procesos","Procesos"))

	INNOVATION_PRIORITY=(
		("ALTA","Alta"),
		("MEDIA","Media"),
		("BAJA","Baja"),)
	
	INNOVATION_ESTRATEGIA=(
		("Crecimiento de mercados","Crecimiento de mercados"),
		("Innovación","Innovación"),
		("Sostenibilidad","Sostenibilidad"),
		("Nuestra gente y cultura","Nuestra gente y cultura"),
		("Productividad y mejora continua","Productividad y mejora continua"),)
	

	def custom_upload_to_documento(instance, filename):
		old_instance = Idea.objects.get(pk=instance.pk)
		old_instance.primer_documento.delete()
		return 'home/' + filename
	
	def custom_upload_to_documento2(instance, filename):
		old_instance = Idea.objects.get(pk=instance.pk)
		old_instance.segundo_documento.delete()
		return 'home/' + filename
	
	def custom_upload_to_documento3(instance, filename):
		old_instance = Idea.objects.get(pk=instance.pk)
		old_instance.tercer_documento.delete()
		return 'home/' + filename

	creation_date=models.DateField(auto_now_add=True,verbose_name=u'Fecha de creación')#auto_now_add=True,
	description=models.TextField('Descripción de problema',max_length=5000, blank=True,null=True)
	title=models.CharField('Título',max_length=150, blank=True,null=True)
	is_active=models.BooleanField(default=True,verbose_name=u'¿Está activa?')
	priority=models.CharField(max_length=20, choices=INNOVATION_PRIORITY, blank=True,null=True,verbose_name=u'Prioridad')
	innovation_type=models.CharField(max_length=20, choices=INNOVATION_TYPE, blank=True,null=True,verbose_name=u'¿En qué etapa se encuentra ia idea?')
	
	innovation_estrategia=models.CharField(max_length=40, choices=INNOVATION_ESTRATEGIA, blank=True,null=True,verbose_name=u'¿A que pilar estratégico le apunta la idea?')
	
	is_merge=models.BooleanField(default=False,verbose_name=u'¿Es merge?',blank=True,null=True)
	is_fastrack=models.BooleanField(default=False,verbose_name=u'¿Es fastrack?',blank=True,null=True)
	current_phase=models.IntegerField(null=True, blank=True,verbose_name=u'Fase Actual')
	conditions=models.BooleanField(default=True,verbose_name=u'Términos y condiciones' , blank=True,null=True)
	link_documentation=URLField(max_length=1500, verbose_name=u'Enlace a Documentación', null = True, blank=True, default=" https://drive.google.com/")
	descripcion_beneficio=models.TextField('Describe el beneficio',max_length=5000, default=' ',null=True, blank=True)
	asigned=models.ForeignKey(User,on_delete=models.CASCADE,related_name="asigned",verbose_name=u'Encargado', default="", null=True, blank=True)

	gain=models.FloatField(verbose_name=u'Beneficio',null=True, blank=True, default=0)
	investment =models.FloatField(verbose_name=u'Inversión adicional',null=True, blank=True, default=0)
	roi =models.FloatField(verbose_name=u'ROI',null=True, blank=True, default=0)
	score_idea=models.IntegerField(null=True, blank=True,verbose_name=u'Leguas invertidas',default=0)
	price_score=models.IntegerField(null=True, blank=True,verbose_name=u'Precio total leguas',default=0)
	total_investment = models.FloatField(verbose_name=u'Inversión total',null=True, blank=True, default=0)

	id_merge=models.ManyToManyField('self',  blank=True, related_name='evaluations')	# Para el merge entre dos ideas la tabla idea se autollama
	state=models.CharField(max_length=20, choices=STATES, default="Sí", blank=True,null=True,verbose_name=u'Proposito')


	id_question=models.ManyToManyField(QuestionPhase, through='IdeaQuestionPhase',
		through_fields=('id_idea', 'id_question'),)
	id_phase=models.ManyToManyField(Phase, through='Phase_Date',
		through_fields=('id_idea', 'id_phase'),default=1)
	task = models.ManyToManyField(TaskByIdea,verbose_name=u'Tareas', blank=True)

	collaborator=models.ManyToManyField(User,related_name="collaborator",verbose_name=u'Autores', blank=True)

	idea_externa = models.ForeignKey(ExternalIdea,on_delete=models.CASCADE,verbose_name=u'Idea Externa', blank=True,null=True)
	area=models.ForeignKey(Area,on_delete=models.CASCADE, verbose_name=u'Área', blank=True,null=True)
	beneficio=models.ForeignKey(Beneficio,on_delete=models.CASCADE, verbose_name=u'Beneficio', blank=True,null=True)
	feedback=models.TextField('Observaciones',max_length=5000, null=True, blank=True, default=" ")
	#subregion = models.ForeignKey(Subregion,on_delete=models.CASCADE,verbose_name=u'Subregión', blank=True,null=True)
	#frente=models.ForeignKey(Frente,on_delete=models.CASCADE,verbose_name=u'Frente de Innovación', blank=True,null=True)
	#dimension = models.ForeignKey(Dimension,on_delete=models.CASCADE,verbose_name=u'Dimensión', blank=True,null=True)
	id_objective = models.ForeignKey(Objective,on_delete=models.CASCADE,verbose_name=u'Objetivos', blank=True,null=True)
	#documento=models.IntegerField(verbose_name=u'Cedula', default=0, blank=True,null=True)
	#external_name = models.CharField('Nombre externo',max_length=150, blank=True,null=True)
	#external_email= models.CharField('Email externo',max_length=150, blank=True,null=True)
	#primer_documento=models.FileField(upload_to='home', blank=True,null=True,verbose_name=u'Documentación de Evolución 1')
	#segundo_documento=models.FileField(upload_to='home', blank=True,null=True,verbose_name=u'Documentación de Evolución 2')
	#tercer_documento=models.FileField(upload_to='home', blank=True,null=True,verbose_name=u'Documentación de Evolución 3')
	#region = models.ManyToManyField(Subregion,related_name='region',verbose_name=u'Regiones de aplicación de la idea', blank=True)
	#solucion=models.TextField('Solución del problema',max_length=5000)
	#revision=models.TextField('Revision del problema',max_length=5000, blank=True,null=True)

	history = HistoricalRecords()	
	
	def __str__(self):
		return str(self.title)

	class Meta:
		permissions = (('view_dashboard', 'view_dashboard'),
			
			)
		
		verbose_name = "Idea"
		verbose_name_plural = "Ideas"

	#def save(self, *args, **kwargs):		
	#	print('self.primer_documento',self.primer_documento)
	#	print('kw	',kwargs)
	#	print('ar	',args)
	#	super(Idea, self).save(*args, **kwargs)




class Phase_Date(models.Model):
	phase_date=models.DateField(auto_now_add=True,null=True,verbose_name=u'Fecha Fase inicial')#auto_now_add=True,
	phase_date_previous=models.DateField(blank=True,null=True,verbose_name=u'Fecha fase previa final')#auto_now_add=True,
	id_phase=models.ForeignKey(Phase, related_name = 'phase_question',on_delete = models.SET_NULL , null = True )
	id_idea=models.ForeignKey(Idea,related_name = 'phase_question',on_delete = models . SET_NULL , null = True )
	document=models.FileField(upload_to='documents_idea', blank=True,null=True,verbose_name=u'Documento Fase')
	is_active=models.BooleanField(default=False,verbose_name=u'¿Está finalizada la fase?')
	days_total=models.IntegerField(null=True, blank=True,verbose_name=u'Días en la fase')
	link_documentation=URLField(max_length=1500, verbose_name=u'Enlace a Documentación', null = True, blank=True, default=" ")
	feedback=models.TextField('Comentarios',max_length=5000, null=True, blank=True, default=" ")
	description=models.TextField('Descripción',max_length=5000, default=" ", blank=True,null=True)
	task = models.ManyToManyField(Task,verbose_name=u'Tareas', blank=True)

	history = HistoricalRecords()

	def __str__(self):
		return 'Fase '+str(self.id_phase) 
	
	class Meta:
		verbose_name = "Fecha Fase"
		verbose_name_plural = " Fechas Fases"


class IdeaQuestionPhase(models.Model):
	id_question=models.ForeignKey(QuestionPhase,on_delete = models.SET_NULL , null = True)
	id_idea=models.ForeignKey(Idea,on_delete = models.SET_NULL , null = True)
	question_date=models.DateField(auto_now_add=True,blank=True, null=True,verbose_name=u'Fecha preguntas')
	is_state_question=models.BooleanField(default=True)
	history = HistoricalRecords()

	class Meta:
		verbose_name = "Pregunta Pain Idea"
		verbose_name_plural = "Preguntas Pain Ideas"


