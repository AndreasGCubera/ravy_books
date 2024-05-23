import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi_sqlalchemy import DBSessionMiddleware, db

from src.models import Author as ModelAuthor
from src.models import Book
from src.models import Book as ModelBook
from src.schema import Author as SchemaAuthor
from src.schema import Book as SchemaBook

load_dotenv(".env")

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])


@app.get("/")
async def root():
    return {"message": "Hello and welcome to Ravy's Books!"}


@app.post("/add-book/", response_model=SchemaBook)
def add_book(book: SchemaBook):
    db_book = ModelBook(title=book.title, rating=book.rating, author_id=book.author_id)
    db.session.add(db_book)
    db.session.commit()
    return db_book


@app.delete("/delete-book/{book_id}")
def del_book(book_id: int):
    book = db.session.query(ModelBook).get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.session.delete(book)
    db.session.commit()
    return


@app.post("/add-author/", response_model=SchemaAuthor)
def add_author(author: SchemaAuthor):
    db_author = ModelAuthor(name=author.name, age=author.age, nationality=author.nationality)
    db.session.add(db_author)
    db.session.commit()
    return db_author


@app.delete("/delete-author/{author_id}")
def del_author(author_id: int):
    author = db.session.query(ModelAuthor).get(author_id)
    authors_book = db.session.query(ModelBook).get(author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    if authors_book:
        raise HTTPException(status_code=400, detail="Author has books assigned and can't be deleted")
    db.session.delete(author)
    db.session.commit()
    return


@app.get("/books/")
def get_books():
    books = db.session.query(Book).all()

    return books


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
