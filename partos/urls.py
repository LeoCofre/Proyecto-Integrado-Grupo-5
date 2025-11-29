from django.urls import path
from . import views

urlpatterns = [
    # Madre
    path("madre/", views.listado_madre, name="listado_madre"),
    path("madre/agregar/", views.crear_madre, name="crear_madre"),

    # Parto
    path("parto/", views.listado_parto, name="listado_parto"),
    path("parto/agregar/", views.crear_parto, name="crear_parto"),

    # Recién Nacido
    path("rn/", views.listado_rn, name="listado_rn"),
    path("rn/agregar/", views.crear_rn, name="crear_rn"),
]
