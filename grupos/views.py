from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Grupo, GrupoAlumno
from .forms import GrupoForm
from alumnos.models import NivelIngles

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
