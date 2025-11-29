from django.db import models
from django.conf import settings # Se importa la configuración de Django
import datetime


class Auditoria(models.Model):
    
    # Referencia al usuario que realiza la acción.
    # settings.AUTH_USER_MODEL : referenciar el modelo de usuario que se utiliza para la autenticación
    # (ya sea el modelo de Django o el modelo 'login.Usuario' si se configura como tal en settings.py).
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,         # Puede ser null si es un LOGIN_FAILED o un intento sin usuario logueado
        verbose_name="Usuario Involucrado"
    )
    
    fecha_hora = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Fecha y Hora del Evento"
    )
    
    # Lista de Tipos de Eventos (Punto B y C del informe)
    ACCIONES_CHOICES = [
        # Acciones Clínicas/Administrativas
        ('CREATE', 'Creación de Registro'),
        ('UPDATE', 'Actualización de Registro'),
        ('DELETE', 'Eliminación de Registro'),
        # Acciones de Autenticación
        ('LOGIN_SUCCESS', 'Inicio de Sesión Exitoso'),
        ('LOGIN_FAILED', 'Intento de Inicio de Sesión Fallido'),
        ('LOGOUT', 'Cierre de Sesión'),
        # Acciones de Seguridad
        ('ACCESS_DENIED', 'Intento de Acceso No Autorizado'),
        ('USER_BLOCKED', 'Usuario Bloqueado por Seguridad'),
        ('TOKEN_RECOVERY', 'Uso de Enlace de Recuperación de Contraseña')
    ]

    accion_realizada = models.CharField(
        max_length=50, 
        choices=ACCIONES_CHOICES,
        verbose_name="Tipo de Evento Registrado"
    )
    
    # Trazabilidad del registro afectado (ya que se eliminó la tabla externa)
    # Permite saber qué tabla (modelo) y qué ID fueron modificados.
    modelo_afectado = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name="Modelo Afectado (Ej: 'Parto', 'Usuario')"
    )
    
    registro_id = models.IntegerField(
        blank=True, 
        null=True, 
        verbose_name="ID del Registro Afectado"
    )
    
    # Contiene la información de los campos modificados, útil para el Auditor Interno
    detalles_cambio = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Detalles, Datos 'Antes' y 'Después', o Mensaje de Error"
    )
    
    # Campo de seguridad adicional requerido por normativas (MINSAL / Ciberseguridad)
    ip_address = models.GenericIPAddressField(
        blank=True, 
        null=True, 
        verbose_name="Dirección IP del Cliente"
    )
    
    class Meta:
        verbose_name = "Registro de Trazabilidad y Auditoría"
        verbose_name_plural = "Registros de Trazabilidad y Auditoría"
        # Ordenar por fecha descendente para ver los eventos más recientes primero
        ordering = ['-fecha_hora']
        
    def __str__(self):
        return f"[{self.fecha_hora.strftime('%Y-%m-%d %H:%M')}] {self.accion_realizada} | Modelo: {self.modelo_afectado} ID: {self.registro_id}"