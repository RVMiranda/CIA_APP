from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Alumno, NivelIngles, GrupoAlumno, Inscripcion, Reinscripcion

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
        alumnos_filtrados = alumnos_filtrados.filter(grupoalumno__nivel__nombre=nivel_filter).distinct()

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