import pytest
from fastapi.testclient import TestClient
from app.config import settings
from app.db.database import Base, engine, get_db
from app.db.db_client import DBClient
from app.main import app

# Фикстуры
@pytest.fixture(scope="session")
def setup_db():
    """Удаление/Создание всех таблиц в БД"""
    assert settings.MODE == "TEST"
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    engine.dispose()


@pytest.fixture
def db_session(setup_db):
    """Подключение к БД"""
    with get_db() as session:
        yield session


@pytest.fixture
def db_client(db_session):
    """Вызов класса для работы с БД"""
    return DBClient(db_session)

@pytest.fixture
def api_client(db_session):
    """Фикстура для тестирования API"""

    app.dependency_overrides[get_db] = db_session
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def mock_tron(monkeypatch):
    """Мокируем вызовы к Tron API"""

    def mock_get_wallet_data(address: str):
        if address == "invalid_address":
            return {"detail": "Wallet not found"}  # Исправляем ошибку возврата
        return {
            "address": address,
            "bandwidth": 1000,
            "energy": 500,
            "trx_balance": 1000000
        }

    monkeypatch.setattr("app.services.get_tron_wallet_data", mock_get_wallet_data)
