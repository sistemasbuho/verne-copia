
from django.urls import path, include
from .views import *

urlpatterns = [
    
    #Meeting
    path('register/',RegisterMeeting.as_view(), name='register'), 
	path('visualize/', watchMeeting.as_view(), name='visualize'),
	path('visualize/register_comment/<int:pk>/<int:id_idea>/', registerComment, name='register_comment'),
    path('detail_meeting/<int:id_reu>/comments_list/<int:id_idea>/', comments_list, name = 'comments_list'),
    path('visualize/detail_meeting/<int:pk>/', detailMeeting, name='detail_meeting'),
    path('visualize/detail_meeting/upload/<int:pk>/',BasicUploadView, name='upload'),
    path('visualize/detail_meeting/close_meeting/<int:pk>/',closeMeeting, name='close'),
    path('buscar_idea/', IdeaAjaxMeeting.as_view(), name='buscar_idea'),
    path('buscar_usuario/', UserAjaxMeeting.as_view(), name='buscar_usuario'),
    path('update/<int:id>', UpdateMeeting, name='update'),

	#Generar pdf
	path('ticket/<int:pk>/', MeetingGeneratorPdf.as_view(), name='ticket'),

]


