from django.urls import path
from . import views

urlpatterns = [
    # Panel matrona: búsqueda de madre confirmada como inicio
    path('', views.buscar_madre_para_parto, name='inicio'),

    # Madre (solo SOME, proteger con decorador de rol en views)
    path('madre/ingreso/', views.ingreso_madre, name='ingreso_madre'),
    path('madre/guardar/', views.guardar_madre, name='guardar_madre'),
    path('madre/listado/', views.listado_madres, name='listado_madres'),
    path('madre/<int:pk>/', views.detalle_madre, name='detalle_madre'),
    path('madre/registrar/<int:pk>/', views.registrar_madre, name='registrar_madre'),

    # Matrona: Buscar madre confirmada para parto
    path('parto/buscar_madre/', views.buscar_madre_para_parto, name='buscar_madre_para_parto'),
    # Ingreso de parto requiere madre_id
    path('parto/ingreso/<int:madre_id>/', views.ingreso_parto, name='ingreso_parto'),
    path('parto/listado/', views.listado_partos, name='listado_partos'),
    path('parto/<int:pk>/', views.detalle_parto, name='detalle_parto'),
    path('parto/registrar/<int:pk>/', views.registrar_parto, name='registrar_parto'),

    # Recién Nacido: ingreso requiere parto_id
    path('rn/ingreso/<int:parto_id>/', views.ingreso_rn, name='ingreso_rn'),
    path('rn/listado/', views.listado_rn, name='listado_rn'),
    path('rn/<int:pk>/', views.detalle_rn, name='detalle_rn'),
    path('rn/registrar/<int:pk>/', views.registrar_rn, name='registrar_rn'),
    path('rn/editar/<int:pk>/', views.editar_rn, name='editar_rn'),
]
