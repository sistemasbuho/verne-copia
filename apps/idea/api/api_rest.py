from rest_framework import viewsets
from .serializers import BasicSerializer,UserSerializers,IdeaSerializer,PhaseDateSerializer
from ..models import Objective,Idea,Phase,Phase_Date
from django.contrib.auth.models import User,Group
from rest_framework.permissions import IsAuthenticated
from django_filters  import rest_framework as filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models import Prefetch

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 100


class CustomPagination(PageNumberPagination):
	page = DEFAULT_PAGE
	page_size = DEFAULT_PAGE_SIZE
	page_size_query_param = 'page_size'

	def get_paginated_response(self, data):
		return Response({
			'links': {
				'next': self.get_next_link(),
				'previous': self.get_previous_link()
			},
			'total_registers': self.page.paginator.count,
			'total_pages': self.page.paginator.num_pages,
			'page_current': int(self.request.GET.get('page', DEFAULT_PAGE)), # can not set default = self.page
			'page_size': int(self.request.GET.get('page_size', self.page_size)),
			'results': data,
		})


class ReadAuthenticatedViewSet(viewsets.ReadOnlyModelViewSet):
	serializer_class = BasicSerializer
	permission_classes = (IsAuthenticated,)


class UserViewSet(ReadAuthenticatedViewSet):
	serializer_class = UserSerializers
	pagination_class = CustomPagination
	
	def get_queryset(self):
		queryset = User.objects.prefetch_related('groups')
		return queryset

	def dispatch(self, *args, **kwargs):
		response = super().dispatch(*args, **kwargs)

		# from django.db import connection
		# print('# of Queries: {}'.format(len(connection.queries)))
		return response


class IdeaViewSet(ReadAuthenticatedViewSet):
	serializer_class = IdeaSerializer
	pagination_class = CustomPagination

	def get_queryset(self):
		queryset = Idea.objects.all().prefetch_related('id_objective','id_phase','collaborator','id_merge').select_related('owner_idea')
		return queryset 
	

class PhaseViewSet(ReadAuthenticatedViewSet):
	serializer_class = PhaseDateSerializer
	pagination_class = CustomPagination

	def get_queryset(self):
		queryset = Phase_Date.objects.all().prefetch_related('id_idea','id_phase').select_related('id_idea')
		return queryset 