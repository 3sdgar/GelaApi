from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional, List

# Esquema base para los campos de usuario
class UserBase(BaseModel):
    name: str = Field(..., max_length=255)
    email: EmailStr = Field(..., max_length=255)

# Esquema para la creación de un nuevo usuario
class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    roleId: int # Agregamos roleId

    # @validator('password')
    # def validate_password(cls, v):
    #     if not any(char.isupper() for char in v):
    #         raise ValueError('La contraseña debe contener al menos una letra mayúscula')
    #     if not any(char.islower() for char in v):
    #         raise ValueError('La contraseña debe contener al menos una letra minúscula')
    #     if not any(char.isdigit() for char in v):
    #         raise ValueError('La contraseña debe contener al menos un número')
    #     if not any(char in '!@#$%^&*()_+=-[]{}\\|;:\'",.<>/?`~' for char in v):
    #         raise ValueError('La contraseña debe contener al menos un carácter especial')
    #     return v

# Esquema para la actualización de un usuario
class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr] = Field(None, max_length=255)
    password: Optional[str] = Field(None, min_length=8)
    roleId: Optional[int] = None # roleId también es opcional para la actualización

# Esquema para la respuesta del usuario (sin password)
class User(UserBase):
    id: int
    roleId: int
    created_at: datetime
    
    class Config:
        orm_mode = True

# Esquema para el token de autenticación
class Token(BaseModel):
    access_token: str
    token_type: str

# Esquema para el login del usuario
class UserLogin(BaseModel):
    email: str
    password: str