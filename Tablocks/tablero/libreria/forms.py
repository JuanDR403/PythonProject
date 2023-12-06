# forms.py

from django import forms
from .models import Tarea, Comentario, Tarjeta, Tablero

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['descripcion', 'estado']

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']

class TarjetaForm(forms.ModelForm):
    usuarios_permitidos = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Tarjeta
        fields = ['nombre', 'descripcion', 'etiquetas']

class TableroForm(forms.ModelForm):
    class Meta:
        model = Tablero
        fields = ['nombre', 'descripcion', 'usuarios_permitidos']
