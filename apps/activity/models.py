from django.db import models
from simple_history.models import HistoricalRecords
from apps.idea.models import Idea
from django.contrib.auth.models import User
from django.db.models.fields import URLField


class Task(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,verbose_name=u'Encargado',related_name='UsersActivity')
	title = models.CharField(max_length=200,verbose_name=u'Título')
	description = models.TextField(null=True, blank=True,verbose_name=u'Descripción')
	complete = models.BooleanField(default=False,verbose_name=u'Estado')
	created = models.DateTimeField(auto_now_add=True,verbose_name=u'Fecha creación')

	def __str__(self):
		return self.title

	class Meta:
		order_with_respect_to = 'user'
		verbose_name = "Tareas Actividad"
		verbose_name_plural = "Tareas Actividad"


class Activity(models.Model):

	tool=models.CharField(max_length=100, null=True, blank=True,verbose_name=u'Herramienta')
	annexed= models.FileField(upload_to='document_activity/', null=True, blank=True,verbose_name=u'Anexo actividad')
	description=models.TextField(null=True, blank=True,max_length=300,verbose_name=u'Descripción')
	name=models.CharField(max_length=50, verbose_name=u'Nombre Actividad')
	date=models.DateField( null=True, blank=True,verbose_name=u'Fecha de creación')
	score=models.IntegerField(null=True, blank=True,verbose_name=u'Leguas por actividad',default=0)
	redeemed_score=models.BooleanField(null=True, blank=True,default=False,verbose_name=u'¿Leguas canjeadas?')
	link_documentation=URLField(max_length=1500, verbose_name=u'Enlace a Documentación', null = True, blank=True, default="https://drive.google.com/")

	id_user=models.ManyToManyField(User,verbose_name=u'Participantes')
	id_idea=models.ManyToManyField(Idea,verbose_name=u'Idea a evaluar')
	task = models.ManyToManyField(Task,verbose_name=u'Tareas', blank=True)

	history = HistoricalRecords()

	def __str__(self):
		return self.name

	class Meta:
		permissions = (
			('admin_activity', 'admin_activity'),)
			
		verbose_name = "Actividad"
		verbose_name_plural = "Actividades"

