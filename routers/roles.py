from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List

from db.database import get_db
from db.rol_model import Rol as DBRol
from schemas.rol import Rol as RolSchema, RolBase, RolUpdate

router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)

# ====================================================================
# Rutas para la gestión de roles
# ====================================================================

@router.get("/", response_model=List[RolSchema], summary="Obtener todos los roles")
def get_all_roles(db: Session = Depends(get_db)):
    """
    Obtiene una lista de todos los roles disponibles en la base de datos.
    """
    roles = db.query(DBRol).all()
    return roles

@router.get("/{rol_id}", response_model=RolSchema, summary="Obtener un rol por ID")
def get_rol_by_id(rol_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un rol específico a partir de su ID.
    """
    rol = db.query(DBRol).filter(DBRol.id == rol_id).first()
    if not rol:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol not found")
    return rol

@router.post("/", response_model=RolSchema, status_code=status.HTTP_201_CREATED, summary="Crear un nuevo rol")
def create_new_rol(rol: RolBase, db: Session = Depends(get_db)):
    """
    Crea un nuevo rol en la base de datos.
    """
    db_rol = DBRol(**rol.model_dump())
    db.add(db_rol)
    try:
        db.commit()
        db.refresh(db_rol)
        return db_rol
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al crear el rol: {e}")

@router.put("/{rol_id}", response_model=RolSchema, summary="Actualizar un rol")
def update_rol(rol_id: int, rol: RolUpdate, db: Session = Depends(get_db)):
    """
    Actualiza la información de un rol existente.
    """
    db_rol = db.query(DBRol).filter(DBRol.id == rol_id).first()
    if not db_rol:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol not found")

    if rol.rol:
        db_rol.rol = rol.rol
    
    db.commit()
    db.refresh(db_rol)
    return db_rol

@router.delete("/{rol_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar un rol")
def delete_rol(rol_id: int, db: Session = Depends(get_db)):
    """
    Elimina un rol de la base de datos.
    """
    db_rol = db.query(DBRol).filter(DBRol.id == rol_id).first()
    if not db_rol:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol not found")

    db.delete(db_rol)
    db.commit()
    return
