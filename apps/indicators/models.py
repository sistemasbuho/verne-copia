from django.db import models
from django.db.models.fields import URLField

from apps.activity.models import Activity
from apps.idea.models import Idea
from apps.prize.models import Action
from django.contrib.auth.models import User



class Indicators(models.Model):
	link_template_power_bi=URLField(max_length=1500, verbose_name=u'Link Plantilla Power BI', unique = True, default="https://app.powerbi.com/view?r=eyJrIjoiZDQwZmMwYTYtMWIwMC00MGQ0LWJiNzgtOWE5NWE5YTgxNjlmIiwidCI6IjVlNmY0NzE0LTk4YmQtNGRhMS1hOGY1LTNjYTQ1OWVhYmRjOSIsImMiOjR9")
	
	def __str__(self):
		return self.link_template_power_bi
		
	class Meta:
		verbose_name = "Indicador"
		verbose_name_plural = "Indicadores"



# usuario:{
# 	nombre:"Camilo",
# 	estado: True,
# 	participaciones:{
# 		tipo: "Actividad"
# 		Fecha: 23/10/2021
# 		Titulo: "Test de creatividad"
		
# 	},
# 	total_participaciones usuario: 1
# }, 
# total_participaciones_equipo : 10