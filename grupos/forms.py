from django import forms
from .models import Grupo, GrupoAlumno
from alumnos.models import Alumno, NivelIngles

class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'input-field', 'placeholder':'Grupo de Miss Ange'}),
            'nivel': forms.Select(attrs={'class': 'input-field'}),
        }
        labels = {
            'nombre': 'Nombre del Grupo',
            'nivel': 'Nivel de Inglés Asociado',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nivel'].queryset = NivelIngles.objects.all().order_by('nombre', 'sub_nivel')

class GrupoAlumnoForm(forms.ModelForm):
    class Meta:
        model = GrupoAlumno
        fields = ['alumno'] # Solo necesitamos seleccionar el alumno
        widgets = {
            'alumno': forms.Select(attrs={'class': 'input-field'}),
        }
        labels = {
            'alumno': 'Seleccionar Alumno',
        }

    def __init__(self, *args, **kwargs):
        # El grupo actual se pasará como argumento al inicializar el formulario en la vista
        self.grupo = kwargs.pop('grupo', None)
        self.alumno_instance_for_filter = kwargs.pop('alumno', None)
        super().__init__(*args, **kwargs)

        # Filtra los alumnos que están activos Y que no están ya en este grupo específico
        if self.grupo:
            alumnos_en_este_grupo = GrupoAlumno.objects.filter(grupo=self.grupo).values_list('alumno__pk', flat=True)
            self.fields['alumno'].queryset = Alumno.objects.filter(activo=True).exclude(pk__in=alumnos_en_este_grupo).order_by('apellido', 'nombre')
        else:
            # Si no se pasa un grupo (ej. en otras vistas si se usara este form), solo mostrar activos
            self.fields['alumno'].queryset = Alumno.objects.filter(activo=True).order_by('apellido', 'nombre')

    def clean(self):
        cleaned_data = super().clean()
        alumno_seleccionado = cleaned_data.get('alumno')

        if self.grupo and alumno_seleccionado:
            # Validar que el alumno no esté ya en ESTE grupo específico
            # (aunque el queryset ya debería manejar esto, es una doble verificación)
            if GrupoAlumno.objects.filter(alumno=alumno_seleccionado, grupo=self.grupo).exists():
                raise forms.ValidationError(
                    f"El alumno '{alumno_seleccionado.nombre} {alumno_seleccionado.apellido}' ya está asignado a este grupo."
                )
        return cleaned_data