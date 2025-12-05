from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CrearUsuarioForm, LoginForm
from .models import Usuario

# --- VISTA 1: CREAR USUARIO (Solo para Admin TI) ---
def crear_usuario_view(request):
    if request.method == 'POST':
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            rut = form.cleaned_data['rut']
            rol = form.cleaned_data['rol']
            password_plana = form.cleaned_data['password']
            try:
                nuevo_usuario = Usuario(
                    nombre=nombre,
                    rut=rut,
                    rol=rol,
                    is_active=True
                )
                nuevo_usuario.set_password(password_plana)
                nuevo_usuario.save()
                messages.success(request, f'Usuario {nombre} creado correctamente.')
                return redirect('crear_usuario')
            except Exception as e:
                messages.error(request, f"Error al guardar: {str(e)}")
        else:
            messages.error(request, f"Errores del formulario: {form.errors}")
    else:
        form = CrearUsuarioForm()

    return render(request, 'login/crear_usuario.html', {'form': form})

# --- VISTA 2: LOGIN (Inicio de Sesión) ---
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            rut = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=rut, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    rol = user.rol.nombre if user.rol else 'guest'
                    if rol == 'Administrador TI':
                        return redirect('crear_usuario')
                    elif rol in ['Matrona']:
                        return redirect('panel_matrona')
                    elif rol == 'Supervisor':
                        return redirect('panel_supervisor')
                    elif rol == 'Auditor Interno':
                        return redirect('panel_auditoria')
                    elif rol == 'SOME':
                        return redirect('panel_some')
                    else:
                        return redirect('panel_matrona')
                else:
                    messages.error(request, "Tu cuenta está desactivada.")
            else:
                messages.error(request, "RUT o contraseña incorrectos.")
    else:
        form = LoginForm()
    return render(request, 'login/login.html', {'form': form})

# --- VISTA 3: LOGOUT (Cerrar Sesión) ---
def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect('login')

@login_required(login_url='login')
def panel_matrona(request):
    return render(request, 'roles/panel_matrona.html')

@login_required(login_url='login')
def panel_supervisor(request):
    return render(request, 'roles/panel_supervisor.html')

@login_required(login_url='login')
def panel_auditoria(request):
    return render(request, 'roles/panel_auditoria.html')

@login_required(login_url='login')
def panel_some(request):
    return render(request, 'roles/panel_some.html')