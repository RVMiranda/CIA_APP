from django.urls import path, include
from . import views

app_name = 'alumnos'

urlpatterns = [
    path('students/', views.alumnos_view, name='lista_alumnos'),
    path('students/add/', views.agregar_alumno, name='agregarAlumno'),
    path('students/<int:pk>/', views.alumno_detail_view, name='detalleAlumno'),
]