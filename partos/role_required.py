from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def role_required(allowed_roles):
    """
    Decorador para restringir acceso según rol.
    allowed_roles = lista de roles permitidos, ej: ['Matrona', 'SOME', ...]
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required(login_url='login')
        def _wrapped_view(request, *args, **kwargs):
            rol = getattr(request.user, 'rol', None)
            rol_nombre = rol.nombre if rol else None
            if rol_nombre not in allowed_roles:
                messages.error(request, "No tienes permisos para acceder a esta sección.")
                return redirect('inicio')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
