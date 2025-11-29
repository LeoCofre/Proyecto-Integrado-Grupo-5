from django.shortcuts import render 
from django.db.models import Count 
from partos.models import Madre, Parto, RecienNacido 
from.forms import FiltroReporte, Form 
from django.http import HttpResponse 
import csvimport datetime
import io 
from openpyxl import Workbook
# Dashboard general def dashboard(request):
    total_madres = Madre.objects.count()
    total_partos = Parto.objects.count()
    total_rn = RecienNacido.objects.count()

    # Ejemplo de datos para gráfico: RN por sexo    rn_por_sexo = RecienNacido.objects.values('sexo').annotate(total=Count('id'))

    context = {
        'total_madres': total_madres,
        'total_partos': total_partos,
        'total_rn': total_rn,
        'rn_por_sexo': rn_por_sexo,
    }
    return render(request, 'reportes/dashboard.html', context)
# Reporte con filtros def reportes_graficos(request):
    form = FiltroReporteForm(request.GET or None)
    rns = RecienNacido.objects.all()

    if form.is_valid():
        madre = form.cleaned_data.get('madre')
        tipo_parto = form.cleaned_data.get('tipo_parto')
        sexo_rn = form.cleaned_data.get('sexo_rn')
        fecha_inicio = form.cleaned_data.get('fecha_inicio')
        fecha_fin = form.cleaned_data.get('fecha_fin')

        if madre:
            rns = rns.filter(madre=madre)
        if tipo_parto:
            rns = rns.filter(parto_asociado__tipo_parto=tipo_parto)
        if sexo_rn:
            rns = rns.filter(sexo=sexo_rn)
        if fecha_inicio:
            rns = rns.filter(parto_asociado__fecha_hora__date__gte=fecha_inicio)
        if fecha_fin:
            rns = rns.filter(parto_asociado__fecha_hora__date__lte=fecha_fin)

    # Datos agregados para gráficos    rn_por_sexo = rns.values('sexo').annotate(total=Count('id'))

    context = {
        'form': form,
        'rns': rns,
        'rn_por_sexo': rn_por_sexo,
    }
    return render(request, 'reportes/reportes_graficos.html', context)
# Exportar Excel def exportar_excel(request):
    rns = RecienNacido.objects.all()
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=Reporte_RN_{datetime.date.today()}.xlsx'

    wb = Workbook()
    ws = wb.active
    ws.title = "Recién Nacidos"
    headers = ["ID", "Madre", "Parto Asociado", "Peso", "Talla", "CC", "Sexo", "APGAR 1'", "APGAR 5'"]
    ws.append(headers)

    for rn in rns:
        ws.append([
            rn.id,
            rn.madre.nombre,
            rn.parto_asociado.id,
            rn.peso,
            rn.talla,
            rn.cc,
            rn.get_sexo_display(),
            rn.apgar_minuto_uno,
            rn.apgar_minuto_cinco
        ])

    wb.save(response)   
    return response