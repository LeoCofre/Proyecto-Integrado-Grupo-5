from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import datetime

# ==============================================================================
# 1. MODELO DE ROL (PERFIL DE USUARIO)
# ==============================================================================
class Rol(models.Model):
    """
    Define los perfiles de usuario y sus permisos específicos.
    Roles: Matrona, Jefe de Área, Administrador TI, Auditor Interno, Enfermero, SOME.
    """
    nombre = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name="Perfil de Usuario"
    )
    descripcion = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Descripción de las responsabilidades"
    )

    # ---------------------------------------------------------
    # PERMISOS OPERACIONALES (Matrona / Enfermero)
    # ---------------------------------------------------------
    puede_registrar_partos_rn = models.BooleanField(
        default=False, 
        verbose_name="Permiso: Registrar Partos y RN (HU-02)"
    )
    # La lógica de editar solo propios va en la VISTA, aquí solo el permiso general
    puede_editar_registros = models.BooleanField(
        default=False, 
        verbose_name="Permiso: Editar registros clínicos propios (HU-03)"
    )

    # ---------------------------------------------------------
    # PERMISOS DE LECTURA Y SUPERVISIÓN (Jefe / Auditor)
    # ---------------------------------------------------------
    puede_ver_datos_clinicos_total = models.BooleanField(
        default=False, 
        verbose_name="Acceso a todos los registros (Lectura)"
    )
    puede_generar_reportes = models.BooleanField(
        default=False, 
        verbose_name="Generar reportes ministeriales REM BS22 (HU-04)"
    )
    puede_consultar_auditoria = models.BooleanField(
        default=False, 
        verbose_name="Consulta de pista de auditoría (HU-05 y HU-10)"
    )

    # ---------------------------------------------------------
    # PERMISOS DE ADMINISTRACIÓN TÉCNICA (TI)
    # ---------------------------------------------------------
    puede_administrar_usuarios = models.BooleanField(
        default=False, 
        verbose_name="Administra usuarios (crear/editar/bloquear) (HU-09/11)"
    )
    puede_revisar_logs_tecnicos = models.BooleanField(
        default=False, 
        verbose_name="Gestiona cuentas y revisa logs técnicos"
    )

    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuarios"
        
    def __str__(self):
        return self.nombre


# ==============================================================================
# 2. MODELO DE USUARIO (TU VERSIÓN PERSONALIZADA)
# ==============================================================================
from django.utils.translation import gettext_lazy as _

class Usuario(AbstractUser):
    rut = models.CharField(
        max_length=12, 
        unique=True, 
        verbose_name="RUT (Identificador Único)"
    )
    nombre = models.CharField(
        max_length=100, 
        verbose_name="Nombre Completo del Trabajador"
    )
    rol = models.ForeignKey(
        Rol, 
        on_delete=models.SET_NULL, 
        null=True, blank=True, 
        verbose_name="Rol Asignado"
    )
    # Sobrescribe username para que no sea requerido ni visible
    username = models.CharField(
        max_length=150,
        unique=False,
        blank=True,
        null=True,
        editable=False,  # Oculta el campo en el admin y formularios
        verbose_name="(Oculto)"
    )
    USERNAME_FIELD = 'rut'
    REQUIRED_FIELDS = []  # Solo rut y password serán requeridos
    def __str__(self):
        return f"{self.nombre} ({self.rut})"
