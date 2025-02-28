from contextlib import asynccontextmanager
from fastapi import FastAPI
from config.database import create_tables
from api.v1.routers import books

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield
    print("Application is shutting down...")

app = FastAPI(title="Library Management System", lifespan=lifespan)

app.include_router(books.router, prefix="/books", tags=["Books"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Library Management System"}
