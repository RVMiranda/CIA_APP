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

# Create your views here.
def alumnos_view(request):
    """
    Vista para mostrar la lista de alumnos (activos o de baja) con paginación,
    filtrado por nivel de inglés y búsqueda por nombre, apellido o matrícula.
    """
    page = request.GET.get('page', 1)
    search_query = request.GET.get('q', '')
    nivel_filter = request.GET.get('nivel', None)
    # Nuevo parámetro para el estado del alumno: 'activo' por defecto, puede ser 'baja'
    estado_filter = request.GET.get('estado', 'activo')

    # 1. Determinar el queryset base según el estado (activo/baja)
    if estado_filter == 'baja':
        alumnos_base_queryset = Alumno.objects.filter(activo=False)
    else: # Por defecto o si es 'activo'
        alumnos_base_queryset = Alumno.objects.filter(activo=True)

    # Ordenar el queryset base
    alumnos_filtrados = alumnos_base_queryset.order_by('apellido', 'nombre')

    # 2. Aplicar la búsqueda por nombre, apellido o matrícula
    if search_query:
        search_query = search_query.strip()
        alumnos_filtrados = alumnos_filtrados.filter(
            Q(nombre__icontains=search_query) | # Busca por nombre (insensible a mayúsculas/minúsculas)
            Q(apellido__icontains=search_query) | # Busca por apellido
            Q(matricula__icontains=search_query) # Busca por matrícula
        ).distinct() # Usa distinct() para evitar duplicados si un alumno coincide en múltiples campos

    # 3. Aplicar el filtro por nivel de inglés
    # Este filtro se aplica a los alumnos que pertenecen a un GrupoAlumno con el nivel seleccionado
    if nivel_filter:
        alumnos_filtrados = alumnos_filtrados.filter(grupoalumno__grupo__nivel__nombre=nivel_filter).distinct()

    # 4. Realizar la paginación
    paginator = Paginator(alumnos_filtrados, 10) # 10 alumnos por página, puedes ajustar este número

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un entero, entrega la primera página.
        page_obj = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera de rango (ej. 9999), entrega la última página de resultados.
        page_obj = paginator.page(paginator.num_pages)

    # Obtener todos los niveles de inglés para el filtro del select
    niveles_ingles = NivelIngles.objects.all().order_by('nombre', 'sub_nivel')

    # Construir los parámetros de la URL para los enlaces de paginación y filtros
    # Esto es crucial para mantener los filtros y la búsqueda al cambiar de página
    query_params = request.GET.copy()
    if 'page' in query_params:
        del query_params['page'] # Eliminar 'page' para construir la base de la URL

    context = {
        'page_obj': page_obj, # Contiene los alumnos para la página actual
        'search_query': search_query, # Para mantener el valor en el campo de búsqueda
        'nivel_seleccionado': nivel_filter, # Para mantener el valor seleccionado en el filtro de nivel
        'niveles_ingles': niveles_ingles,
        'estado_seleccionado': estado_filter, # Para que el HTML sepa qué botón de estado está activo
        'query_params': query_params.urlencode(), # Parámetros para los enlaces de paginación y filtros
    }

    return render(request, 'alumnos/alumnos.html', context)

def agregar_alumno(request):
    if request.method == 'POST':
        form = AlumnoInscripcionForm(request.POST)
        if form.is_valid():
            # 1) Guardar Alumno (sin matricula)
            alumno = form.save(commit=False)
            alumno.matricula = generar_matricula(alumno.nombre, alumno.apellido)
            alumno.save()

            # 2) Guardar Inscripcion ligada
            nivel = form.cleaned_data['nivel']
            monto = form.cleaned_data['monto']
            Inscripcion.objects.create(
                alumno=alumno,
                nivel=nivel,
                monto=monto
            )

            # --- Generar la primera colegiatura mensual ---
            today = timezone.now().date()
            current_month = today.month
            current_year = today.year

            # Día de vencimiento: el día 5 (o el último si el mes es más corto)
            last_day = _get_last_day_of_month(current_year, current_month)
            due_day = min(5, last_day)
            fecha_venc = date(current_year, current_month, due_day)

            # Crear Colegiatura
            Colegiatura.objects.create(
                alumno=alumno,
                anio=current_year,
                mes=current_month,
                fecha_vencimiento=fecha_venc,
                monto_base=650.00,         # usa tu valor por defecto
                estado_pago=Colegiatura.PENDIENTE,
                # los demás campos (fecha_pago, monto_pagado, recargo, descuento)
                # quedan en null o default según tu modelo
            )

            return redirect('alumnos:lista_alumnos')
    else:
        form = AlumnoInscripcionForm(initial={'activo': True})

    return render(request, 'alumnos/agregarAlumno.html', {
        'form': form,
    })

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
                # Mensaje de éxito o redirección
                return redirect('alumnos:detalleAlumno', pk=alumno.pk)
        elif 'submit_grupo_form' in request.POST:
            grupo_alumno_form = GrupoAlumnoForm(request.POST, alumno=alumno)
            if grupo_alumno_form.is_valid():
                grupo_alumno = grupo_alumno_form.save(commit=False)
                grupo_alumno.alumno = alumno
                grupo_alumno.save()
                # Mensaje de éxito o redirección
                return redirect('alumnos:detalleAlumno', pk=alumno.pk)
    else: # Petición GET
        alumno_form = AlumnoForm(instance=alumno) # Precarga los datos del alumno
        reinscripcion_form = ReinscripcionForm() # Formulario vacío para nueva reinscripción
        grupo_alumno_form = GrupoAlumnoForm(alumno=alumno) # Formulario vacío para nueva asignación de grupo

    # Obtener todas las reinscripciones y grupos del alumno para mostrarlas
    reinscripciones = Reinscripcion.objects.filter(alumno=alumno).order_by('-fecha_reinscripcion')
    grupos_alumno = GrupoAlumno.objects.filter(alumno=alumno).order_by('grupo__nivel__nombre', 'grupo__nombre')

    context = {
        'alumno': alumno,
        'alumno_form': alumno_form,
        'reinscripcion_form': reinscripcion_form,
        'grupo_alumno_form': grupo_alumno_form,
        'reinscripciones': reinscripciones,
        'grupos_alumno': grupos_alumno,
    }
    return render(request, 'alumnos/detalleAlumno.html', context)

def _get_last_day_of_month(year, month):
    return calendar.monthrange(year, month)[1]