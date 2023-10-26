from django.urls import path , re_path, include
from .views import *


urlpatterns = [

	# Módulo Leguas
	path('score_user_register/',ScoreUser.as_view(), name='score_user_register'),
	path('visualize/user/',visualizeUser.as_view(),name='visualize_user'),
	path('visualize/user/details_score/<int:id_user>/',detailsScoreUser, name='details_score'),
	path('visualize/user/delete_action/<int:pk>/',deleteAction, name='delete_action'),
	path('visualize/user/inactive_user/<int:pk>/',inactiveUser, name='inactive_user'),
	path('visualize/user/club/<int:pk>/',InscriptionClub, name='club'),
	path('buscar_idea/', IdeaAjaxScore.as_view(), name='buscar_idea'),
    path('buscar_usuario/', UserAjaxScore.as_view(), name='buscar_usuario'),
	
	
	# Módulo premios
	path('register_prize/', AssignedPrizeAjax.as_view(),name='register_prize'),
	path('visualize/prize',visualizePrize.as_view(),name='visualize_prize'),
	path('visualize/user/delete_prize/<int:pk>/',deletePrize, name='delete_prize'),
 
	path('save_prize/', PremioRedimido, name='save_prize'),


 ]