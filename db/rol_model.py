from sqlalchemy import Column, Integer, String, DateTime, func
from db.database import Base

# ====================================================================
# Modelo de la tabla de roles
# ====================================================================

class Rol(Base):
    """
    Representa la tabla 'roles' en la base de datos.
    """
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    rol = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<Rol(id={self.id}, rol='{self.rol}')>"
