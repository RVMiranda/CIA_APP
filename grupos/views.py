from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Grupo, GrupoAlumno
from .forms import GrupoForm, GrupoAlumnoForm
from alumnos.models import NivelIngles, Alumno
from django.db.models import Q

# Create your views here.

class GrupoListView(ListView):
    model = Grupo
    template_name = 'grupos/grupos.html'
    context_object_name = 'grupos'
    paginate_by = 10 # Paginación para la lista de grupos

    def get_queryset(self):
        # Obtener el queryset base, ordenado por nivel y luego por nombre
        queryset = super().get_queryset().order_by('nivel__nombre', 'nombre')

        # Lógica de Filtrado por Nivel de Inglés
        nivel_filter = self.request.GET.get('nivel', None)
        if nivel_filter:
            queryset = queryset.filter(nivel__nombre=nivel_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener todos los niveles de inglés para el filtro del select
        context['niveles_ingles'] = NivelIngles.objects.all().order_by('nombre', 'sub_nivel')
        # Para mantener el valor seleccionado en el filtro
        context['nivel_seleccionado'] = self.request.GET.get('nivel', None)

        # Construir los parámetros de la URL para los enlaces de paginación y filtros
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            del query_params['page']
        context['query_params'] = query_params.urlencode()

        return context

class GrupoCreateView(CreateView):
    model = Grupo
    form_class = GrupoForm
    template_name = 'grupos/agregarGrupo.html' # Esta es la plantilla que acabamos de definir
    success_url = reverse_lazy('grupos:lista_grupos') # Redirige a la lista de grupos después de crear

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Nuevo Grupo'
        context['boton_submit'] = 'Guardar Grupo'
        return context

class GrupoDetailView(DetailView):
    model = Grupo
    template_name = 'grupos/detalleGrupo.html'
    context_object_name = 'grupo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grupo = self.object

        # Formulario para editar el grupo
        context['grupo_form'] = GrupoForm(instance=grupo)

        # Filtro de búsqueda
        q = self.request.GET.get('q', '').strip()

        # Alumnos disponibles (activos y no asignados a este grupo)
        disponibles = Alumno.objects.filter(activo=True) \
            .exclude(grupoalumno__grupo=grupo) \
            .order_by('apellido', 'nombre')

        if q:
            disponibles = disponibles.filter(
                Q(nombre__icontains=q) |
                Q(apellido__icontains=q) |
                Q(matricula__icontains=q)
            )

        context['available_alumnos'] = disponibles
        context['search_query'] = q

        # Formulario para asignar (solo contiene el campo "grupo")
        # pero vamos a tomar el alumno desde POST manualmente
        context['grupo_alumno_form'] = GrupoAlumnoForm(grupo=grupo)

        # Alumnos ya en el grupo
        context['alumnos_en_grupo'] = GrupoAlumno.objects.filter(
            grupo=grupo,
            alumno__activo=True
        ).select_related('alumno').order_by('alumno__apellido', 'alumno__nombre')

        context['titulo'] = f'Detalles del Grupo: {grupo.nombre}'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        grupo = self.object

        # Edición de datos de grupo
        if 'submit_grupo_form' in request.POST:
            form = GrupoForm(request.POST, instance=grupo)
            if form.is_valid():
                form.save()
            return redirect('grupos:detalleGrupo', pk=grupo.pk)

        # Asignar un alumno seleccionado
        if 'submit_assign_alumno_form' in request.POST:
            alumno_pk = request.POST.get('alumno_pk')
            alumno = get_object_or_404(Alumno, pk=alumno_pk, activo=True)
            # crear asignación si no existe
            GrupoAlumno.objects.get_or_create(alumno=alumno, grupo=grupo)
            return redirect('grupos:detalleGrupo', pk=grupo.pk)

        # ... (eliminar alumno ya lo tienes) ...
        if 'submit_remove_alumno_from_group' in request.POST:
            asignacion_id = request.POST.get('asignacion_id')
            GrupoAlumno.objects.filter(pk=asignacion_id, grupo=grupo).delete()
            return redirect('grupos:detalleGrupo', pk=grupo.pk)

        return redirect('grupos:detalleGrupo', pk=grupo.pk)