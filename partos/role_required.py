from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def role_required(allowed_roles=[]):
    """
    Decorador para restringir acceso según rol.
    allowed_roles = lista de roles permitidos, ej: ['matrona', 'enfermero']
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Obtener rol del usuario; asumir que está en request.user.role
            # O en sesión: request.session.get('rol')
            rol = getattr(request.user, 'role', None) or request.session.get('rol', 'guest')
            
            if rol not in allowed_roles:
                messages.error(request, "Algo salió mal.")
                return redirect('inicio')  # Redirigir a dashboard o inicio
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
