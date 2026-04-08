# Guía de Actualización y Despliegue (Local)

El siguiente documento detalla el procedimiento oficial y seguro para desplegar nuevas actualizaciones de código al servidor local, garantizando la integridad de la base de datos existente.

---

## 1. Generación de Respaldo Preventivo

Antes de interrumpir el servicio o manipular los archivos del proyecto, es mandatorio generar un respaldo completo de la base de datos para prevenir pérdida de información en caso de fallo durante las migraciones.

- **Paso:** Ejecutar el archivo de tareas programadas del sistema.
  - Asegúrese de tener el contenedor en ejecución.
  - Ejecute el archivo **`mantenimiento.bat`** (ubicado en el directorio principal).
  - Verifique que se haya generado correctamente el archivo `.sql` en el directorio de `backups` y que su tamaño en disco sea válido (mayor a 0kb).

---

## 2. Detención del Servicio Actual

Es fundamental detener los contenedores sin eliminar los volúmenes de almacenamiento de datos (`db_data`), los cuales retienen toda la información de la base de datos.
- **Comando:**
  ```bash
  docker compose down
  ```
> [!WARNING]
> No agregar parámetros adicionales como `-v` al detener los servicios, ya que esto purgaría irrevocablemente toda la información contenida en la base de datos local.

---

## 3. Sustitución del Código Fuente

- Reemplace los archivos del directorio del sistema con los archivos de la nueva versión proporcionada.
- **Cuidado:** Conserve intacto el archivo local `.env` del servidor, ya que en este residen las credenciales críticas cifradas y ajustes específicos de entorno (como accesos a base de datos y puertos de red).

---

## 4. Reconstrucción y Arranque del Servicio

Una vez con el código fuente actualizado, indique al gestor de contenedores que empaquete las nuevas imágenes del servidor web respetando los volúmenes previos.

- **Comando:**
  ```bash
  docker compose up --build -d
  ```
- *Nota:* Permita aproximadamente 60 segundos posteriores a este comando para que el gestor interno de la base de datos (MySQL) logre un arranque estable antes de continuar.

---

## 5. Sincronización de Base de Datos (Migraciones)

Cuando la actualización cuenta con modificaciones a nivel de tabla (nuevas columnas, validaciones, periodos lógicos), se debe correr el asistente de migración del ORM. Este proceso crea el nuevo esquema estructural sin afectar los registros comerciales ya habitando el sistema.

- **Comando:**
  ```bash
  docker compose exec web python manage.py migrate
  ```
- Este comando acoplará la información actual al nuevo ecosistema. Al finalizar, la terminal listará un informe de éxito (`OK`) detallando las aplicaciones que fueron sincronizadas.

---

## Flujo Extraordinario: Migración a un Servidor Completamente Nuevo

Si el sistema debe instalarse en una computadora en blanco que no cuenta con volúmenes existentes, el flujo es el siguiente:

1. Ejecute la construcción inicial del sistema en blanco:
   ```bash
   docker compose up --build -d
   ```
2. Restaure el respaldo poblacional (`.sql`) usando la consola nativa:
   ```bash
   docker compose exec -T db mysql -u root -p[CONTRASEÑA_DEL_ENV] [NOMBRE_DE_BD] < backups/nombre_del_respaldo.sql
   ```
3. Ahora sí, aplique el parche de modernización a esas tablas heredadas:
   ```bash
   docker compose exec web python manage.py migrate
   ```

El sistema estará listo y funcional para operar con las nuevas características.
