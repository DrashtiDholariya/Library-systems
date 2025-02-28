from pydantic import BaseModel

class BookCreate(BaseModel):
    isbn: str
    title: str
    author: str
    published_year: int

class BookUpdate(BaseModel):
    title: str
    author: str
    published_year: int
    available: bool
