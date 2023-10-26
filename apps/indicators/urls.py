from django.urls import path
from .views import *


urlpatterns = [
    
    path('indicadores/', IdeaAnual.as_view(), name='indicadores'),
    path('search_idea/', SearchIdeaAjax.as_view(), name = 'search_idea'),
    path('medidor/<int:pk>/', GraficaMedidorAjax.as_view(), name = 'medidor_grafica_ajax'),
    path('list_task/',ListTask.as_view(), name='list_task'), 
    path('indicator_table/',IndicatorTable.as_view(), name='indicator_table'), 

]