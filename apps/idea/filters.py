import django_filters
from django_filters import DateFilter, CharFilter,ModelChoiceFilter,BooleanFilter
from .models import Idea,Phase
from django.contrib.auth.models import User
from distutils.util import strtobool


class IdeaFilter(django_filters.FilterSet):

        
	PRIORITY_IDEA = (
		('','Ninguno'),
		("ALTA","Alta"),
		("MEDIA","Media"),
		("BAJA","Baja"),
	)

	INNOVATION_TYPE=(

		('','Ninguno'),
		("INCREMENTAL","Incremental"),
		("PROCESOS","Procesos"),
		("PRODUCTO","Producto"),)

	INNOVATION_ESTRATEGIA=(
		("Crecimiento de mercados","Crecimiento de mercados"),
		("Innovación","Innovación"),
		("Sostenibilidad","Sostenibilidad"),
		("Nuestra gente y cultura","Nuestra gente y cultura"),
		("Productividad y mejora continua","Productividad y mejora continua"),)

	is_active=BooleanFilter(field_name="is_active",lookup_expr='icontains')
	is_merge=BooleanFilter(field_name="is_merge",lookup_expr='icontains')
	is_fastrack=BooleanFilter(field_name="is_fastrack",lookup_expr='icontains')
	id_phase = ModelChoiceFilter(queryset=Phase.objects.all())
	collaborator = ModelChoiceFilter(queryset=User.objects.all())
	creation_date = DateFilter(field_name="creation_date",lookup_expr='gte')
	description = CharFilter(field_name="description",lookup_expr='icontains')
	title = CharFilter(field_name="title",lookup_expr='icontains')
	priority = django_filters.TypedChoiceFilter(choices=PRIORITY_IDEA,
                                            coerce=strtobool)
	innovation_type = django_filters.TypedChoiceFilter(choices=INNOVATION_TYPE,
                                            coerce=strtobool)
	innovation_estrategia = django_filters.TypedChoiceFilter(choices=INNOVATION_ESTRATEGIA,
                                            coerce=strtobool)


	class Meta:
		model = Idea
		fields=['creation_date', 'description', 'title', 'is_active', 'priority', 
		'innovation_type', 'innovation_estrategia', 'is_merge', 'is_fastrack', 'collaborator','id_phase']

	def __init__(self, data, *args, **kwargs):
		data = data.copy()
		data.setdefault('format', 'id')
		data.setdefault('order', '-added')
		super().__init__(data, *args, **kwargs)