import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from routers import articles, users, roles

# Configuración básica de logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

# Inicializa la aplicación FastAPI
app = FastAPI(
    title="Gela API",
    description="Una API simple con FastAPI y MySQL para gestionar usuarios y artículos.",
    version="1.0.0"
)

# Configurar CORS para permitir solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar el esquema de seguridad para que Swagger UI pida "email"
# en lugar de "username"
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/users/login",
    # Usa `description` para especificar que el campo es un email
    description="Ingrese el **email** y la contraseña para obtener un token JWT"
)

# ====================================================================
# Incluir los routers
# ====================================================================
app.include_router(articles.router)
app.include_router(users.router)
app.include_router(roles.router)

# ====================================================================
# Rutas de la API
# ====================================================================
@app.get("/", summary="Ruta de prueba", tags=["General"])
def read_root():
    """
    Ruta de prueba que retorna un mensaje de bienvenida.
    """
    return {"message": "¡Bienvenido a la Gela API!"}
