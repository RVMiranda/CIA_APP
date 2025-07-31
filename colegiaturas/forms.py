from django import forms
from .models import Colegiatura, Descuento, Recargo

class ColegiaturaPagoForm(forms.ModelForm):
    class Meta:
        model = Colegiatura
        fields = ['fecha_pago', 'monto_pagado', 'estado_pago'] # estado_pago se usará para forzar a 'Pagado'
        widgets = {
            'fecha_pago': forms.DateInput(attrs={'type': 'date', 'class': 'input-field'}),
            'monto_pagado': forms.NumberInput(attrs={'class': 'input-field'}),
            'estado_pago': forms.Select(attrs={'class': 'input-field'}),
        }
        labels = {
            'fecha_pago': 'Fecha Real de Pago',
            'monto_pagado': 'Monto Pagado',
            'estado_pago': 'Estado del Pago',
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_pago = cleaned_data.get('fecha_pago')
        monto_pagado = cleaned_data.get('monto_pagado')
        estado_pago = cleaned_data.get('estado_pago')

        # Si el estado es 'Pagado', la fecha de pago y el monto pagado son obligatorios
        if estado_pago == Colegiatura.PAGADO:
            if not fecha_pago:
                self.add_error('fecha_pago', 'La fecha de pago es obligatoria si el estado es "Pagado".')
            if monto_pagado is None:
                self.add_error('monto_pagado', 'El monto pagado es obligatorio si el estado es "Pagado".')
        
        return cleaned_data

class DescuentoForm(forms.ModelForm):
    class Meta:
        model = Descuento
        fields = '__all__'
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'input-field'}),
            'meses_anticipo': forms.NumberInput(attrs={'class': 'input-field'}),
            'porcentaje': forms.NumberInput(attrs={'class': 'input-field', 'step': '0.01'}),
        }
        labels = {
            'descripcion': 'Descripción del Descuento',
            'meses_anticipo': 'Meses de Anticipo',
            'porcentaje': 'Porcentaje (ej. 0.05 para 5%)',
        }

class RecargoForm(forms.ModelForm):
    class Meta:
        model = Recargo
        fields = '__all__'
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'input-field'}),
            'porcentaje_por_dia': forms.NumberInput(attrs={'class': 'input-field', 'step': '0.001'}),
        }
        labels = {
            'descripcion': 'Descripción del Recargo',
            'porcentaje_por_dia': 'Porcentaje por Día (ej. 0.01 para 1%)',
        }
