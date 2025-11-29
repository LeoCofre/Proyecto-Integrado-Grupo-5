from django import formsfrom partos.models import Madre, Parto, RecienNacido
class FiltroReporteForm(forms.Form):
    madre = forms.ModelChoiceField(
        queryset=Madre.objects.all(), required=False, label="Madre"    )
    tipo_parto = forms.ChoiceField(
        choices=[("", "Todos"), ("vaginal", "Vaginal"), ("cesarea", "Cesárea"), ("instrumentado", "Instrumentado")],
        required=False,
        label="Tipo de Parto"    )
    sexo_rn = forms.ChoiceField(
        choices=[("", "Todos"), ("M", "Masculino"), ("F", "Femenino"), ("I", "Indeterminado")],
        required=False,
        label="Sexo RN"    )
    fecha_inicio = forms.DateField(required=False, widget=forms.DateInput(attrs={'type':'date'}))
    fecha_fin = forms.DateField(required=False, widget=forms.DateInput(attrs={'type':'date'}))