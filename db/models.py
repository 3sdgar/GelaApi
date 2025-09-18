from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Importa todos los modelos para que sean reconocidos por los metadatos de SQLAlchemy.
from . import article_model
from . import user_model
from . import rol_model