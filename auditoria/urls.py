from django.urls import path
from . import views

urlpatterns = [
    path('auditoria/', views.vista_auditoria, name='vista_auditoria'),
    # path('logs/<int:log_id>/', views.detalle_log, name='detalle_log'), # Opcional
]