from django.db import models
from django.contrib.auth.models import User

# ------------------------------
# MADRE
# ------------------------------
class Madre(models.Model):
    nombre = models.CharField(max_length=150)
    rut = models.CharField(max_length=12, unique=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    antecedentes_obstetricos = models.TextField(blank=True, null=True)
    atenciones_clinicas = models.TextField(blank=True, null=True)
    acompañante = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.rut})"

# ------------------------------
# PARTO
# ------------------------------
class Parto(models.Model):
    TIPO_PARTO_CHOICES = [
        ("vaginal", "Vaginal"),
        ("cesarea", "Cesárea"),
        ("instrumentado", "Instrumentado"),
    ]

    fecha_hora = models.DateTimeField()
    tipo_parto = models.CharField(max_length=20, choices=TIPO_PARTO_CHOICES)
    complicaciones = models.TextField(blank=True, null=True)
    matrona_responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    madre = models.ForeignKey(Madre, on_delete=models.CASCADE, related_name="partos")

    def __str__(self):
        return f"Parto {self.id} - {self.madre.nombre} - {self.fecha_hora.strftime('%d-%m-%Y %H:%M')}"

# ------------------------------
# RECIÉN NACIDO
# ------------------------------
class RecienNacido(models.Model):
    SEXO_CHOICES = [
        ("M", "Masculino"),
        ("F", "Femenino"),
        ("I", "Indeterminado"),
    ]

    ESTADO_VITAL_CHOICES = [
        ("V", "Vivo"),
        ("F", "Fallecido"),
    ]

    peso = models.FloatField()
    talla = models.FloatField()
    cc = models.FloatField()
    apego = models.IntegerField()
    lactante_60min = models.BooleanField(default=False)
    profilaxis_ocular = models.BooleanField(default=False)
    vacuna_hepatitis_b = models.BooleanField(default=False)
    profesional_que_vacuna_bcg = models.CharField(max_length=150, blank=True, null=True)
    vacuna_bcg = models.BooleanField(default=False)
    apgar_minuto_uno = models.IntegerField()
    apgar_minuto_cinco = models.IntegerField()
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    estado_vital = models.CharField(max_length=1, choices=ESTADO_VITAL_CHOICES)
    reanimacion = models.BooleanField(default=False)

    madre = models.ForeignKey(Madre, on_delete=models.CASCADE, related_name="hijos")
    parto_asociado = models.ForeignKey(Parto, on_delete=models.CASCADE, related_name="recién_nacidos")

    def __str__(self):
        return f"RN {self.id} - {self.sexo} - Madre: {self.madre.nombre}"
