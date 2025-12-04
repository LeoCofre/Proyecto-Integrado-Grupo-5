from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from .models import Auditoria 

'''
# ==============================================================================
# LÓGICA DE PERMISOS: Simulación de la función de verificación de Rol
# ==============================================================================

# NOTA: Esta función DEBE ser creada en la app 'login' o 'utils' 
# y debe verificar si el Rol del usuario tiene el permiso 'puede_consultar_auditoria'.
def verificar_permiso_auditoria(user):
    """
    Verifica si el rol del usuario tiene permiso para consultar la auditoría.
    Asume que user.rol es un objeto del modelo Rol de la app 'login'.
    """
    if user.is_authenticated and hasattr(user, 'rol'):
        # Verifica el campo booleano 'puede_consultar_auditoria' del objeto Rol
        return user.rol.puede_consultar_auditoria
    return False
'''

# ==============================================================================
# VISTA PRINCIPAL DE AUDITORÍA (HU-05)
# ==============================================================================

@login_required 
# 1. Fuerza al usuario a estar autenticado (Punto B)
def vista_auditoria(request):
    """
    Muestra la lista de registros de Auditoría, restringido por Rol.
    """
    
    # 2. VERIFICACIÓN DE PERMISOS (Punto A y C - RBAC)
    if not verificar_permiso_auditoria(request.user):   #lo llama desde la funcion q debe estar en login o utils
        # Si no tiene permiso, lo redirige o muestra un error 
        
        messages.error(request, "Acceso denegado. Su perfil no tiene permiso para consultar la pista de auditoría (HU-05).")
        
        # Opcional: Registrar intento de acceso no autorizado en el log de Auditoria:
        log_acceso_denegado(request.user, request.META.get('REMOTE_ADDR'))
        
        return redirect('index') # Redirige a la página principal u otra según convenga.
    
    # 3. CONSULTA DE DATOS
    # Solo los usuarios con permiso pueden ver todos los logs.
    # Usamos .select_related('usuario') para obtener los datos del usuario (y su rol) 
    # en una sola consulta, optimizando la carga del template.
    logs = Auditoria.objects.all().select_related('usuario').order_by('-fecha_hora')
    
    context = {
        'logs': logs,
    }
    
    # para renderizar el template con los logs
    return render(request, 'auditoria/auditoria.html', context)

'''
Pasos a Seguir para la Implementación:
Asegurar la Referencia a Usuario:
Confirma que el modelo Usuario en la app login está configurado como AUTH_USER_MODEL en settings.py.
Definir verificar_permiso_auditoria:
Esta función simulada (verificar_permiso_auditoria) debe ser implementada en la app login para que pueda acceder 
al campo puede_consultar_auditoria del Rol del usuario.
'''