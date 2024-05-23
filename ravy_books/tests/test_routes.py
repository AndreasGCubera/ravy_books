import os

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from src.models import Base, Author as ModelAuthor


# Configura la base de datos de prueba
engine = create_engine("postgresql+psycopg2://postgres:password@db:5432/book_db")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def setup_database():
    # Aquí puedes añadir datos iniciales a tu base de datos de prueba si es necesario
    author = ModelAuthor(name="Author Test", age=50, nationality="Testland")
    db = TestingSessionLocal()
    db.add(author)
    db.commit()
    db.close()

    yield

    # Limpieza después de los tests
    Base.metadata.drop_all(bind=engine)


def test_add_book(client, setup_database):
    response = client.post("/add-book/", json={"title": "Test Book", "rating": 5, "author_id": 1})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Book"
    assert data["rating"] == 5
    assert data["author_id"] == 1
