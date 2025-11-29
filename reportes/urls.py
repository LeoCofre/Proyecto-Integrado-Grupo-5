from django.urls import pathfrom . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('graficos/', views.reportes_graficos, name='reportes_graficos'),
    path('exportar/excel/', views.exportar_excel, name='exportar_excel'),
]