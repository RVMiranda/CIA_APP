from django.contrib import admin

# Register your models here.
from .models import Grupo, GrupoAlumno

admin.site.register(Grupo)
admin.site.register(GrupoAlumno)