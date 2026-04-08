from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q, Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from datetime import timedelta, date, datetime
import calendar # Para obtener el último día del mes
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Colegiatura, Descuento, Recargo
from .forms import ColegiaturaPagoForm, DescuentoForm, RecargoForm 
from alumnos.models import Alumno, Inscripcion, Reinscripcion 
from grupos.models import GrupoAlumno

def _get_last_day_of_month(year, month):
    return calendar.monthrange(year, month)[1]

def _generate_next_month_tuition(alumno, current_colegiatura):
    # Calculamos el mes y año de la próxima colegiatura
    next_month_date = date(current_colegiatura.anio, current_colegiatura.mes, 1) + timedelta(days=32)
    next_month = next_month_date.month
    next_year = next_month_date.year

    pref = alumno.dia_pago_preferido
    # Verificamos si ya existe una colegiatura para el próximo mes y año
    if Colegiatura.objects.filter(alumno=alumno, anio=next_year, mes=next_month).exists():
        return None

    # la fecha de vencimiento para la próxima colegiatura
    last_day_next_month = _get_last_day_of_month(next_year, next_month)
    #due_day = min(5, last_day_next_month) # El día 5
    due_day = min(pref, last_day_next_month)
    
    fecha_vencimiento_next_month = date(next_year, next_month, due_day)

    new_colegiatura = Colegiatura.objects.create(
        alumno=alumno,
        anio=next_year,
        mes=next_month,
        fecha_vencimiento=fecha_vencimiento_next_month,
        monto_base=current_colegiatura.monto_base, # Mantiene el monto base del último pago
        estado_pago=Colegiatura.PENDIENTE,
    )
    return new_colegiatura


