from django.urls import path
from . import views

urlpatterns = [
    # Inicio
    path('', views.inicio, name='inicio'),
    
    # Madre
    path('madre/ingreso/', views.ingreso_madre, name='ingreso_madre'),
    path('madre/guardar/', views.guardar_madre, name='guardar_madre'),
    path('madre/listado/', views.listado_madres, name='listado_madres'),
    path('madre/<int:pk>/', views.detalle_madre, name='detalle_madre'),
    path('madre/registrar/<int:pk>/', views.registrar_madre, name='registrar_madre'),
    
    # Parto
    path('parto/ingreso/', views.ingreso_parto, name='ingreso_parto'),
    path('parto/listado/', views.listado_partos, name='listado_partos'),
    path('parto/<int:pk>/', views.detalle_parto, name='detalle_parto'),
    path('parto/registrar/<int:pk>/', views.registrar_parto, name='registrar_parto'),
    
    # Recién Nacido
    path('rn/ingreso/', views.ingreso_rn, name='ingreso_rn'),
    path('rn/listado/', views.listado_rn, name='listado_rn'),
    path('rn/<int:pk>/', views.detalle_rn, name='detalle_rn'),
    path('rn/registrar/<int:pk>/', views.registrar_rn, name='registrar_rn'),
    path('rn/editar/<int:pk>/', views.editar_rn, name='editar_rn'),
]
