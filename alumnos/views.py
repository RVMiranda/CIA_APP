from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.utils import timezone
from datetime import date
import calendar
from .models import Alumno, NivelIngles, Inscripcion, Reinscripcion
from grupos.models import Grupo, GrupoAlumno
from colegiaturas.models import Colegiatura, Descuento, Recargo 
from .forms import AlumnoForm, AlumnoInscripcionForm, ReinscripcionForm
from grupos.forms import GrupoAlumnoForm
from .utils import generar_matricula
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def alumnos_view(request):
    page = request.GET.get('page', 1)
    search_query = request.GET.get('q', '')
    nivel_filter = request.GET.get('nivel', None)
    estado_filter = request.GET.get('estado', 'activo')

    if estado_filter == 'baja':
        alumnos_base_queryset = Alumno.objects.filter(activo=False)
    else:
        alumnos_base_queryset = Alumno.objects.filter(activo=True)

    alumnos_filtrados = alumnos_base_queryset.order_by('apellido', 'nombre')

    if search_query:
        search_query = search_query.strip()
        alumnos_filtrados = alumnos_filtrados.filter(
            Q(nombre__icontains=search_query) |
            Q(apellido__icontains=search_query) |
            Q(matricula__icontains=search_query)
        ).distinct()

    if nivel_filter:
        alumnos_filtrados = alumnos_filtrados.filter(grupoalumno__grupo__nivel__nombre=nivel_filter).distinct()

    paginator = Paginator(alumnos_filtrados, 10) # 10 alumnos por página

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    niveles_ingles = NivelIngles.objects.all().order_by('nombre', 'sub_nivel')

    query_params = request.GET.copy()
    if 'page' in query_params:
        del query_params['page']

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'nivel_seleccionado': nivel_filter,
        'niveles_ingles': niveles_ingles,
        'estado_seleccionado': estado_filter,
        'query_params': query_params.urlencode(),
    }

    return render(request, 'alumnos/alumnos.html', context)

@login_required
def agregar_alumno(request):
    if request.method == 'POST':
        form = AlumnoInscripcionForm(request.POST)
        if form.is_valid():
            alumno = form.save(commit=False)
            alumno.matricula = generar_matricula(alumno.nombre, alumno.apellido)
            alumno.save()

            nivel = form.cleaned_data['nivel']
            monto = form.cleaned_data['monto']
            Inscripcion.objects.create(
                alumno=alumno,
                nivel=nivel,
                monto=monto
            )

            # Generamos la primer colegiatura mensual
            today = timezone.now().date()
            current_month = today.month
            current_year = today.year

            # Día de vencimiento: el día 18 (o el último si el mes es más corto)
            last_day = _get_last_day_of_month(current_year, current_month)
            due_day = min(18, last_day)
            fecha_venc = date(current_year, current_month, due_day)

            base = 700.00 if form.cleaned_data['es_nuevo'] else 650.00
            Colegiatura.objects.create(
                alumno=alumno,
                anio=current_year,
                mes=current_month,
                fecha_vencimiento=fecha_venc,
                monto_base=base,         # 650 es el monto si es alumno antiguo
                estado_pago=Colegiatura.PENDIENTE,
            )

            return redirect('alumnos:detalleAlumno', pk=alumno.pk)
    else:
        form = AlumnoInscripcionForm(initial={'activo': True})

    return render(request, 'alumnos/agregarAlumno.html', {
        'form': form,
    })

@login_required
def alumno_detail_view(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)

    if request.method == 'POST':
        if 'submit_alumno_form' in request.POST:
            alumno_form = AlumnoForm(request.POST, instance=alumno)
            if alumno_form.is_valid():
                alumno_form.save()
                return redirect('alumnos:detalleAlumno', pk=alumno.pk)
        elif 'submit_reinscripcion_form' in request.POST:
            reinscripcion_form = ReinscripcionForm(request.POST)
            if reinscripcion_form.is_valid():
                reinscripcion = reinscripcion_form.save(commit=False)
                reinscripcion.alumno = alumno
                reinscripcion.save()
                return redirect('alumnos:detalleAlumno', pk=alumno.pk)
    else:
        alumno_form = AlumnoForm(instance=alumno)
        reinscripcion_form = ReinscripcionForm()

    # Obtenemos todas las reinscripciones del alumno para mostrarlas
    inscripciones = list(Inscripcion.objects.filter(alumno=alumno).order_by('fecha_inscripcion'))
    reinscripciones = Reinscripcion.objects.filter(alumno=alumno).order_by('-fecha_reinscripcion') 

    context = {
        'alumno': alumno,
        'alumno_form': alumno_form,
        'reinscripcion_form': reinscripcion_form,
        'reinscripciones': reinscripciones,
        'inscripciones':  inscripciones,
    }
    return render(request, 'alumnos/detalleAlumno.html', context)

def _get_last_day_of_month(year, month):
    return calendar.monthrange(year, month)[1]

def print_inscripcion_view(request, pk):
    inscripcion = get_object_or_404(Inscripcion, pk=pk)
    context = {
        'object': inscripcion,
        'type': 'inscripcion'
    }
    return render(request, 'base/reciboPrint.html', context)

def print_reinscripcion_view(request, pk):
    reinscripcion = get_object_or_404(Reinscripcion, pk=pk)
    context = {
        'object': reinscripcion,
        'type': 'reinscripcion'
    }
    return render(request, 'base/reciboPrint.html', context)
