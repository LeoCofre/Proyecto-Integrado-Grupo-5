from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from .forms import CrearUsuarioForm, LoginForm # Asegúrate de importar tus forms
from .models import Usuario

# --- VISTA 1: CREAR USUARIO (Solo para Admin TI) ---
# Esta vista maneja la lógica de crear un usuario nuevo con contraseña encriptada.



""" def crear_usuario_view(request):
    # TODO: Aquí podrías agregar una validación simple: if request.user.rol.nombre != 'ADMIN_TI': return redirect('home')
    
    if request.method == 'POST':
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            # 1. Obtener datos limpios del formulario
            nombre = form.cleaned_data['nombre']
            rut = form.cleaned_data['rut']
            rol = form.cleaned_data['rol']
            password_plana = form.cleaned_data['password']
            
            # 2. Encriptar contraseña MANUALMENTE antes de guardar
            # Esto es vital porque tu modelo usa un CharField simple para password (si decidiste mantener tu modelo original)
            # Si usas AbstractUser, make_password también funciona bien para setear el campo password.
            password_encriptada = make_password(password_plana)
            
            # 3. Crear el objeto Usuario
            try:
                nuevo_usuario = Usuario(
                    nombre=nombre, # O nombre_completo, según tu modelo exacto
                    rut=rut,
                    rol=rol,
                    password=password_encriptada, # Guardamos el hash
                    is_active=True
                )
                nuevo_usuario.save()
                print("Usuario creado:", nuevo_usuario.rut)



                messages.success(request, f'Usuario {nombre} creado correctamente.')
                return redirect('crear_usuario') # Recarga la página limpia para crear otro
                
            except Exception as e:
                messages.error(request, f"Error al guardar: {str(e)}")
                
    else:
        messages.error(request, f"Errores del formulario: {form.errors}")


        form = CrearUsuarioForm()
    
    return render(request, 'login/crear_usuario.html', {'form': form}) """

def crear_usuario_view(request):
    if request.method == 'POST':
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            rut = form.cleaned_data['rut']
            rol = form.cleaned_data['rol']
            password_plana = form.cleaned_data['password']
            password_encriptada = make_password(password_plana)

            try:
                nuevo_usuario = Usuario(
                    nombre=nombre,
                    rut=rut,
                    rol=rol,
                    password=password_encriptada,
                    is_active=True
                )
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
# Esta vista maneja la autenticación y la redirección según el rol.

""" def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            rut = form.cleaned_data['username'] # En el form se llama 'username' pero es el RUT
            password = form.cleaned_data['password']
            
            # 1. Autenticar con Django
            # authenticate busca un usuario con ese RUT y verifica el hash de la contraseña
            user = authenticate(request, username=rut, password=password)
            
            if user is not None:
                if user.is_active:
                    # 2. Iniciar la sesión oficial
                    login(request, user)
                    
                    # 3. Guardar Rol en Sesión (Truco para compatibilidad con código de tu compañero)
                    if user.rol:
                        request.session['rol'] = user.rol.nombre
                    else:
                        request.session['rol'] = 'guest'
                    
                    # 4. Redirigir según el Rol
                    rol_actual = request.session['rol']
                    
                    if rol_actual == 'Matrona':
                        return redirect('panel_matrona') # Asegúrate de tener esta URL name
                    elif rol_actual == 'Enfermero':
                        return redirect('panel_matrona') # Enfermero va al mismo panel que Matrona
                    elif rol_actual == 'Jefe de Área' or rol_actual == 'Supervisor':
                        return redirect('panel_supervisor')
                    elif rol_actual == 'Administrador TI':
                        return redirect('crear_usuario') # El admin va directo a crear usuarios
                    else:
                        return redirect('home') # Página por defecto
                else:
                    messages.error(request, "Tu cuenta está desactivada.")
            else:
                messages.error(request, "RUT o contraseña incorrectos.")
    else:
        form = LoginForm()
        
    return render(request, 'login/login.html', {'form': form}) """


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            rut = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                usuario = Usuario.objects.get(rut=rut)
                if check_password(password, usuario.password):
                    # Guardar sesión manual
                    request.session['usuario_id'] = usuario.id
                    request.session['rol'] = usuario.rol.nombre if usuario.rol else 'guest'

                    # Redirigir según rol
                    rol_actual = request.session['rol']
                    if rol_actual == 'Administrador TI':
                        return redirect('crear_usuario')
                    elif rol_actual in ['Matrona', 'Enfermero']:
                        return redirect('panel_matrona')
                    elif rol_actual == 'Supervisor':
                        return redirect('panel_supervisor')
                    elif rol_actual == 'Auditor Interno':
                        return redirect('panel_auditoria')
                    elif rol_actual == 'SOME':
                        return redirect('panel_some')
                    else:
                        return redirect('panel_matrona')
                else:
                    messages.error(request, "RUT o contraseña incorrectos.")
            except Usuario.DoesNotExist:
                messages.error(request, "RUT o contraseña incorrectos.")
    else:
        form = LoginForm()

    return render(request, 'login/login.html', {'form': form})

# --- VISTA 3: LOGOUT (Cerrar Sesión) ---
def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect('login')

def panel_matrona(request):
    # Check for custom session-based authentication
    if 'usuario_id' not in request.session:
        messages.warning(request, "Debes iniciar sesión primero.")
        return redirect('login')
    return render(request, 'roles/panel_matrona.html')

def panel_supervisor(request):
    if 'usuario_id' not in request.session:
        messages.warning(request, "Debes iniciar sesión primero.")
        return redirect('login')
    return render(request, 'roles/panel_supervisor.html')

def panel_auditoria(request):
    if 'usuario_id' not in request.session:
        messages.warning(request, "Debes iniciar sesión primero.")
        return redirect('login')
    return render(request, 'roles/panel_auditoria.html')

def panel_some(request):
    if 'usuario_id' not in request.session:
        messages.warning(request, "Debes iniciar sesión primero.")
        return redirect('login')
    return render(request, 'roles/panel_some.html')