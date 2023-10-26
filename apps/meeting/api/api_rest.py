from rest_framework import viewsets
from .serializers import *
from ..models import Meeting,UserVotes
from apps.idea.api.api_rest import CustomPagination,ReadAuthenticatedViewSet

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 50

class CustomPaginationMeeting(CustomPagination):
	page = DEFAULT_PAGE
	page_size = DEFAULT_PAGE_SIZE

class MeetingViewSet(ReadAuthenticatedViewSet):
	serializer_class = MeetingSerializer
	pagination_class = CustomPaginationMeeting
	queryset = Meeting.objects.prefetch_related('id_idea')


class UserVotesgViewSet(ReadAuthenticatedViewSet):
	serializer_class = UserVotesSerializer
	queryset = UserVotes.objects.select_related('id_idea','id_user_comitte','id_meeting')
	pagination_class = CustomPaginationMeeting