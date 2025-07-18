from django.db import models
from django.utils import timezone
from alumnos.models import Alumno
# Create your models here.
class Descuento(models.Model):
    descripcion = models.CharField(max_length=255, null=False, verbose_name="Descripción del Descuento")
    meses_anticipo = models.IntegerField(null=False, unique=True, verbose_name="Meses de Anticipo",
        help_text="Número de meses de anticipación para aplicar el descuento")
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2, null=False, verbose_name="Porcentaje",
        help_text="Ej. 0.05 para 5%")

    class Meta:
        verbose_name = "Descuento"
        verbose_name_plural = "Descuentos"

    def __str__(self):
        return f"{self.descripcion} ({self.porcentaje*100:.0f}%)"

class Recargo(models.Model):
    descripcion = models.CharField(max_length=255, null=False, verbose_name="Descripción del Recargo")
    porcentaje_por_dia = models.DecimalField(max_digits=5, decimal_places=2, null=False, 
        verbose_name="Porcentaje por Día", help_text="Ej. 0.01 para 1% diario")

    class Meta:
        verbose_name = "Recargo"
        verbose_name_plural = "Recargos"

    def __str__(self):
        return f"{self.descripcion} ({self.porcentaje_por_dia*100:.2f}% diario)"

class Colegiatura(models.Model):
    MESES_CHOICES = [(1, "Enero"), (2, "Febrero"), (3, "Marzo"), (4, "Abril"),
    (5, "Mayo"), (6, "Junio"), (7, "Julio"), (8, "Agosto"),
    (9, "Septiembre"), (10, "Octubre"), (11, "Noviembre"), (12, "Diciembre")]
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, verbose_name="Alumno")
    anio = models.IntegerField(null=False, verbose_name="Año")
    mes = models.IntegerField( choices=MESES_CHOICES, default=1,
        null=False, verbose_name="Mes", help_text="1=Enero … 12=Diciembre")
    fecha_pago = models.DateField(null=True, blank=True, verbose_name="Fecha de Pago")
    fecha_vencimiento = models.DateField(null=False, verbose_name="Fecha de Vencimiento")
    monto_base = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=650.00, verbose_name="Monto Base")
    # rango_dias = models.IntegerField(null=False, default=30, verbose_name="Rango de Días de Pago")
    descuento = models.ForeignKey(Descuento, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Descuento Aplicado")
    recargo = models.ForeignKey(Recargo, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Recargo Aplicado")
    monto_final = models.DecimalField(max_digits=10, decimal_places=2, null=False, verbose_name="Monto Final Pagado")
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=False, verbose_name="Fecha de Registro")
    fecha_pago_actualizacion = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="Fecha de Actualización del Pago")

    class Meta:
        verbose_name = "Colegiatura"
        verbose_name_plural = "Colegiaturas"
        unique_together = ('alumno', 'anio', 'mes')

    def __str__(self):
        return f"Colegiatura de {self.alumno.nombre} {self.alumno.apellido} - {self.get_mes_display()}/{self.anio}"
