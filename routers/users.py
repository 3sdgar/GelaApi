import logging
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import bcrypt

from db.database import get_db
from db.user_model import User as DBUser
from schemas.user import User as UserSchema, UserCreate, UserUpdate
from utils.auth import create_access_token, Token, get_current_user

# Configuración básica de logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

# Inicializa el router de FastAPI
router = APIRouter(
    prefix="/users",
    tags=["Usuarios"]
)

# ====================================================================
# Rutas para la gestión de usuarios
# ====================================================================

@router.get("/", response_model=List[UserSchema], summary="Get all users")
def get_users(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    """
    Recupera todos los usuarios de la base de datos.
    Ahora requiere autenticación.
    """
    users = db.query(DBUser).all()
    return users

@router.get("/me", summary="Get current user")
def read_users_me(current_user: str = Depends(get_current_user)):
    """
    Obtiene la información del usuario autenticado.
    """
    return {"email": current_user}

@router.post("/login", response_model=Token, summary="User login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Verifica las credenciales del usuario y genera un token JWT.
    Use el email en el campo de username.
    """
    db_user = db.query(DBUser).filter(DBUser.email == form_data.username).first()

    if not db_user or not bcrypt.verify(form_data.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    access_token = create_access_token(data={"sub": db_user.email})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED, summary="Create a new user")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo usuario con la contraseña cifrada.
    """
    try:
        # Revisa si el email ya existe
        existing_user = db.query(DBUser).filter(DBUser.email == user.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )
        
        # Cifra la contraseña antes de guardarla
        hashed_password = bcrypt.hash(user.password)

        # Crea el nuevo objeto de usuario para la base de datos
        db_user = DBUser(name=user.name, email=user.email, password=hashed_password, roleId=user.roleId)
        
        # Agrega el nuevo usuario a la sesión y confirma los cambios
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        # Retorna el usuario creado (excluyendo la contraseña)
        return db_user
    except HTTPException as http_exc:
        raise http_exc
    except SQLAlchemyError as error:
        db.rollback()
        logger.error(f"Error al intentar agregar un nuevo usuario: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user"
        )


@router.put("/{user_id}", response_model=UserSchema, summary="Update a user")
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    """
    Actualiza un usuario existente por su ID.
    Requiere autenticación.
    """
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Actualizar solo los campos que se proporcionan en la solicitud
    if user_data.name is not None:
        db_user.name = user_data.name
    if user_data.email is not None:
        db_user.email = user_data.email
    if user_data.password is not None:
        db_user.password = bcrypt.hash(user_data.password)
    if user_data.roleId is not None:
        db_user.roleId = user_data.roleId

    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a user")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    """
    Elimina un usuario por su ID.
    Requiere autenticación.
    """
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return