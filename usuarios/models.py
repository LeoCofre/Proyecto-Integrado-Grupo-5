from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Profesional(models.Model):
    ROLE_CHOICES = [
        ('matrona', 'Matrona Clínica'),
        ('jefe', 'Jefe de Área'),
        ('admin_ti', 'Administrador de TI'),
        ('auditor', 'Auditor Interno'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='matrona')

    def _str_(self):
        return f"{self.user.username} ({self.get_role_display()})"
