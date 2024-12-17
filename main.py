# Import necessary libraries
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base

# Initialize FastAPI app
app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Welcome to the Book Management System!"}

# Step 1: Database Configuration
DATABASE_URL = "mysql+mysqlconnector://admin:admin_password@localhost/book_management"

# Create a SQLAlchemy engine for connecting to the database
engine = create_engine(DATABASE_URL, echo=True)

# Create a declarative base to define the database tables
Base = declarative_base()

# Step 2: Database Table Definition
class Book(Base):
    __tablename__ = "books"  # Table name in MySQL

    id = Column(Integer, primary_key=True, index=True)  # Primary key
    title = Column(String(255), nullable=False)  # Book title
    author = Column(String(255), nullable=False)  # Author of the book
    published_year = Column(Integer)  # Year of publication
    genre = Column(String(100))  # Genre of the book
    price = Column(Float)  # Price of the book

# Step 3: Create the Database Tables
Base.metadata.create_all(bind=engine)

# Step 4: Pydantic Models for Request Validation
class BookBase(BaseModel):
    title: str = Field(..., example="The Great Gatsby")
    author: str = Field(..., example="F. Scott Fitzgerald")
    published_year: Optional[int] = Field(None, example=1925)
    genre: Optional[str] = Field(None, example="Fiction")
    price: float = Field(..., example=10.99)

class BookCreate(BookBase):
    pass  # Inherits fields from BookBase for creation

class BookResponse(BookBase):
    id: int  # Include ID when responding

    class Config:
        orm_mode = True  # Allow compatibility with ORM models

# Step 5: Session Configuration
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency: Function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Step 6: CRUD Endpoints
from fastapi import Depends
from sqlalchemy.orm import Session

# 1. Create a new book
@app.post("/books/", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """
    Endpoint to add a new book to the database.
    """
    db_book = Book(**book.dict())  # Convert Pydantic model to SQLAlchemy model
    db.add(db_book)  # Add to session
    db.commit()  # Commit to save changes
    db.refresh(db_book)  # Refresh instance with database data
    return db_book  # Return the created book

# 2. Get all books
@app.get("/books/", response_model=List[BookResponse])
def read_books(db: Session = Depends(get_db)):
    """
    Endpoint to retrieve all books from the database.
    """
    return db.query(Book).all()  # Return all books as a list

# 3. Get a book by ID
@app.get("/books/{book_id}", response_model=BookResponse)
def read_book(book_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to retrieve a single book by its ID.
    """
    book = db.query(Book).filter(Book.id == book_id).first()  # Query book by ID
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")  # Raise error if not found
    return book

# 4. Update a book by ID
@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, updated_book: BookCreate, db: Session = Depends(get_db)):
    """
    Endpoint to update an existing book by its ID.
    """
    book = db.query(Book).filter(Book.id == book_id).first()  # Query book
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")  # Error if not found

    for key, value in updated_book.dict().items():  # Update fields
        setattr(book, key, value)
    db.commit()  # Commit changes
    db.refresh(book)  # Refresh instance
    return book  # Return updated book

# 5. Delete a book by ID
@app.delete("/books/{book_id}", response_model=dict)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to delete a book by its ID.
    """
    book = db.query(Book).filter(Book.id == book_id).first()  # Query book
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")  # Error if not found

    db.delete(book)  # Delete the book
    db.commit()  # Commit changes
    return {"detail": "Book deleted successfully"}  # Return confirmation

# Step 7: Run the FastAPI server
# Run using: uvicorn main:app --reload
