from rest_framework import serializers
from ..models import *
from django.contrib.auth.models import User,Group
from django.utils.timezone import now


class BasicSerializer(serializers.ModelSerializer):
	class Meta:
		model = QuestionPhase
		fields ='__all__'
		read_only = True

class ObjetiveSerializer(serializers.ModelSerializer):
	class Meta:
		model = Objective
		fields = ('description','year')
		read_only = True

class GroupSerializer(serializers.ModelSerializer):    
	class Meta:
		model = Group
		fields = ('name',)
		read_only = True


class PhaseSerializer(serializers.ModelSerializer):    
	class Meta:
		model = Phase
		fields = ('name',)
		read_only = True


class PhaseDateSerializer(serializers.ModelSerializer):    
	
	dias_por_fase = serializers.SerializerMethodField()

	def get_dias_por_fase(self, obj):
		if obj.phase_date_previous:
			return (  obj.phase_date_previous - obj.phase_date).days
		else:
			return ('-1')

	class Meta:
		model = Phase_Date
		fields = ('phase_date','phase_date_previous','id_idea','id_phase','dias_por_fase')
		read_only = True

class UserSerializers(BasicSerializer):
	dias_ingreso = serializers.SerializerMethodField()
	groups = GroupSerializer(many=True)
	full_name = serializers.SerializerMethodField()

	def get_full_name(self, obj):
		if obj.first_name:
			return f'{obj.first_name} {obj.last_name}'
		else:
			return "Sin Nombre completo"

	def get_dias_ingreso(self, obj):
		return (now() - obj.date_joined).days
	
	#guia 
	#http://ses4j.github.io/2015/11/23/optimizing-slow-django-rest-framework-performance/

	class Meta:
		model = User
		fields = 'dias_ingreso','full_name','email','is_active','date_joined','groups'


class IdeaSerializer(serializers.ModelSerializer):
	id_merge = serializers.StringRelatedField(read_only=True, many=True)
	id_objective = ObjetiveSerializer(many=True)
	id_phase = serializers.StringRelatedField(read_only=True,many=True)
	owner_idea = serializers.StringRelatedField(read_only=True)
	collaborator = serializers.StringRelatedField(read_only=True,many=True)

	class Meta:
		model = Idea
		fields = 'id','id_merge','id_objective','id_phase','owner_idea','collaborator','creation_date','description','title','is_active','priority','innovation_type', 'innovation_estrategia','is_merge','is_fastrack','feedback','score_idea','current_phase','conditions'

