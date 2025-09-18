from sqlalchemy import Integer, String,DateTime, Time, Boolean, Column, Text, DECIMAL  
from sqlalchemy.sql import func
from .models import Base

class Article(Base):
   
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    type = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(DECIMAL(10,2), nullable=False)
    available_quantity = Column(Integer, nullable=False)
    create_at = Column(DateTime(timezone=True),server_default=func.now())

    