from django.urls import path
from . import views

urlpatterns = [
    # Madre
    path('madre/crear/', views.crear_madre, name='crear_madre'),
    path('madre/listado/', views.listado_madre, name='listado_madre'),
    
    # Parto
    path('parto/crear/', views.crear_parto, name='crear_parto'),
    path('parto/listado/', views.listado_parto, name='listado_parto'),
    
    # Recién Nacido
    path('rn/crear/', views.crear_rn, name='crear_rn'),
    path('rn/listado/', views.listado_rn, name='listado_rn'),
]
