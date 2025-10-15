import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_session
from app.models import Post, User


# ------------------------------------------
# 1️⃣  Base SQLite en mémoire partagée
# ------------------------------------------
TEST_DATABASE_URL = "sqlite://"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # ✅ permet de réutiliser la même connexion
)


# ------------------------------------------
# 2️⃣  Setup / teardown
# ------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Crée toutes les tables avant les tests."""
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)


# ------------------------------------------
# 3️⃣  Session et client
# ------------------------------------------
@pytest.fixture(scope="function")
def session():
    with Session(engine) as session:
        yield session


@pytest.fixture(scope="function")
def client(session):
    """Client FastAPI avec la session de test injectée."""
    def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
