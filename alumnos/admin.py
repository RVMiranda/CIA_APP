from django.contrib import admin

# Register your models here.
from .models import Alumno, Inscripcion, NivelIngles, Reinscripcion

admin.site.register(Alumno)
admin.site.register(NivelIngles)
admin.site.register(Inscripcion)
admin.site.register(Reinscripcion)

