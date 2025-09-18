from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# ====================================================================
# Esquemas de Pydantic para los roles
# ====================================================================

class RolBase(BaseModel):
    """
    Esquema base para la creación de roles.
    """
    rol: str = Field(..., max_length=50)

class Rol(RolBase):
    """
    Esquema completo de un rol, incluyendo su ID y fecha de creación.
    """
    id: int
    created_at: datetime

class RolUpdate(RolBase):
    """
    Esquema para la actualización de un rol.
    """
    rol: Optional[str] = None
