from django.db import models
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
class Usuario(models.Model):
    
    # Identificación
    nombre = models.CharField(
        max_length=100, 
        verbose_name="Nombre Completo del Trabajador"
    )
    rut = models.CharField(
        max_length=12, 
        unique=True, 
        verbose_name="RUT (Identificador Único)"
    )
    
    # Autenticación (Tu lógica manual)
    password = models.CharField(
        max_length=128, 
        verbose_name="Contraseña (Hasheada Manualmente)"
    ) 
    
    # Relación con Rol
    rol = models.ForeignKey(
        Rol, 
        on_delete=models.PROTECT, 
        verbose_name="Rol Asignado"
    )
    
    # --- SEGURIDAD Y BLOQUEO (HU-01) ---
    is_active = models.BooleanField(
        default=True,
        verbose_name="Cuenta Activa/Desbloqueada"
    )
    intentos_fallidos = models.IntegerField(
        default=0,
        verbose_name="Intentos fallidos de inicio de sesión"
    )
    
    # --- RECUPERACIÓN ---
    # Aunque no usen tokens por correo, estos campos pueden servir 
    # para auditoría interna del reseteo manual.
    token_recuperacion = models.CharField(
        max_length=64, 
        blank=True, 
        null=True, 
        verbose_name="Token de Recuperación (Opcional)"
    )
    token_expira = models.DateTimeField(
        blank=True, 
        null=True, 
        verbose_name="Expiración del Token"
    )
    
    class Meta:
        verbose_name = "Usuario del Sistema"
        verbose_name_plural = "Usuarios del Sistema"
        
    def __str__(self):
        return f"{self.nombre} ({self.rol.nombre})"