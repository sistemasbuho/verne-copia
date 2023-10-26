from rest_framework import viewsets
from .serializers import ActivitySerializer
from rest_framework.permissions import IsAuthenticated
from django_filters  import rest_framework as filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from ..models import Activity

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
	#serializer_class = BasicSerializer
	permission_classes = (IsAuthenticated,)


class ActivityViewSet(ReadAuthenticatedViewSet):
	serializer_class = ActivitySerializer
	pagination_class = CustomPagination
	queryset = Activity.objects.all().prefetch_related('id_idea','id_user')
