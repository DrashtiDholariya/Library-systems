from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from config.database import get_db
from models.domain.book import Book
from schemas.v1.requests.book import BookCreate, BookUpdate
from schemas.v1.responses.book import BookResponse

router = APIRouter()

@router.post("/", response_model=BookResponse)
async def create_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).filter(Book.isbn == book.isbn))
    existing_book = result.scalars().first()
    
    if existing_book:
        raise HTTPException(status_code=400, detail="Book already exists.")
    
    new_book = Book(**book.dict())
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book

@router.get("/{isbn}", response_model=BookResponse)
async def get_book(isbn: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).filter(Book.isbn == isbn))
    book = result.scalars().first()
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")
    
    return book

@router.put("/{isbn}", response_model=BookResponse)
async def update_book(isbn: str, book_update: BookUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).filter(Book.isbn == isbn))
    book = result.scalars().first()
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")
    
    for key, value in book_update.dict().items():
        setattr(book, key, value)
    
    await db.commit()
    await db.refresh(book)
    return book

@router.delete("/{isbn}", response_model=dict)
async def delete_book(isbn: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).filter(Book.isbn == isbn))
    book = result.scalars().first()
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")
    
    await db.delete(book)
    await db.commit()
    return {"message": "Book deleted successfully"}
