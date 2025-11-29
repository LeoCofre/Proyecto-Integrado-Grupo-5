from django.db import models

class Madre(models.Model):
    nombre = models.CharField(max_length=255)
    rut = models.CharField(max_length=12, unique=True)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    antecedentes_obstetricos = models.TextField(blank=True, null=True)
    atenciones_clinicas = models.TextField(blank=True, null=True)
    acompañante = models.CharField(max_length=255, blank=True, null=True)
    confirmado = models.BooleanField(default=False)  # Para control de Matrona

    def __str__(self):
        return f"{self.nombre} ({self.rut})"


class Parto(models.Model):
    TIPO_PARTO_CHOICES = [
        ('vaginal', 'Vaginal'),
        ('cesarea', 'Cesárea'),
        ('instrumental', 'Instrumental'),
        ('extrahospitalario', 'Extrahospitalario'),
    ]
    madre = models.ForeignKey(Madre, on_delete=models.CASCADE, related_name='partos')
    fecha_hora = models.DateTimeField()
    tipo_parto = models.CharField(max_length=20, choices=TIPO_PARTO_CHOICES)
    tipo_parto_clasificado = models.CharField(max_length=20, blank=True, null=True)
    complicaciones = models.TextField(blank=True, null=True)
    parto_distocico = models.BooleanField(default=False)
    parto_vacuum = models.BooleanField(default=False)
    rem_a24 = models.BooleanField(default=False)
    confirmado = models.BooleanField(default=False)

    def __str__(self):
        return f"Parto {self.id} - {self.madre.nombre}"


class RecienNacido(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('I', 'Indeterminado'),
    ]
    madre = models.ForeignKey(Madre, on_delete=models.CASCADE, related_name='recién_nacidos')
    parto_asociado = models.ForeignKey(Parto, on_delete=models.CASCADE, related_name='recién_nacidos')
    fecha_nacimiento = models.DateField()
    hora_nacimiento = models.TimeField()
    apellido_paterno_rn = models.CharField(max_length=255)
    comuna = models.CharField(max_length=255, blank=True, null=True)
    cesfam = models.CharField(max_length=255, blank=True, null=True)
    fecha_nacimiento_madre = models.DateField(blank=True, null=True)
    tipo_parto = models.CharField(max_length=20, blank=True, null=True)
    tipo_parto_clasificado = models.CharField(max_length=20, blank=True, null=True)
    peso = models.IntegerField(blank=True, null=True)
    talla = models.IntegerField(blank=True, null=True)
    cc = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    semanas_gestacion = models.IntegerField(blank=True, null=True)
    dias_gestacion = models.IntegerField(blank=True, null=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    apego = models.BooleanField(default=False)
    lactancia_antes_60 = models.BooleanField(default=False)
    profilaxis_ocular = models.BooleanField(default=False)
    vacuna_hepatitis_b = models.BooleanField(default=False)
    vacuna_bcg = models.BooleanField(default=False)
    profesional_vhb = models.CharField(max_length=255, blank=True, null=True)
    apgar_1 = models.IntegerField(blank=True, null=True)
    apgar_5 = models.IntegerField(blank=True, null=True)
    anomalia_congenita = models.BooleanField(default=False)
    reanimacion_basica = models.BooleanField(default=False)
    reanimacion_avanzada = models.BooleanField(default=False)
    ehi_grado_ii_iii = models.BooleanField(default=False)
    confirmado = models.BooleanField(default=False)  # Solo Matrona puede confirmar

    def __str__(self):
        return f"{self.apellido_paterno_rn} - {self.madre.nombre}"
