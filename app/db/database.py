#import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
# from dotenv import load_dotenv

from app.config import settings

DB_URL = settings.DB_URL
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal  = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)


# load_dotenv()
#
# # Проверяем наличие переменной окружения DB_DPATH
# db_dpath = os.getenv("DATABASE_URL")
# if db_dpath is None:
#     raise ValueError("Переменная окружения DATABASE_URL не определена в файле .env")
#
# engine = create_engine(f"sqlite:///./{db_dpath}", connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

Base = declarative_base()

@contextmanager
def get_db():
    """
    Контекстный менеджер для работы с сессией базы данных.

    Yields:
        Session: Сессия SQLAlchemy для работы с базой данных
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Database session failed: {str(e)}")
    finally:
        db.close()