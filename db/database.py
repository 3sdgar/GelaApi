from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración de la base de datos
# Configuración de la base de datos
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost/gela"

# Crea el motor de la base de datos. Esto es lo que se conecta a la base de datos.
# El 'pool_pre_ping=True' ayuda a evitar problemas con conexiones inactivas.
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

# Crea una clase SessionLocal para crear sesiones de base de datos.
# Cada sesión es una "conversación" con la base de datos.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# `Base` es una clase que los modelos de la base de datos heredarán.
# Les dice a SQLAlchemy que estas son las clases que corresponden a las tablas.
Base = declarative_base()

def get_db():
    """
    Función de dependencia para FastAPI que proporciona una sesión de base de datos.
    Crea una sesión, la usa y se asegura de cerrarla al finalizar.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
