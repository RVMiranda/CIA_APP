from django.db import models
from django.utils import timezone
from alumnos.models import Alumno
from datetime import timedelta, date
import calendar
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
        ordering = ['meses_anticipo']

    def __str__(self):
        return f"{self.descripcion} ({self.porcentaje*100:.0f}%)"

class Recargo(models.Model):
    descripcion = models.CharField(max_length=255, null=False, verbose_name="Descripción del Recargo")
    porcentaje_por_dia = models.DecimalField(max_digits=5, decimal_places=2, null=False, 
        verbose_name="Porcentaje por Día", help_text="Ej. 0.01 para 1% diario")

    class Meta:
        verbose_name = "Recargo"
        verbose_name_plural = "Recargos"
        ordering = ['-porcentaje_por_dia']

    def __str__(self):
        return f"{self.descripcion} ({self.porcentaje_por_dia*100:.2f}% diario)"

class Colegiatura(models.Model):
    MESES_CHOICES = [(1, "Enero"), (2, "Febrero"), (3, "Marzo"), (4, "Abril"),
    (5, "Mayo"), (6, "Junio"), (7, "Julio"), (8, "Agosto"),
    (9, "Septiembre"), (10, "Octubre"), (11, "Noviembre"), (12, "Diciembre")]
    PENDIENTE = 'Pendiente'
    PAGADO = 'Pagado'
    ATRASADO = 'Atrasado'
    ESTADO_CHOICES = [
        (PENDIENTE, 'Pendiente'),
        (PAGADO, 'Pagado'),
        (ATRASADO, 'Atrasado'),
    ]
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, verbose_name="Alumno")
    anio = models.IntegerField(null=False, verbose_name="Año")
    mes = models.IntegerField( choices=MESES_CHOICES, default=1,
        null=False, verbose_name="Mes", help_text="1=Enero … 12=Diciembre")
    fecha_vencimiento = models.DateField(null=False, verbose_name="Fecha de Vencimiento")
    monto_base = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=650.00, verbose_name="Monto Base")
    
    # Campos que se llenan al momento del pago
    fecha_pago = models.DateField(null=True, blank=True, verbose_name="Fecha de Pago")
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Monto Pagado")
    recargo_aplicado = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Recargo Aplicado")
    descuento_aplicado = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Descuento Aplicado")
    
    # Relaciones para registrar qué descuento/recargo se aplicó
    descuento_ref = models.ForeignKey(Descuento, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Descuento Usado")
    recargo_ref = models.ForeignKey(Recargo, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Recargo Usado")

    estado_pago = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=PENDIENTE, verbose_name="Estado del Pago")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    class Meta:
        verbose_name = "Colegiatura"
        verbose_name_plural = "Colegiaturas"
        unique_together = ('alumno', 'anio', 'mes')
        ordering = ['anio', 'mes', 'alumno__apellido', 'alumno__nombre']

    def __str__(self):
        return f"Colegiatura de {self.alumno.nombre} {self.alumno.apellido} - {self.mes}/{self.anio} ({self.get_estado_pago_display()})"

    def calcular_monto_final(self):
        monto = self.monto_base
        hoy = timezone.now().date()

        # Descuento
        if self.descuento_ref and (self.fecha_pago is None or self.fecha_pago <= self.fecha_vencimiento):
            desc = self.monto_base * self.descuento_ref.porcentaje
            monto -= desc
            self.descuento_aplicado = desc
        else:
            self.descuento_aplicado = 0

        # obtenemos la referencia al modelo recargo (puede venir de self o por defecto)
        rec_ref = self.recargo_ref or Recargo.objects.first()

        # Usamos fecha_pago si existe, o hoy si aún está pendiente
        fecha_calculo = self.fecha_pago or hoy
        if rec_ref and fecha_calculo > self.fecha_vencimiento:
            dias_atraso = (fecha_calculo - self.fecha_vencimiento).days
            recargo = self.monto_base * rec_ref.porcentaje_por_dia * dias_atraso
            monto += recargo
            self.recargo_aplicado = recargo
            self.recargo_ref = rec_ref
        else:
            self.recargo_aplicado = 0

        return max(0, monto)