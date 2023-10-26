from rest_framework import viewsets
from .serializers import PrizeSerializer,ActionSerializer,LeguasSerializer
from ..models import AssignedPrize,Action,UserLeguas
from apps.idea.api.api_rest import CustomPagination,ReadAuthenticatedViewSet

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 50

class CustomPaginationPrize(CustomPagination):
	page = DEFAULT_PAGE
	page_size = DEFAULT_PAGE_SIZE


class PrizeViewSet(ReadAuthenticatedViewSet):
	serializer_class = PrizeSerializer
	pagination_class = CustomPaginationPrize
	queryset = AssignedPrize.objects.all().prefetch_related('id_user').select_related('id_prize')

class ActionViewSet(ReadAuthenticatedViewSet):
	serializer_class = ActionSerializer
	pagination_class = CustomPaginationPrize
	queryset = Action.objects.all().prefetch_related('id_user').select_related('id_idea','id_activity')


class LeguasViewSet(ReadAuthenticatedViewSet):
	serializer_class = LeguasSerializer
	pagination_class = CustomPaginationPrize
	queryset = UserLeguas.objects.all().select_related('id_user')


