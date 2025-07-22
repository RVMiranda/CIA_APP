from django.urls import path
from .views import GrupoListView, GrupoCreateView, GrupoDetailView
# from .views import GrupoListView, GrupoCreateView, GrupoUpdateView, GrupoDeleteView

app_name = 'grupos'

urlpatterns = [
    path('groups/', GrupoListView.as_view(), name='lista_grupos'),
    path('groups/add/', GrupoCreateView.as_view(), name='agregarGrupo'),
    path('groups/<int:pk>/', GrupoDetailView.as_view(), name='detalleGrupo'),
]