class ColegiaturaListView(LoginRequiredMixin, ListView):
    model = Colegiatura
    template_name = 'colegiaturas/colegiaturas.html'
    context_object_name = 'colegiaturas'
    paginate_by = 10 

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtros
        alumno_id = self.request.GET.get('alumno', None)
        mes = self.request.GET.get('mes', None)
        anio = self.request.GET.get('anio', None)
        estado = self.request.GET.get('estado', None)
        search_query = self.request.GET.get('q', '')

        if alumno_id:
            queryset = queryset.filter(alumno__pk=alumno_id)
        if mes:
            queryset = queryset.filter(mes=mes)
        if anio:
            queryset = queryset.filter(anio=anio)
        if estado:
            queryset = queryset.filter(estado_pago=estado)
        
        if search_query:
            queryset = queryset.filter(
                Q(alumno__nombre__icontains=search_query) |
                Q(alumno__apellido__icontains=search_query) |
                Q(alumno__matricula__icontains=search_query)
            )

        today = timezone.now().date()
        default_recargo = Recargo.objects.first()
        for c in queryset:
            if c.estado_pago == Colegiatura.PENDIENTE and c.fecha_vencimiento < today:
                c.estado_pago = Colegiatura.ATRASADO

                if not c.recargo_ref:
                    c.recargo_ref = default_recargo

                c.calcular_monto_final()
                c.save(update_fields=['estado_pago', 'recargo_aplicado', 'descuento_aplicado', 'recargo_ref'])

        return queryset.order_by('-anio', '-mes', 'alumno__apellido', 'alumno__nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['alumnos'] = Alumno.objects.filter(activo=True).order_by('nombre', 'apellido')
        context['meses'] = [(i, calendar.month_name[i]) for i in range(1, 13)]
        context['anios'] = range(timezone.now().year - 2, timezone.now().year + 3)
        context['estados_pago'] = Colegiatura.ESTADO_CHOICES

        # Para mantener los valores seleccionados en los filtros
        context['alumno_seleccionado'] = self.request.GET.get('alumno', '')
        context['mes_seleccionado'] = self.request.GET.get('mes', '')
        context['anio_seleccionado'] = self.request.GET.get('anio', '')
        context['estado_seleccionado'] = self.request.GET.get('estado', '')
        context['search_query'] = self.request.GET.get('q', '')

        query_params = self.request.GET.copy()
        if 'page' in query_params:
            del query_params['page']
        context['query_params'] = query_params.urlencode()

        return context

class ColegiaturaDetailView(LoginRequiredMixin, DetailView):
    model = Alumno
    template_name = 'colegiaturas/detalleColegiatura.html'
    context_object_name = 'alumno'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        alumno = self.get_object()
        hoy = timezone.now().date()

        colegiaturas = Colegiatura.objects.filter(alumno=alumno).order_by('anio', 'mes')
        default_recargo = Recargo.objects.first()

        for c in colegiaturas:
            # Si ya venció y no está "Pagado", lo marcamos Atrasado
            if c.fecha_vencimiento < hoy and c.estado_pago != Colegiatura.PAGADO:
                c.estado_pago = Colegiatura.ATRASADO
                # Aseguramos que tenga recargo_ref
                if not c.recargo_ref:
                    c.recargo_ref = default_recargo

            c.calcular_monto_final()

            c.save(update_fields=[
                'estado_pago',
                'recargo_aplicado',
                'descuento_aplicado',
                'recargo_ref'
            ])

        context['colegiaturas'] = colegiaturas
        context['pago_form']  = ColegiaturaPagoForm()
        context['last_generated_colegiatura'] = colegiaturas.order_by('-anio','-mes').first()
        context['titulo']     = f'Historial de Colegiaturas de {alumno.nombre} {alumno.apellido}'
        
        # Obtener el grupo actual para mostrar info académica
        grupo_actual = GrupoAlumno.objects.filter(alumno=alumno).select_related('grupo', 'grupo__nivel').first()
        context['grupo_actual'] = grupo_actual
        
        return context

    def post(self, request, *args, **kwargs):
        alumno = self.get_object()
        
        if 'mark_as_paid' in request.POST:
            colegiatura_id = request.POST.get('colegiatura_id')
            colegiatura = get_object_or_404(Colegiatura, pk=colegiatura_id, alumno=alumno)
            
            pago_form = ColegiaturaPagoForm(request.POST, instance=colegiatura)
            
            if pago_form.is_valid():
                colegiatura = pago_form.save(commit=False)
                pago_real = pago_form.cleaned_data['fecha_pago']
                colegiatura.fecha_pago   = pago_real
                colegiatura.monto_pagado = pago_form.cleaned_data['monto_pagado']
                colegiatura.estado_pago  = Colegiatura.PAGADO
                colegiatura.fecha_auditoria_pago = timezone.now()

                # el recargo siempre se aplica si paga después de vencimiento
                default_recargo = Recargo.objects.first()
                colegiatura.recargo_ref = default_recargo

                # descuento automático si paga con suficiente antelación
                descuentos = Descuento.objects.order_by('-meses_anticipo')
                aplicable = None
                for d in descuentos:
                    mes_diff = (
                        (colegiatura.fecha_vencimiento.year - pago_real.year) * 12 +
                        (colegiatura.fecha_vencimiento.month - pago_real.month)
                    )
                    if mes_diff >= d.meses_anticipo:
                        aplicable = d
                        break

                colegiatura.descuento_ref = aplicable       

                colegiatura.calcular_monto_final()
                colegiatura.save()

                _generate_next_month_tuition(alumno, colegiatura)
                
                return redirect('colegiaturas:historial_colegiaturas_alumno', pk=alumno.pk)
            else:
                context = self.get_context_data(object=alumno)
                context['pago_form'] = pago_form
                return render(request, self.template_name, context)
        
        return redirect('colegiaturas:historial_colegiaturas_alumno', pk=alumno.pk)

def print_colegiatura_view(request, pk):
    colegiatura = get_object_or_404(Colegiatura, pk=pk)

    if request.method == 'POST':
        periodo_custom = request.POST.get('periodo_pago')
        rango_custom = request.POST.get('rango_periodo')
        update_fields = []
        
        if periodo_custom is not None:
            colegiatura.periodo_pago = periodo_custom
            update_fields.append('periodo_pago')
            
        if rango_custom is not None:
            colegiatura.rango_periodo = rango_custom
            update_fields.append('rango_periodo')
            
        if update_fields:
            colegiatura.save(update_fields=update_fields)

    context = {
        'object': colegiatura,
        'type': 'colegiatura',
        'periodo_impresion': colegiatura.generar_periodo_sugerido(),
        'rango_impresion': colegiatura.generar_rango_sugerido()
    }
    return render(request, 'base/reciboPrint.html', context)

@login_required
def cobros_por_dia(request):
    fecha_str = request.GET.get('fecha')
    if fecha_str:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    else:
        # Usar localtime para obtener la fecha correcta configurada en TIME_ZONE
        fecha = timezone.localtime(timezone.now()).date()
        fecha_str = fecha.strftime('%Y-%m-%d')

    # 1. Colegiaturas PAGADAS en esa fecha
    colegiaturas = Colegiatura.objects.filter(
        Q(fecha_auditoria_pago__date=fecha) | Q(fecha_auditoria_pago__isnull=True, fecha_pago=fecha),
        estado_pago=Colegiatura.PAGADO
    ).select_related('alumno')

    # 2. Inscripciones realizadas en esa fecha
    inscripciones = Inscripcion.objects.filter(
        fecha_inscripcion=fecha
    ).select_related('alumno', 'nivel')

    # 3. Reinscripciones realizadas en esa fecha
    reinscripciones = Reinscripcion.objects.filter(
        fecha_reinscripcion=fecha
    ).select_related('alumno', 'nivel')

    # Totales
    total_colegiaturas = colegiaturas.aggregate(Sum('monto_pagado'))['monto_pagado__sum'] or 0
    total_inscripciones = inscripciones.aggregate(Sum('monto'))['monto__sum'] or 0
    total_reinscripciones = reinscripciones.aggregate(Sum('monto'))['monto__sum'] or 0

    total_dia = total_colegiaturas + total_inscripciones + total_reinscripciones

    # Unificar lista para el template
    lista_cobros = []

    for c in colegiaturas:
        lista_cobros.append({
            'alumno': c.alumno,
            'concepto': f"Colegiatura {c.get_mes_display()} {c.anio}",
            'monto_base': c.monto_base,
            'descuento_aplicado': c.descuento_aplicado,
            'recargo_aplicado': c.recargo_aplicado,
            'monto_pagado': c.monto_pagado,
        })

    for i in inscripciones:
        lista_cobros.append({
            'alumno': i.alumno,
            'concepto': f"Inscripción - {i.nivel}",
            'monto_base': i.monto,
            'descuento_aplicado': 0,
            'recargo_aplicado': 0,
            'monto_pagado': i.monto,
        })
    
    for r in reinscripciones:
        lista_cobros.append({
            'alumno': r.alumno,
            'concepto': f"Reinscripción - {r.nivel}",
            'monto_base': r.monto,
            'descuento_aplicado': 0,
            'recargo_aplicado': 0,
            'monto_pagado': r.monto,
        })

    context = {
        'fecha': fecha,
        'fecha_str': fecha_str,
        'cobros': lista_cobros,
        'total_dia': total_dia,
    }
    return render(request, 'colegiaturas/cobros_por_dia.html', context)
