Gela API
Esta es la API de backend para el proyecto "Gela", construida con FastAPI y conectada a una base de datos MySQL.

Requisitos
Asegúrate de tener instalado lo siguiente:

Python 3.8 o superior

Guía de Configuración
Sigue estos pasos para poner a funcionar la API en tu entorno local.

1. Clona el repositorio (si aplica)
Si este es un repositorio de Git, clónalo en tu máquina. De lo contrario, solo navega a la carpeta del proyecto.

cd gelaApi

2. Crear y activar el entorno virtual
Es una buena práctica crear un entorno virtual para aislar las dependencias del proyecto.

En Windows:

python -m venv venv
venv\Scripts\activate

En macOS o Linux:

python3 -m venv venv
source venv/bin/activate

3. Instalar dependencias
Con el entorno virtual activado, instala todas las librerías necesarias (FastAPI, Uvicorn, MySQL Connector y Bcrypt).

pip install fastapi uvicorn mysql-connector-python bcrypt

4. Configurar la base de datos
Abre el archivo main.py y actualiza las credenciales de la base de datos con tu configuración local.

DB_HOST = "mysql.webcindario.com"
DB_USER = "gela"
DB_PASSWORD = "edgar321"
DB_NAME = "gela" 

5. Iniciar la API
Ejecuta el siguiente comando para iniciar el servidor de la API en modo de desarrollo. El flag --reload reiniciará el servidor automáticamente cuando guardes cambios.

python -m uvicorn main:app --reload

python -m venv venv
venv\Scripts\activate
python -m uvicorn main:app --reload --port 9000

Si todo está configurado correctamente, verás un mensaje que indica que el servidor se está ejecutando en http://127.0.0.1:8000.

6. Pruebas de la API
Página de bienvenida: Abre http://127.0.0.1:8000 en tu navegador.

Conexión a la base de datos: Abre http://127.0.0.1:8000/status para verificar la conexión.

Documentación interactiva: FastAPI genera automáticamente documentación. Puedes verla en http://127.0.0.1:8000/docs.