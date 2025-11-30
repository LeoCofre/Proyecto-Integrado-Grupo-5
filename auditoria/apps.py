from django.apps import AppConfig


class AuditoriaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auditoria'
    def ready(self):
        import auditoria.signals
        # Asegura que las señales se registren cuando la app esté lista


  