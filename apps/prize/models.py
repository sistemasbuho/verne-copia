from django.db import models
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User
from apps.idea.models import Idea
from apps.activity.models import Activity
from apps.prize.validators import validar_peso_maximo


class Legua(models.Model):
	price_legua= models.IntegerField(verbose_name=u'Precio de cada Legua')

	def __str__(self):
		return self.price_legua
		
	class Meta:
		verbose_name = "Precio Legua"
		verbose_name_plural = "Precio Legua"


def custom_upload_to(instance, filename):
    #old_instance = Prize.objects.get(pk=instance.pk)
    #old_instance.image.delete()
    return 'prizes/' + filename

class Prize(models.Model):
	name = models.TextField(verbose_name=u'Nombre premio')
	score= models.IntegerField(verbose_name=u'Leguas por premio')
	image=models.ImageField(null=True, blank=True, verbose_name=u'Imagen premio',upload_to=custom_upload_to)
	history = HistoricalRecords()

	def __str__(self):
		return self.name
	
	class Meta:
		permissions = (
			('rol_user_view', 'rol_user_view'),
			('rol_admin_view', 'rol_admin_view'),
			)
		verbose_name = "Premio"
		verbose_name_plural = "Premios"


class AssignedPrize(models.Model):
	date=models.DateField(auto_now_add=True,)
	id_user=models.ManyToManyField(User)
	id_prize=models.ForeignKey(Prize,on_delete = models.CASCADE)
	history = HistoricalRecords()



	class Meta:
		verbose_name = "Premio redimido"
		verbose_name_plural = "Premios redimidos"

class Action(models.Model):
	date=models.DateField()
	name=models.CharField(max_length=1000,verbose_name=u'Acción')
	description=models.CharField(max_length=2000,verbose_name=u'Descripción',null=True, blank=True)
	score=models.IntegerField(verbose_name=u'Leguas por acción')
	id_idea=models.ForeignKey(Idea,on_delete = models.CASCADE,blank=True, null = True)
	id_activity=models.ForeignKey(Activity,on_delete = models.CASCADE,blank=True, null = True)
	id_user=models.ManyToManyField(User)
	date_asigned=models.DateField(auto_now_add=True, null=True)

	history = HistoricalRecords()

	def __str__(self):
		return self.name
	
	class Meta:
		verbose_name = "Logro"
		verbose_name_plural = "Logros"


class UserLeguas(models.Model):
	NAME_CATEGORY=(
	("1","Innovation Team"),
	("2","Aprendiz"),
	("3","Explorador"),
	("4","Gurú"), )
	quantity=models.IntegerField(blank=True, null=True,verbose_name=u'Leguas', default=0)
	category=models.CharField(max_length=100, choices=NAME_CATEGORY,default="1",verbose_name=u'Categoría')
	id_user=models.ForeignKey(User,on_delete = models.CASCADE)
	inscription_club=models.BooleanField(default=False,verbose_name=u'Inscrito en Club Verne')

	class Meta:
		verbose_name = "Leguas del usuario"
		verbose_name_plural = "Leguas de los usuarios"