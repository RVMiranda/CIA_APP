from django.db import models
from alumnos.models import NivelIngles, Alumno

# Create your models here.

class Grupo(models.Model):
    nombre = models.CharField(max_length=100, null=False, verbose_name="Nombre del Grupo")
    nivel = models.ForeignKey(NivelIngles, on_delete=models.PROTECT, verbose_name="Nivel Asociado")

    class Meta:
        verbose_name = "Grupo"
        verbose_name_plural = "Grupos"
        unique_together = ('nombre', 'nivel')
        ordering = ['nivel__nombre', 'nombre']

    def __str__(self):
        return f"{self.nombre} ({self.nivel.nombre} - {self.nivel.sub_nivel})"

class GrupoAlumno(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, verbose_name="Alumno")
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, verbose_name="Grupo Asignado")
    fecha_asignacion = models.DateField(auto_now_add=True, verbose_name="Fecha de Asignación")

    class Meta:
        verbose_name = "Asignación de Grupo"
        verbose_name_plural = "Asignaciones de Grupos"
        unique_together = ('alumno', 'grupo')
        ordering = ['grupo__nivel__nombre', 'grupo__nombre', 'alumno__apellido']

    def __str__(self):
        return f"{self.alumno.nombre} {self.alumno.apellido} asignado a {self.grupo.nombre} ({self.grupo.nivel.nombre})"
