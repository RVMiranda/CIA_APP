import random
from .models import Alumno

def generar_matricula(nombre: str, apellido: str) -> str:
    iniciales = (nombre[0] + apellido[0]).upper()
    while True:
        numeros = ''.join(random.choices('0123456789', k=4))
        codigo = f"{iniciales}{numeros}"
        if not Alumno.objects.filter(matricula=codigo).exists():
            return codigo
