from django.urls import path
from . import views

urlpatterns = [
    path('panel_matrona/', views.panel_matrona, name='panel_matrona'),
    path('panel_supervisor/', views.panel_supervisor, name='panel_supervisor'),
    path('panel_auditoria/', views.panel_auditoria, name='panel_auditoria'),
    path('panel_some/', views.panel_some, name='panel_some'),
]
