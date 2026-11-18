from django import forms

from .models import Encargo


class EncargoForm(forms.ModelForm):
    class Meta:
        model = Encargo
        fields = ('nombre_cliente', 'correo_cliente', 'fecha_retiro', 'cantidad')
        labels = {
            'nombre_cliente': 'Nombre',
            'correo_cliente': 'Correo electrónico',
            'fecha_retiro': 'Fecha de retiro',
            'cantidad': 'Cantidad de unidades',
        }
        widgets = {
            'fecha_retiro': forms.DateInput(attrs={'type': 'date'}),
            'cantidad': forms.NumberInput(attrs={'min': 1}),
        }
