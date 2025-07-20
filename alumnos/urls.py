from django.urls import path, include
from . import views

app_name = 'alumnos'

urlpatterns = [
    path('students/', views.alumnos_view, name='lista_alumnos')
]