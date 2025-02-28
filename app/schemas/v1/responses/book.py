from pydantic import BaseModel

class BookResponse(BaseModel):
    isbn: str
    title: str
    author: str
    published_year: int
    available: bool
