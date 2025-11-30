from django.db.models.signals import post_save, post_delete
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from .models import Auditoria
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

#signals.py sirve para registrar eventos en el modelo Auditoria
# cuando ocurren ciertas acciones en otros modelos o eventos de autenticación.

# ==============================================================================
# 1. IMPORTACIÓN DE MODELOS
# ==============================================================================
# Intentamos obtener los modelos Parto, RecienNacido y Usuario.
# Si no existen, usamos una clase temporal para evitar que el servidor se caiga.
try:
    #  HAY QUE CAMBIARLO YA QUE asume que 'registros' es la app donde están Parto y RecienNacido
    Parto = settings.AUTH_USER_MODEL.model._meta.apps.get_model('registros', 'Parto')
    RecienNacido = settings.AUTH_USER_MODEL.model._meta.apps.get_model('registros', 'RecienNacido')
    Usuario = settings.AUTH_USER_MODEL.model
except LookupError:
    logger.warning("Modelos clínicos no encontrados. La auditoría clínica estará deshabilitada.")
    class Parto: pass
    class RecienNacido: pass
    class Usuario: pass


# ==============================================================================
# 2. SEÑALES PARA EVENTOS CLÍNICOS (CREATE / UPDATE / DELETE)
# ==============================================================================

def registrar_evento_clinico(sender, instance, accion, **kwargs):
    """Función centralizada para registrar cualquier evento clínico simple."""
    modelo_afectado = sender.__name__
    registro_id = instance.pk
    
    # Asumimos que la instancia tiene un campo 'usuario' o 'autor' para saber quién hizo el cambio.
    # Si no tiene ese campo, 'usuario_log' será None.
    usuario_log = getattr(instance, 'usuario', None) 
    
    # Detalle simplificado
    detalles = f"Evento '{accion}' en registro ID {registro_id} del modelo {modelo_afectado}."

    Auditoria.objects.create(
        usuario=usuario_log,
        accion_realizada=accion,
        modelo_afectado=modelo_afectado,
        registro_id=registro_id,
        detalles_cambio=detalles,
        # La IP no se registra aquí porque post_save/delete no tienen acceso directo al request.
    )
    logger.info(f"Log simple registrado: {accion} en {modelo_afectado} por {usuario_log}")


@receiver(post_save, sender=Parto)
@receiver(post_save, sender=RecienNacido)
def log_clinical_save_event(sender, instance, created, **kwargs):
    """Registra Creación (CREATE) o Actualización (UPDATE)."""
    accion = 'CREATE' if created else 'UPDATE'
    registrar_evento_clinico(sender, instance, accion, **kwargs)

@receiver(post_delete, sender=Parto)
@receiver(post_delete, sender=RecienNacido)
def log_clinical_delete_event(sender, instance, **kwargs):
    """Registra Eliminación (DELETE)."""
    registrar_evento_clinico(sender, instance, 'DELETE', **kwargs)


# ==============================================================================
# 3. SEÑALES PARA EVENTOS DE SEGURIDAD (LOGIN / LOGOUT / FAILED)
# ==============================================================================

@receiver(user_logged_in)
def log_login_success(sender, request, user, **kwargs):
    """Registra Inicio de Sesión Exitoso (LOGIN_SUCCESS)."""
    Auditoria.objects.create(
        usuario=user,
        accion_realizada='LOGIN_SUCCESS',
        modelo_afectado='Usuario',
        registro_id=user.pk,
        detalles_cambio="Inicio de sesión exitoso.",
        ip_address=request.META.get('REMOTE_ADDR')
    )

@receiver(user_logged_out)
def log_logout(sender, request, user, **kwargs):
    """Registra Cierre de Sesión (LOGOUT)."""
    if user and user.is_authenticated:
        Auditoria.objects.create(
            usuario=user,
            accion_realizada='LOGOUT',
            modelo_afectado='Usuario',
            registro_id=user.pk,
            detalles_cambio="Cierre de sesión manual.",
            ip_address=request.META.get('REMOTE_ADDR')
        )

@receiver(user_login_failed)
def log_login_failed(sender, credentials, request, **kwargs):
    """Registra Intento de Inicio de Sesión Fallido (LOGIN_FAILED) y la IP."""
    username_tried = credentials.get(settings.AUTH_USER_MODEL.USERNAME_FIELD, 'Desconocido')
    ip_address = request.META.get('REMOTE_ADDR')
    
    # El usuario será None si el login falla.
    Auditoria.objects.create(
        usuario=None, 
        accion_realizada='LOGIN_FAILED',
        modelo_afectado='Sistema',
        registro_id=None,
        detalles_cambio=f"Fallo de login. Usuario intentado: {username_tried}",
        ip_address=ip_address
    )

@receiver(post_save, sender=Usuario)
def log_user_security_update(sender, instance, created, **kwargs):
    """
    Registra Bloqueo/Desbloqueo de un Usuario por parte del Administrador TI.
    """
    if not created and not instance.is_active:
        # Se asume que si no fue creado y ahora está inactivo, fue bloqueado.
        Auditoria.objects.create(
            usuario=None, 
            accion_realizada='USER_BLOCKED',
            modelo_afectado='Usuario',
            registro_id=instance.pk,
            detalles_cambio=f"Usuario RUT {instance.rut} fue BLOQUEADO por un administrador.",
            # IP es nula.
        )