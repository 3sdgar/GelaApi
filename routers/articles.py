import logging
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from db.database import get_db
from schemas.article import Article as ArticleSchema, ArticleBase
from db.article_model import Article as DBArticle
from utils.auth import get_current_user

# Configuración básica de logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

# Inicializa el router de FastAPI
router = APIRouter(
    prefix="/articles",
    tags=["Artículos"]
)

# ====================================================================
# Rutas para la gestión de artículos (protegidas)
# ====================================================================

@router.get("/", response_model=List[ArticleSchema], summary="Get all articles")
def get_articles(db: Session = Depends(get_db)):
    articles = db.query(DBArticle).all()
    return articles

@router.get("/{article_id}", response_model=ArticleSchema, summary="Get an article by ID")
def get_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(DBArticle).filter(DBArticle.id == article_id).first()
    if article is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    return article

@router.post("/", response_model=ArticleSchema, status_code=status.HTTP_201_CREATED, summary="Create a new article (protected)")
def create_article(article: ArticleBase, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    try:
        db_article = DBArticle(**article.dict())
        db.add(db_article)
        db.commit()
        db.refresh(db_article)
        return db_article
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating article: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating article")

@router.put("/{article_id}", response_model=ArticleSchema, summary="Update an article (protected)")
def update_article(article_id: int, article: ArticleBase, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_article = db.query(DBArticle).filter(DBArticle.id == article_id).first()
    if db_article is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    
    for key, value in article.dict().items():
        setattr(db_article, key, value)
    
    try:
        db.commit()
        db.refresh(db_article)
        return db_article
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error updating article: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error updating article")

@router.delete("/{article_id}", status_code=status.HTTP_200_OK, summary="Delete an article (protected)")
def delete_article(article_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_article = db.query(DBArticle).filter(DBArticle.id == article_id).first()
    if db_article is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    
    try:
        db.delete(db_article)
        db.commit()
        return {"message": "Article deleted successfully."}
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error deleting article: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error deleting article")
