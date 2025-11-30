from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('graficos/', views.reportes_graficos, name='reportes_graficos'),
]