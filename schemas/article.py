from pydantic import BaseModel, Field

class ArticleBase(BaseModel):
    name: str = Field(..., max_length=255)
    type: str = Field(..., max_length=255)
    description: str = Field(...)
    price: float = Field(..., gt=0)
    available_quantity: int = Field(..., ge=0)

class Article(ArticleBase):
    id: int