from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from datetime import timedelta, date
import calendar # Para obtener el último día del mes

from .models import Colegiatura, Descuento, Recargo
from .forms import ColegiaturaPagoForm, DescuentoForm, RecargoForm 
from alumnos.models import Alumno 

def _get_last_day_of_month(year, month):
    return calendar.monthrange(year, month)[1]

def _generate_next_month_tuition(alumno, current_colegiatura):
    # Calculamos el mes y año de la próxima colegiatura
    next_month_date = date(current_colegiatura.anio, current_colegiatura.mes, 1) + timedelta(days=32)
    next_month = next_month_date.month
    next_year = next_month_date.year

    # Verificamos si ya existe una colegiatura para el próximo mes y año
    if Colegiatura.objects.filter(alumno=alumno, anio=next_year, mes=next_month).exists():
        return None

    # la fecha de vencimiento para la próxima colegiatura
    last_day_next_month = _get_last_day_of_month(next_year, next_month)
    due_day = min(5, last_day_next_month) # El día 5
    
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


class ColegiaturaListView(ListView):
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

class ColegiaturaDetailView(DetailView):
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
        return context

    def post(self, request, *args, **kwargs):
        alumno = self.get_object()
        
        if 'mark_as_paid' in request.POST:
            colegiatura_id = request.POST.get('colegiatura_id')
            colegiatura = get_object_or_404(Colegiatura, pk=colegiatura_id, alumno=alumno)
            
            pago_form = ColegiaturaPagoForm(request.POST, instance=colegiatura)
            
            if pago_form.is_valid():
                colegiatura = pago_form.save(commit=False)
                colegiatura.fecha_pago   = pago_form.cleaned_data['fecha_pago']
                colegiatura.monto_pagado = pago_form.cleaned_data['monto_pagado']
                colegiatura.estado_pago = Colegiatura.PAGADO
                
                default_recargo = Recargo.objects.first() # Toma el primer recargo disponible
                default_descuento = Descuento.objects.first() # Toma el primer descuento disponible
                
                colegiatura.recargo_ref = default_recargo
                colegiatura.descuento_ref = default_descuento

                #colegiatura.monto_pagado = colegiatura.calcular_monto_final()
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
    context = {
        'object': colegiatura,
        'type': 'colegiatura'
    }
    return render(request, 'base/reciboPrint.html', context)
