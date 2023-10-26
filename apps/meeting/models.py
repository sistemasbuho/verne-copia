from email.policy import default
from django.db import models
from simple_history.models import HistoricalRecords
from apps.idea.models import Idea
from django.contrib.auth.models import User
from django.db.models.fields import URLField
from ckeditor_uploader.fields import  RichTextUploadingField



class Meeting(models.Model):
	name=models.CharField(max_length=50,verbose_name=u'Nombre Reunión')
	date=models.DateField(null=True,verbose_name=u'Fecha de creación')
	document_act=models.FileField(upload_to='document_meeting/', blank=True,null=True)
	place=models.CharField(max_length=50,verbose_name=u'Lugar')
	start_time=models.TimeField(null=True,verbose_name=u'Hora de Inicio')
	end_time=models.TimeField(null=True,verbose_name=u'Hora Fin')
	is_active=models.BooleanField(max_length=100, default=True, verbose_name=u'Está calificada')
	link_documentation=URLField(max_length=1500, verbose_name=u'Enlace a Documentación', null = True, blank=True, default="https://drive.google.com/")
	id_idea=models.ManyToManyField(Idea)
	user_comitte=models.ManyToManyField(User)
	history = HistoricalRecords()

	class Meta:
		verbose_name = "Reunión Comité"
		verbose_name_plural = "Reuniones Comité"

	def __str__(self):
		return self.name

class UserVotes(models.Model):
	STATE_PHASE=(
     
	("1","Avanza de fase"),
	("2","Se mantiene en fase"),
  	("3","Ideas en Stand By"), )
	STATE_PRIORITY=(
     
	("1","Sube de prioridad"),
 	("2","Baja de prioridad"),
    ("3","Se mantiene en prioridad"))
	
	vote=models.CharField(max_length=100, choices=STATE_PHASE,verbose_name=u'Voto de Fase')
	vote_priority=models.CharField(max_length=100, choices=STATE_PRIORITY,verbose_name=u'Voto de Prioridad')
	id_meeting=models.ForeignKey(Meeting,on_delete=models.SET_NULL,null = True)
	id_idea=models.ForeignKey(Idea,on_delete = models.SET_NULL,null = True, verbose_name=u'Miembro Comité',)
	id_user_comitte=models.ForeignKey(User,on_delete = models.SET_NULL,null = True)	
	is_evaluate=models.BooleanField(default=False,verbose_name=u'Está calificada')
	phase_actual=models.IntegerField(null=True,blank=True)
	message = models.CharField(max_length=500,verbose_name=u'Comentario' ,null=True,blank=True, default="Sin comentarios")
	pub_date=models.DateTimeField('date_published',auto_now=True)
	history = HistoricalRecords()
	def __str__(self):
		return "message: {0}".format(self.vote) 

	class Meta:
		verbose_name = "Voto Comité"
		verbose_name_plural = "Votos Comité"