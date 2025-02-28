from sqlalchemy import Column, String, Integer, Boolean
from config.database import Base

class Book(Base):
    __tablename__ = "books"

    isbn = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    published_year = Column(Integer)
    available = Column(Boolean, default=True)
