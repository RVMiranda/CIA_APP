from django.db import models

# Create your models here.
class NivelIngles(models.Model):
    BASICO = 'Basico'
    INTERMEDIO = 'Intermedio'
    AVANZADO = 'Avanzado'
    NIVEL_CHOICES = [ (BASICO, 'Basico'), (INTERMEDIO, 'Intermedio'), (AVANZADO, 'Avanzado'),]
    nombre = models.CharField(max_length=30, null=False, 
        verbose_name="Nombre del Nivel", choices=NIVEL_CHOICES, default=BASICO)
    sub_nivel = models.CharField(max_length=10, null=True, verbose_name="Subnivel", 
        help_text="A1, A2, B1, B2, C1, C2", blank=True, default="A1")

    class Meta:
        verbose_name = "Nivel de Ingles"
        verbose_name_plural = "Niveles de Ingles"
        ordering = ['nombre', 'sub_nivel']
        unique_together = ('nombre', 'sub_nivel')

    def __str__(self):
        return f"{self.nombre} - {self.sub_nivel}" if self.sub_nivel else self.nombre

class Alumno(models.Model):
    nombre = models.CharField(max_length=100, null=False, verbose_name="Nombre")
    apellido = models.CharField(max_length=100, null=False, verbose_name="Apellido")
    matricula = models.CharField(max_length=12, null=False, unique=True)
    fecha_nacimiento = models.DateField(null=True, blank=True, verbose_name="Fecha de Nacimiento")
    edad = models.PositiveIntegerField(null=True, blank=True, verbose_name="Edad")
    telefono = models.CharField(max_length=15, null=True, blank=True, verbose_name="Teléfono")
    nombre_tutor = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nombre del Tutor")
    telefono_tutor = models.CharField(max_length=15, null=True, blank=True, verbose_name="Teléfono del Tutor")
    direccion = models.CharField(max_length=255, null=True, blank=True, verbose_name="Dirección")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="Fecha de Actualización")

    class Meta:
        verbose_name = "Alumno"
        verbose_name_plural = "Alumnos"
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.matricula})"

class Inscripcion(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, verbose_name="Alumno")
    nivel = models.ForeignKey(NivelIngles, on_delete=models.CASCADE, verbose_name="Nivel de Inscripción")
    fecha_inscripcion = models.DateField(auto_now_add=True, null=False, verbose_name="Fecha de Inscripción")
    monto = models.DecimalField(max_digits=10, decimal_places=2, null=False, verbose_name="Monto de Inscripción")

    class Meta:
        verbose_name = "Inscripción"
        verbose_name_plural = "Inscripciones"
        unique_together = ('alumno', 'nivel')

    def __str__(self):
        return f"Inscripción de {self.alumno.nombre} a {self.nivel} en {self.fecha_inscripcion}"

class Reinscripcion(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, verbose_name="Alumno")
    nivel = models.ForeignKey(NivelIngles, on_delete=models.CASCADE, verbose_name="Nivel de Reinscripción")
    fecha_reinscripcion = models.DateField(auto_now_add=True, null=False, verbose_name="Fecha de Reinscripción")
    monto = models.DecimalField(max_digits=10, decimal_places=2, null=False, verbose_name="Monto de Reinscripción")

    class Meta:
        verbose_name = "Reinscripción"
        verbose_name_plural = "Reinscripciones"
        unique_together = ('alumno', 'nivel')

    def __str__(self):
        return f"Reinscripción de {self.alumno.nombre} a {self.nivel} en {self.fecha_reinscripcion}"

class GrupoAlumno(models.Model):
    nombre = models.CharField(max_length=100, null=False, verbose_name="Nombre del Grupo")
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, verbose_name="Alumno")
    nivel = models.ForeignKey(NivelIngles, on_delete=models.CASCADE, verbose_name="Nivel del Grupo")

    class Meta:
        verbose_name = "Grupo de Alumno"
        verbose_name_plural = "Grupos de Alumnos"
        unique_together = ('alumno', 'nivel')

    def __str__(self):
        return f"Grupo '{self.nombre}' - {self.alumno.nombre} ({self.nivel.nombre})"

