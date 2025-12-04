from django.shortcuts import render, get_object_or_404, redirect
 
from django.contrib import messages
from .models import Madre, Parto, RN
from .forms import BuscarRutForm, MadreForm, PartoForm, RNForm
 

# ----------------------------
# Inicio / Dashboard simple
# ----------------------------
def inicio(request):
    return render(request, 'partos/partos.html')


# ----------------------------
# Paso 1: Buscar o ingresar madre
# ----------------------------
 
def ingreso_madre(request):
    if request.method == "POST":
        buscar_form = BuscarRutForm(request.POST)
        if buscar_form.is_valid():
            rut = buscar_form.cleaned_data['rut']
            madre = Madre.objects.filter(rut=rut).first()
            if madre:
                messages.info(request, "Datos encontrados. Presione 'Editar' para modificar.")
                form = MadreForm(instance=madre)
            else:
                form = MadreForm(initial={'rut': rut})
                madre = None
            request.session['rut_madre'] = rut
            return render(request, 'partos/form_madre.html', {'form': form, 'madre': madre})
    else:
        buscar_form = BuscarRutForm()
    return render(request, 'partos/buscar_rut.html', {'form': buscar_form})


# ----------------------------
# Guardar madre (borrador)
# ----------------------------
 
def guardar_madre(request):
    rut = request.session.get('rut_madre')
    if not rut:
        messages.error(request, "Algo salió mal, por favor inicie nuevamente.")
        return redirect('ingreso_madre')

    madre = Madre.objects.filter(rut=rut).first()
    form = MadreForm(request.POST, instance=madre)

    if form.is_valid():
        madre_guardada = form.save(commit=False)
        # Check which button was pressed
        if 'btnRegistrar' in request.POST:
            madre_guardada.confirmado = True
            messages.success(request, "Madre registrada con éxito.")
        else:
            madre_guardada.confirmado = False
            messages.success(request, "Datos de la madre guardados como borrador.")
        madre_guardada.save()
        request.session['madre_id'] = madre_guardada.id
        return redirect('ingreso_parto')
    else:
        messages.error(request, "Corrija los errores antes de continuar.")
        return render(request, 'partos/form_madre.html', {'form': form, 'madre': madre})


# ----------------------------
# Paso 2: Ingreso Parto
# ----------------------------
 
def ingreso_parto(request):
    madre_id = request.session.get('madre_id')
    if not madre_id:
        messages.error(request, "Acceso no autorizado.")
        return redirect('inicio')

    madre = get_object_or_404(Madre, id=madre_id)
    if not madre.confirmado:
        messages.warning(request, "Debe confirmar los datos de la madre antes de registrar el parto.")
        return redirect('ingreso_madre')

    parto_existente = Parto.objects.filter(madre=madre).last()

    if request.method == "POST":
        form = PartoForm(request.POST, instance=parto_existente)
        if form.is_valid():
            parto = form.save(commit=False)
            parto.madre = madre
            parto.confirmado = False
            parto.save()
            request.session['parto_id'] = parto.id
            messages.success(request, "Parto guardado como borrador.")
            return redirect('ingreso_rn')
    else:
        form = PartoForm(instance=parto_existente)

    return render(request, 'partos/form_parto.html', {'form': form, 'madre': madre, 'parto': parto_existente})


# ----------------------------
# Paso 3: Ingreso Recién Nacido
# ----------------------------
 

def ingreso_rn(request):
    madre_id = request.session.get('madre_id')
    parto_id = request.session.get('parto_id')
    if not madre_id or not parto_id:
        messages.error(request, "Acceso no autorizado.")
        return redirect('inicio')

    madre = get_object_or_404(Madre, id=madre_id)
    parto = get_object_or_404(Parto, id=parto_id)
    if not parto.confirmado:
        messages.warning(request, "Debe confirmar el parto antes de registrar el RN.")
        return redirect('ingreso_parto')

    rn_existente = RN.objects.filter(madre=madre, parto_asociado=parto).last()

    if request.method == "POST":
        form = RNForm(request.POST, instance=rn_existente)
        if form.is_valid():
            rn = form.save(commit=False)
            rn.madre = madre
            rn.parto_asociado = parto
            rn.confirmado = False
            rn.save()
            messages.success(request, "RN guardado como borrador.")
            return redirect('listado_rn')
    else:
        form = RNForm(instance=rn_existente)

    return render(request, 'partos/form_rn.html', {'form': form, 'madre': madre, 'parto': parto, 'rn': rn_existente})

# ----------------------------
# Edición de Recién Nacido
# ----------------------------
def editar_rn(request, pk):
    rn = get_object_or_404(RN, pk=pk)
    if request.method == "POST":
        form = RNForm(request.POST, instance=rn)
        if form.is_valid():
            form.save()
            messages.success(request, "Datos del RN actualizados correctamente.")
            return redirect('listado_rn')
    else:
        form = RNForm(instance=rn)
    return render(request, 'partos/form_rn.html', {'form': form, 'madre': rn.madre, 'parto': rn.parto_asociado, 'rn': rn})


# ----------------------------
# Registrar (confirmar) registros - SOLO MATRONA
# ----------------------------
 
def registrar_madre(request, pk):
    madre = get_object_or_404(Madre, pk=pk)
    madre.confirmado = True
    madre.save()
    messages.success(request, "Madre registrada con éxito.")
    return redirect('listado_madres')


 
def registrar_parto(request, pk):
    parto = get_object_or_404(Parto, pk=pk)
    parto.confirmado = True
    parto.save()
    messages.success(request, "Parto registrado con éxito.")
    return redirect('listado_partos')


 
def registrar_rn(request, pk):
    rn = get_object_or_404(RN, pk=pk)
    rn.confirmado = True
    rn.save()
    messages.success(request, "RN registrado con éxito.")
    return redirect('listado_rn')


# ----------------------------
# Listados
# ----------------------------
 
def listado_madres(request):
    madres = Madre.objects.all().order_by('-fecha_nacimiento')
    return render(request, 'partos/listado_madre.html', {'madres': madres})


 
def listado_partos(request):
    partos = Parto.objects.all().order_by('-fecha_hora')
    return render(request, 'partos/listado_parto.html', {'partos': partos})


 
def listado_rn(request):
    rns = RN.objects.all().order_by('-fecha_nacimiento')
    return render(request, 'partos/listado_rn.html', {'rns': rns})


# ----------------------------
# Detalle
# ----------------------------
 
def detalle_madre(request, pk):
    madre = get_object_or_404(Madre, pk=pk)
    return render(request, 'partos/detalle_madre.html', {'madre': madre})


 
def detalle_parto(request, pk):
    parto = get_object_or_404(Parto, pk=pk)
    return render(request, 'partos/detalle_parto.html', {'parto': parto})


 
def detalle_rn(request, pk):
    rn = get_object_or_404(RN, pk=pk)
    return render(request, 'partos/detalle_rn.html', {'rn': rn})
