
from django.shortcuts import render

def panel_matrona(request):
	return render(request, 'roles/panel_matrona.html')

def panel_supervisor(request):
	return render(request, 'roles/panel_supervisor.html')

def panel_auditoria(request):
	return render(request, 'roles/panel_auditoria.html')

def panel_some(request):
	return render(request, 'roles/panel_some.html')
