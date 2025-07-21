from django import forms
from .models import Alumno, NivelIngles, Inscripcion, Reinscripcion

class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['nombre', 'apellido', 'fecha_nacimiento', 'edad', 'telefono', 'nombre_tutor', 'telefono_tutor', 'direccion', 'activo']
        widgets = {
            'nombre':           forms.TextInput(attrs={'class': 'input-field'}),
            'apellido':         forms.TextInput(attrs={'class': 'input-field'}),
            'matricula':        forms.TextInput(attrs={'class': 'input-field'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'input-field', 'type': 'date'}),
            'edad':             forms.NumberInput(attrs={'class': 'input-field'}),
            'telefono':         forms.TextInput(attrs={'class': 'input-field'}),
            'nombre_tutor':     forms.TextInput(attrs={'class': 'input-field'}),
            'telefono_tutor':   forms.TextInput(attrs={'class': 'input-field'}),
            'direccion': forms.Textarea(attrs={'class': 'input-field', 'rows': 3}),
            'activo':           forms.CheckboxInput(attrs={'class':'mr-2'}),
        }
        labels = {
            'nombre': 'Nombre(s)',
            'apellido': 'Apellido(s)',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'edad': 'Edad',
            'telefono': 'Teléfono del Alumno',
            'nombre_tutor': 'Nombre del Tutor',
            'telefono_tutor': 'Teléfono del Tutor',
            'direccion': 'Dirección',
            'activo': '¿Alumno activo? (Marcar si el alumno está activo)'
        }

class AlumnoInscripcionForm(forms.ModelForm):
    nivel = forms.ModelChoiceField(
        queryset=NivelIngles.objects.all(),
        label="Nivel al que se inscribe",
        widget=forms.Select(attrs={'class': 'input-field'})
    )
    monto = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label="Monto de la inscripción",
        widget=forms.NumberInput(attrs={'class': 'input-field', 'placeholder': '650.00'})
    )

    class Meta:
        model = Alumno
        fields = [
            'nombre', 'apellido', 'fecha_nacimiento',
            'edad', 'telefono', 'nombre_tutor', 'telefono_tutor',
            'direccion',
        ]
        widgets = {
            'nombre':           forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Alondra'}),
            'apellido':         forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Miranda'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'input-field', 'type': 'date'}),
            'edad':             forms.NumberInput(attrs={'class': 'input-field', 'placeholder': '14'}),
            'telefono':         forms.TextInput(attrs={'class': 'input-field', 'placeholder': '9191003085'}),
            'nombre_tutor':     forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Valentin Miranda'}),
            'telefono_tutor':   forms.TextInput(attrs={'class': 'input-field', 'placeholder': '9196726551'}),
            'direccion': forms.Textarea(attrs={'class': 'input-field', 'rows': 3, 'placeholder': '11a oriente, barrio tonina'}),
        }
        labels = {
            'nombre': 'Nombre(s) del alumno',
            'apellido': 'Apellido(s) del alumno',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'edad': 'Edad',
            'telefono': 'Teléfono del alumno',
            'nombre_tutor': 'Nombre del tutor',
            'telefono_tutor': 'Teléfono del tutor',
            'direccion': 'Dirección del domicilio',
        }

class ReinscripcionForm(forms.ModelForm):
    class Meta:
        model = Reinscripcion
        fields = ['nivel', 'monto']
        widgets = {
            'nivel': forms.Select(attrs={'class':'input-field'}),
            'monto': forms.NumberInput(attrs={'class':'input-field','placeholder':'650.00'}),
        }
        labels = {
            'nivel': 'Nivel al que se reinscribe',
            'monto': 'Monto de la Reinscripción',
        }

