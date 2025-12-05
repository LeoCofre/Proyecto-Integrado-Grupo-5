from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Madre, Parto, RN
from .forms import BuscarRutForm, MadreForm, PartoForm, RNForm
from django.contrib.auth.decorators import login_required
from .role_required import role_required

# ----------------------------
# Panel Matrona: Buscar madre y registrar parto/RN
# ----------------------------
def buscar_madre_para_parto(request):
    if request.method == "POST":
        buscar_form = BuscarRutForm(request.POST)
        if buscar_form.is_valid():
            rut = buscar_form.cleaned_data['rut']
            madre = Madre.objects.filter(rut=rut, confirmado=True).first()
            if madre:
                # Redirigir a ingreso de parto con el id de la madre
                return redirect('ingreso_parto', madre_id=madre.id)
            else:
                messages.error(request, "No se encontró una madre confirmada con ese RUT. Solicite a SOME el registro.")
    else:
        buscar_form = BuscarRutForm()
    return render(request, 'partos/buscar_rut.html', {'form': buscar_form})

# ----------------------------
# Ingreso Parto (solo para madres confirmadas)
# ----------------------------
def ingreso_parto(request, madre_id):
    madre = get_object_or_404(Madre, id=madre_id, confirmado=True)
    parto_existente = Parto.objects.filter(madre=madre).last()
    if request.method == "POST":
        form = PartoForm(request.POST, instance=parto_existente)
        if form.is_valid():
            parto = form.save(commit=False)
            parto.madre = madre
            parto.confirmado = False
            parto.save()
            messages.success(request, "Parto guardado como borrador.")
            return redirect('ingreso_rn', parto_id=parto.id)
    else:
        form = PartoForm(instance=parto_existente)
    return render(request, 'partos/form_parto.html', {'form': form, 'madre': madre, 'parto': parto_existente})

# ----------------------------
# Ingreso RN (requiere madre y parto)
# ----------------------------
def ingreso_rn(request, parto_id):
    parto = get_object_or_404(Parto, id=parto_id)
    madre = parto.madre
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
    if request.GET.get('borradores'):
        partos = Parto.objects.filter(confirmado=False).order_by('-fecha_hora')
    else:
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

# ----------------------------
# Editar RN (solo para Matronas)
# ----------------------------
def editar_rn(request, pk):
    rn = get_object_or_404(RN, pk=pk)
    madre = rn.madre
    parto = rn.parto_asociado
    # Solo matrona puede editar
    if not (request.user.is_authenticated and hasattr(request.user, 'rol') and request.user.rol and request.user.rol.nombre == 'Matrona'):
        messages.error(request, "Solo la Matrona puede editar datos del RN.")
        return redirect('listado_rn')
    if request.method == "POST":
        form = RNForm(request.POST, instance=rn)
        if form.is_valid():
            rn_editado = form.save(commit=False)
            rn_editado.madre = madre  # No se puede cambiar
            rn_editado.parto_asociado = parto  # No se puede cambiar
            rn_editado.save()
            messages.success(request, "Datos del RN actualizados correctamente.")
            return redirect('listado_rn')
    else:
        form = RNForm(instance=rn)
    return render(request, 'partos/form_rn.html', {'form': form, 'madre': madre, 'parto': parto, 'rn': rn})

# ----------------------------
# Ingreso y guardado de madre (solo para SOME)
# ----------------------------
@role_required(['SOME'])
def ingreso_madre(request):
    if request.method == "POST":
        form = MadreForm(request.POST)
        if form.is_valid():
            madre = form.save(commit=False)
            madre.confirmado = False  # Por defecto, no confirmado
            madre.save()
            messages.success(request, "Madre guardada como borrador.")
            return redirect('listado_madres')
    else:
        form = MadreForm()
    return render(request, 'partos/form_madre.html', {'form': form})

@role_required(['SOME'])
def guardar_madre(request, pk):
    madre = get_object_or_404(Madre, pk=pk)
    madre.confirmado = True
    madre.save()
    messages.success(request, "Madre registrada con éxito.")
    return redirect('listado_madres')
