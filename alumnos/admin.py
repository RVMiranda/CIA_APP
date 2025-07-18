from django.contrib import admin

# Register your models here.
from .models import Alumno, Inscripcion, NivelIngles, Reinscripcion, GrupoAlumno

admin.site.register(Alumno)
admin.site.register(NivelIngles)
admin.site.register(Inscripcion)
admin.site.register(Reinscripcion)
admin.site.register(GrupoAlumno)
