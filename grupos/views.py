from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Grupo, GrupoAlumno
from .forms import GrupoForm, GrupoAlumnoForm
from alumnos.models import NivelIngles, Alumno
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
        # Formulario para editar el grupo
        context['grupo_form'] = GrupoForm(instance=self.object)
        # Formulario para asignar alumnos a este grupo
        context['grupo_alumno_form'] = GrupoAlumnoForm(grupo=self.object)

        # Obtener los alumnos asignados a este grupo, filtrando solo los activos
        context['alumnos_en_grupo'] = GrupoAlumno.objects.filter(
            grupo=self.object,
            alumno__activo=True # ¡Filtrar solo alumnos activos!
        ).order_by('alumno__apellido', 'alumno__nombre')
        context['titulo'] = f'Detalles del Grupo: {self.object.nombre}'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object() # Obtener la instancia del grupo

        if 'submit_grupo_form' in request.POST: # Si se envió el formulario de edición del grupo
            form = GrupoForm(request.POST, instance=self.object)
            if form.is_valid():
                form.save()
                return redirect('grupos:detalleGrupo', pk=self.object.pk)
            else:
                context = self.get_context_data(object=self.object)
                context['grupo_form'] = form
                return self.render_to_response(context)
        elif 'submit_assign_alumno_form' in request.POST: # Si se envió el formulario de asignar alumno
            grupo_alumno_form = GrupoAlumnoForm(request.POST, grupo=self.object)
            if grupo_alumno_form.is_valid():
                asignacion = grupo_alumno_form.save(commit=False)
                asignacion.grupo = self.object
                asignacion.save()
                return redirect('grupos:detalleGrupo', pk=self.object.pk)
            else:
                context = self.get_context_data(object=self.object)
                context['grupo_alumno_form'] = grupo_alumno_form
                return self.render_to_response(context)
        elif 'submit_remove_alumno_from_group' in request.POST: # ¡Nuevo! Para eliminar alumno del grupo
            asignacion_id = request.POST.get('asignacion_id')
            if asignacion_id:
                try:
                    asignacion = GrupoAlumno.objects.get(pk=asignacion_id, grupo=self.object)
                    asignacion.delete()
                except GrupoAlumno.DoesNotExist:
                    # Manejar el error si la asignación no existe o no pertenece a este grupo
                    pass # Podrías añadir un mensaje de error aquí
            return redirect('grupos:detalleGrupo', pk=self.object.pk)

        # Si no se reconoce el botón de submit, recarga la página
        return redirect('grupos:detalleGrupo', pk=self.object.pk)