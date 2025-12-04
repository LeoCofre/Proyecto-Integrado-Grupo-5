from django.shortcuts import render
from .models import Auditoria
from django.contrib.auth.decorators import login_required, user_passes_test
# Importar Paginator si la lista es muy grande

def es_administrador_o_auditor(user):
    # Función de ejemplo: ajusta esto a tu lógica de permisos (ej. grupo 'Auditores')
    return user.is_superuser or user.is_staff 


@login_required
@user_passes_test(es_administrador_o_auditor)
def vista_auditoria(request):
    # El ordenamiento descendente (-fecha_hora) está definido en models.py
    registros = Auditoria.objects.all() 
    
    context = {
        'registros_auditoria': registros # o registros_auditoria si usas paginación
    }
    
    return render(request, 'auditoria/auditoria.html', context)