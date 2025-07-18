# Usa una imagen oficial de Python
FROM python:3.9-slim

# Evita que Python genere archivos .pyc
ENV PYTHONDONTWRITEBYTECODE 1
# Asegura que la salida se muestre en consola
ENV PYTHONUNBUFFERED 1

# Establece el directorio de trabajo en /app
WORKDIR /app

# Instala las dependencias
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia el código de la aplicación
COPY . /app/

EXPOSE 8001

# Comando por defecto: para desarrollo, ejecuta el servidor de Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
