from django import forms
from .models import Grupo, GrupoAlumno
from alumnos.models import Alumno, NivelIngles

class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'input-field'}),
            'nivel': forms.Select(attrs={'class': 'input-field'}),
        }
        labels = {
            'nombre': 'Nombre del Grupo (ej. "Grupo A", "Grupo de Conversación")',
            'nivel': 'Nivel de Inglés Asociado',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nivel'].queryset = NivelIngles.objects.all().order_by('nombre', 'sub_nivel')

class GrupoAlumnoForm(forms.ModelForm):
    class Meta:
        model = GrupoAlumno
        fields = ['grupo']
        widgets = {
            'grupo': forms.Select(attrs={'class': 'input-field'}),
        }
        labels = {
            'grupo': 'Seleccionar Grupo Existente',
        }

    def __init__(self, *args, **kwargs):
        # El alumno se pasará como argumento al inicializar el formulario en la vista
        self.alumno = kwargs.pop('alumno', None)
        super().__init__(*args, **kwargs)
        # Aseguramos que el queryset de grupo muestre los grupos existentes
        self.fields['grupo'].queryset = Grupo.objects.all().order_by('nivel__nombre', 'nombre')

    def clean(self):
        cleaned_data = super().clean()
        grupo_seleccionado = cleaned_data.get('grupo')

        if self.alumno and grupo_seleccionado:
            # Validar que el alumno no esté ya en un grupo de este nivel
            # Es decir, un alumno solo puede tener UNA asignación de grupo para un NivelIngles dado.
            # Obtenemos el nivel del grupo seleccionado
            nivel_del_grupo_seleccionado = grupo_seleccionado.nivel

            # Buscamos si el alumno ya tiene una asignación a un grupo de este nivel
            existing_assignment_for_level = GrupoAlumno.objects.filter(
                alumno=self.alumno,
                grupo__nivel=nivel_del_grupo_seleccionado
            ).exclude(pk=self.instance.pk if self.instance else None).first()

            if existing_assignment_for_level:
                raise forms.ValidationError(
                    f"Este alumno ya está asignado al grupo '{existing_assignment_for_level.grupo.nombre}' "
                    f"para el nivel '{nivel_del_grupo_seleccionado.nombre} - {nivel_del_grupo_seleccionado.sub_nivel}'. "
                    "Un alumno solo puede estar en un grupo por nivel."
                )
        return cleaned_data
