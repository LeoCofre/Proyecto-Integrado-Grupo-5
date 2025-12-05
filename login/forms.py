from django import forms
from .models import Usuario, Rol

# Formulario para que el Administrador TI cree usuarios (HU-09/HU-11)
class CrearUsuarioForm(forms.ModelForm):
    # Campos adicionales para manejar la contraseña de forma segura en el formulario
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese contraseña'}),
        label="Contraseña"
    )
    confirmar_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repita la contraseña'}),
        label="Confirmar Contraseña"
    )

    class Meta:
        model = Usuario
        # Solo incluimos los campos que se guardan directamente (excepto password que procesamos manual)
        fields = ['nombre', 'rut', 'rol']
        
        # Agregamos estilos CSS básicos (Bootstrap)
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12345678-9'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        """
        Validación personalizada para verificar que las contraseñas coincidan.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmar_password = cleaned_data.get("confirmar_password")

        if password and confirmar_password:
            if password != confirmar_password:
                raise forms.ValidationError("Las contraseñas no coinciden. Por favor, inténtelo de nuevo.")
        
        return cleaned_data

# Formulario simple para el Login (HU-01)
class LoginForm(forms.Form):
    rut = forms.CharField(
        label="RUT",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su RUT'})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su contraseña'})
    )