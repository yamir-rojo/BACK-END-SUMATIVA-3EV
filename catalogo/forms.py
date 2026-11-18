from django import forms
from django.utils import timezone

from .models import Encargo


class EncargoForm(forms.ModelForm):
    cantidad = forms.IntegerField(
        min_value=1,
        max_value=3,
        label='Cantidad de unidades',
        widget=forms.NumberInput(attrs={'min': 1, 'max': 3}),
    )

    class Meta:
        model = Encargo
        fields = ('nombre_cliente', 'correo_cliente', 'fecha_retiro', 'cantidad')
        labels = {
            'nombre_cliente': 'Nombre',
            'correo_cliente': 'Correo electrónico',
            'fecha_retiro': 'Fecha de retiro',
        }
        widgets = {
            'fecha_retiro': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_fecha_retiro(self):
        fecha_retiro = self.cleaned_data['fecha_retiro']
        if fecha_retiro < timezone.localdate():
            raise forms.ValidationError(
                'La fecha de retiro no puede ser anterior a hoy.',
            )
        return fecha_retiro
