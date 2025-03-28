from fastapi import FastAPI
from .db import models
from app.db.database import engine
from app.api.routers import router as tron_router

app = FastAPI(
    title="Tron Wallet API",
    description="Микросервис для получения информации о кошельках в сети Tron",
    version="1.0.0"
)

# Создаём таблицы в базе данных при старте приложения
models.Base.metadata.create_all(bind=engine)

# Подключение роутера
app.include_router(tron_router)
