from django.shortcuts import render


def vista_auditoria(request): return render(request, 'auditoria/auditoria.html')

# para agregar otra vista: def vista_otro(request): return render(request, 'auditoria/otro.html')
