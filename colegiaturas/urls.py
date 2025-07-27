from django.urls import path, include
from .views import ColegiaturaListView, ColegiaturaDetailView, print_colegiatura_view

app_name = 'colegiaturas'

urlpatterns = [
    path('payments/', ColegiaturaListView.as_view(), name='lista_colegiaturas'),
    path('payments/student/<int:pk>/', ColegiaturaDetailView.as_view(), name='historial_colegiaturas_alumno'),
    path('payments/student/<int:pk>/print/', print_colegiatura_view, name='print_colegiatura'),
]