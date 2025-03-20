# solicitudes/forms.py
from django import forms # type: ignore
from django.contrib.auth.forms import UserCreationForm # type: ignore
from django.contrib.auth.models import User # type: ignore
from django import forms
from .models import SolicitudMaterial

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico", help_text="")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Eliminar los mensajes de ayuda de los campos
        self.fields['username'].help_text = ""
        self.fields['password1'].help_text = ""
        self.fields['password2'].help_text = ""
        
        
        

class SolicitudMaterialForm(forms.ModelForm):
    class Meta:
        model = SolicitudMaterial
        fields = ['nombre_solicitante', 'tipo_material', 'cantidad', 'comentarios']