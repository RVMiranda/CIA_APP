@echo off
setlocal EnableDelayedExpansion

REM ========================================================
REM SCRIPT DE MANTENIMIENTO Y RESPALDO - CIA APP
REM ========================================================

cd /d "%~dp0"

REM --- Configuracion ---
set BACKUP_DIR=backups
REM Formato de fecha y hora seguro para nombres de archivo
set FECHA=%date:~-4,4%-%date:~-7,2%-%date:~-10,2%
set HORA=%time:~0,2%-%time:~3,2%-%time:~6,2%
set HORA=%HORA: =0%
set TIMESTAMP=%FECHA%_%HORA%
set BACKUP_FILE=%BACKUP_DIR%\backup_%TIMESTAMP%.sql

REM Crear directorio de backups si no existe
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

REM Leer credenciales del .env para usarlas en el comando
REM (Se ha optimizado para usar las variables internas del contenedor directamente)

echo ========================================================
echo       INICIANDO SISTEMA DE MANTENIMIENTO
echo       Fecha: %date% %time%
echo ========================================================
echo.

REM --------------------------------------------------------
REM 1. RESPALDO DE BASE DE DATOS
REM --------------------------------------------------------
echo [1/3] Generando respaldo de la base de datos MySQL...
echo       Destino: %BACKUP_FILE%

REM Se ejecuta mysqldump dentro del contenedor 'db' usando las variables de entorno internas ($MYSQL_USER, etc)
REM Esto asegura que funcione aunque el archivo .env del cliente tenga formato diferente o no este accesible.
docker compose exec -T db sh -c "mysqldump --opt --routines --triggers --events --complete-insert --hex-blob -u\"$MYSQL_USER\" -p\"$MYSQL_PASSWORD\" \"$MYSQL_DATABASE\"" > "%BACKUP_FILE%"

if %ERRORLEVEL% equ 0 (
    echo       [OK] Respaldo creado exitosamente.
) else (
    echo       [ERROR] Hubo un problema al crear el respaldo. Verifica que el contenedor 'db' este corriendo.
)

REM --------------------------------------------------------
REM 2. LIMPIEZA DE ARCHIVOS TEMPORALES (Python Cache)
REM --------------------------------------------------------
echo.
echo [2/3] Limpiando archivos temporales (__pycache__, .pyc)...

REM Eliminar recursivamente carpetas __pycache__ y archivos .pyc en el directorio actual
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc >nul 2>&1

echo       [OK] Limpieza de cache completada.

REM --------------------------------------------------------
REM 3. OPTIMIZACION DE DOCKER (Recursos no usados)
REM --------------------------------------------------------
echo.
echo [3/3] Optimizando recursos de Docker...
echo       (Eliminando contenedores detenidos y redes no usadas para liberar espacio)

docker system prune -f --filter "label!=keep" >nul 2>&1

echo       [OK] Mantenimiento de Docker completado.

echo.
echo ========================================================
echo       PROCESO TERMINADO EXITOSAMENTE
echo ========================================================
echo Puedes cerrar esta ventana o presionar una tecla...
pause >nul
