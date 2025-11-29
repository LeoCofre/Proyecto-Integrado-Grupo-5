from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Madre, Parto, RecienNacido
from .forms import BuscarRutForm, MadreForm, PartoForm, RecienNacidoForm
from django.views.decorators.http import require_http_methods
from .role_required import role_required  # nuestro decorador

# ----------------------------
# Inicio / Dashboard simple
# ----------------------------
def inicio(request):
    return render(request, 'partos/inicio.html')


# ----------------------------
# Paso 1: Buscar o ingresar madre
# ----------------------------
@role_required(allowed_roles=['matrona', 'enfermero'])
@require_http_methods(["GET", "POST"])
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
@role_required(allowed_roles=['matrona', 'enfermero'])
@require_http_methods(["POST"])
def guardar_madre(request):
    rut = request.session.get('rut_madre')
    if not rut:
        messages.error(request, "Algo salió mal, por favor inicie nuevamente.")
        return redirect('ingreso_madre')

    madre = Madre.objects.filter(rut=rut).first()
    form = MadreForm(request.POST, instance=madre)

    if form.is_valid():
        madre_guardada = form.save(commit=False)
        madre_guardada.confirmado = False
        madre_guardada.save()
        request.session['madre_id'] = madre_guardada.id
        messages.success(request, "Datos de la madre guardados como borrador.")
        return redirect('ingreso_parto')
    else:
        messages.error(request, "Corrija los errores antes de continuar.")
        return render(request, 'partos/form_madre.html', {'form': form, 'madre': madre})


# ----------------------------
# Paso 2: Ingreso Parto
# ----------------------------
@role_required(allowed_roles=['matrona', 'enfermero'])
@require_http_methods(["GET", "POST"])
def ingreso_parto(request):
    madre_id = request.session.get('madre_id')
    if not madre_id:
        messages.error(request, "Acceso no autorizado.")
        return redirect('inicio')

    madre = get_object_or_404(Madre, id=madre_id)
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
            return redirect('ingreso_recién_nacido')
    else:
        form = PartoForm(instance=parto_existente)

    return render(request, 'partos/form_parto.html', {'form': form, 'madre': madre, 'parto': parto_existente})


# ----------------------------
# Paso 3: Ingreso Recién Nacido
# ----------------------------
@role_required(allowed_roles=['matrona', 'enfermero'])
@require_http_methods(["GET", "POST"])
def ingreso_recién_nacido(request):
    madre_id = request.session.get('madre_id')
    parto_id = request.session.get('parto_id')
    if not madre_id or not parto_id:
        messages.error(request, "Acceso no autorizado.")
        return redirect('inicio')

    madre = get_object_or_404(Madre, id=madre_id)
    parto = get_object_or_404(Parto, id=parto_id)

    rn_existente = RecienNacido.objects.filter(madre=madre, parto_asociado=parto).last()

    if request.method == "POST":
        form = RecienNacidoForm(request.POST, instance=rn_existente)
        if form.is_valid():
            rn = form.save(commit=False)
            rn.madre = madre
            rn.parto_asociado = parto
            rn.confirmado = False
            rn.save()
            messages.success(request, "Recién nacido guardado como borrador.")
            return redirect('listado_recién_nacidos')
    else:
        form = RecienNacidoForm(instance=rn_existente)

    return render(request, 'partos/form_rn.html', {'form': form, 'madre': madre, 'parto': parto, 'rn': rn_existente})


# ----------------------------
# Registrar (confirmar) registros - SOLO MATRONA
# ----------------------------
@role_required(allowed_roles=['matrona'])
@require_http_methods(["POST"])
def registrar_madre(request, pk):
    madre = get_object_or_404(Madre, pk=pk)
    madre.confirmado = True
    madre.save()
    messages.success(request, "Madre registrada con éxito.")
    return redirect('listado_madres')


@role_required(allowed_roles=['matrona'])
@require_http_methods(["POST"])
def registrar_parto(request, pk):
    parto = get_object_or_404(Parto, pk=pk)
    parto.confirmado = True
    parto.save()
    messages.success(request, "Parto registrado con éxito.")
    return redirect('listado_partos')


@role_required(allowed_roles=['matrona'])
@require_http_methods(["POST"])
def registrar_rn(request, pk):
    rn = get_object_or_404(RecienNacido, pk=pk)
    rn.confirmado = True
    rn.save()
    messages.success(request, "Recién nacido registrado con éxito.")
    return redirect('listado_recién_nacidos')


# ----------------------------
# Listados
# ----------------------------
@role_required(allowed_roles=['matrona', 'enfermero'])
def listado_madres(request):
    madres = Madre.objects.all().order_by('-fecha_nacimiento')
    return render(request, 'partos/listado_madre.html', {'madres': madres})


@role_required(allowed_roles=['matrona', 'enfermero'])
def listado_partos(request):
    partos = Parto.objects.all().order_by('-fecha_hora')
    return render(request, 'partos/listado_parto.html', {'partos': partos})


@role_required(allowed_roles=['matrona', 'enfermero'])
def listado_recién_nacidos(request):
    rns = RecienNacido.objects.all().order_by('-fecha_nacimiento')
    return render(request, 'partos/listado_rn.html', {'rns': rns})


# ----------------------------
# Detalle
# ----------------------------
@role_required(allowed_roles=['matrona', 'enfermero'])
def detalle_madre(request, pk):
    madre = get_object_or_404(Madre, pk=pk)
    return render(request, 'partos/detalle_madre.html', {'madre': madre})


@role_required(allowed_roles=['matrona', 'enfermero'])
def detalle_parto(request, pk):
    parto = get_object_or_404(Parto, pk=pk)
    return render(request, 'partos/detalle_parto.html', {'parto': parto})


@role_required(allowed_roles=['matrona', 'enfermero'])
def detalle_recién_nacido(request, pk):
    rn = get_object_or_404(RecienNacido, pk=pk)
    return render(request, 'partos/detalle_rn.html', {'rn': rn})
