# forms.py

from django import forms
from .models import Tarea, Comentario, Tarjeta

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['descripcion', 'estado']

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']

class TarjetaForm(forms.ModelForm):
    class Meta:
        model = Tarjeta
        fields = ['nombre', 'descripcion', 'etiquetas']