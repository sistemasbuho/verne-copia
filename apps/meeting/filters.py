import django_filters
from django_filters import DateFilter, CharFilter,ModelChoiceFilter,TimeFilter
from apps.meeting.models import Meeting
from apps.idea.models import Idea

from django import forms
from django.forms import ModelForm
from distutils.util import strtobool


class MeetingFilter(django_filters.FilterSet):

	TRUE_FALSE_CHOICES = (
		('','Ninguno'),
		(True, 'Activo'),
		(False, 'Completado')
	)

	id_idea = ModelChoiceFilter(queryset=Idea.objects.all())
	date = DateFilter(field_name="date",lookup_expr='gte')
	start_time=TimeFilter(field_name="start_time",lookup_expr='gte')
	name = CharFilter(field_name="name",lookup_expr='icontains')
	place = CharFilter(field_name="place",lookup_expr='icontains')
	is_active = django_filters.TypedChoiceFilter(choices=TRUE_FALSE_CHOICES,
                                            coerce=strtobool)



	class Meta:
		model = Meeting
		#fields = '__all__' #para traer todos los campos
		#exclude = ['proyecto','finished']
		fields=['name','date','place','is_active','id_idea' ,'place','start_time']

