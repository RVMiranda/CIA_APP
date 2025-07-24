from django.urls import path, include
from .views import ColegiaturaListView, ColegiaturaDetailView

app_name = 'colegiaturas'

urlpatterns = [
    path('payments/', ColegiaturaListView.as_view(), name='lista_colegiaturas'),
    path('payments/student/<int:pk>/', ColegiaturaDetailView.as_view(), name='historial_colegiaturas_alumno'),
]