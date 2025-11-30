from django import forms
from .models import Madre, Parto, RecienNacido

# ------------------------------
# Formulario para buscar Rut
# ------------------------------
class BuscarRutForm(forms.Form):
    rut = forms.CharField(
        max_length=12, 
        label="RUT de la Madre", 
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ingrese RUT sin puntos ni guion'})
    )

# ------------------------------
# Formulario Madre
# ------------------------------
class MadreForm(forms.ModelForm):
    class Meta:
        model = Madre
        fields = [
            'nombre', 'rut', 'fecha_nacimiento', 'direccion', 'telefono',
            'antecedentes_obstetricos', 'atenciones_clinicas', 'acompañante'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'rut': forms.TextInput(attrs={'class':'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'type':'date', 'class':'form-control'}),
            'direccion': forms.TextInput(attrs={'class':'form-control'}),
            'telefono': forms.TextInput(attrs={'class':'form-control'}),
            'antecedentes_obstetricos': forms.Textarea(attrs={'class':'form-control', 'rows':2}),
            'atenciones_clinicas': forms.Textarea(attrs={'class':'form-control', 'rows':2}),
            'acompañante': forms.TextInput(attrs={'class':'form-control'}),
        }

# ------------------------------
# Formulario Parto
# ------------------------------
class PartoForm(forms.ModelForm):
    class Meta:
        model = Parto
        exclude = ['madre', 'confirmado']
        widgets = {
            'fecha_hora': forms.DateTimeInput(attrs={'type':'datetime-local','class':'form-control'}),
            'tipo_parto': forms.Select(attrs={'class':'form-control'}),
            'tipo_parto_clasificado': forms.TextInput(attrs={'class':'form-control'}),
            'complicaciones': forms.Textarea(attrs={'class':'form-control', 'rows':2}),
            'parto_distocico': forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'parto_vacuum': forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'rem_a24': forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }

# ------------------------------
# Formulario Recién Nacido
# ------------------------------
class RecienNacidoForm(forms.ModelForm):
    class Meta:
        model = RecienNacido
        exclude = ['madre', 'parto_asociado', 'confirmado']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type':'date', 'class':'form-control'}),
            'hora_nacimiento': forms.TimeInput(attrs={'type':'time', 'class':'form-control'}),
            'apellido_paterno_rn': forms.TextInput(attrs={'class':'form-control'}),
            'comuna': forms.TextInput(attrs={'class':'form-control'}),
            'cesfam': forms.TextInput(attrs={'class':'form-control'}),
            'fecha_nacimiento_madre': forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'tipo_parto': forms.TextInput(attrs={'class':'form-control'}),
            'tipo_parto_clasificado': forms.TextInput(attrs={'class':'form-control'}),
            'peso': forms.NumberInput(attrs={'class':'form-control'}),
            'talla': forms.NumberInput(attrs={'class':'form-control'}),
            'cc': forms.NumberInput(attrs={'class':'form-control', 'step':'0.1'}),
            'semanas_gestacion': forms.NumberInput(attrs={'class':'form-control'}),
            'dias_gestacion': forms.NumberInput(attrs={'class':'form-control'}),
            'sexo': forms.Select(choices=RecienNacido.SEXO_CHOICES, attrs={'class':'form-control'}),
            'apego': forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'lactancia_antes_60': forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'profilaxis_ocular': forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'vacuna_hepatitis_b': forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'vacuna_bcg': forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'profesional_vhb': forms.TextInput(attrs={'class':'form-control'}),
            'apgar_1': forms.NumberInput(attrs={'class':'form-control'}),
            'apgar_5': forms.NumberInput(attrs={'class':'form-control'}),
            'anomalia_congenita': forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'reanimacion_basica': forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'reanimacion_avanzada': forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'ehi_grado_ii_iii': forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }
