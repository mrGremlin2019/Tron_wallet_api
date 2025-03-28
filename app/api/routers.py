from fastapi import FastAPI, HTTPException, APIRouter
from .. import services
from ..api import schemas
from app.db.database import get_db
from app.db.db_client import DBClient

router = APIRouter(
    prefix="/tron_info",
    tags=["Tron Wallet"],
    responses={404: {"description": "Not found"}},
)


@router.post("/wallet/", response_model=schemas.QueryResponse)
def get_wallet_info(address: str):
    """Получение информации о кошельке в сети Tron и сохранение запроса в базу данных.

    Args:
        address (str): Адрес кошелька в сети Tron (начинается с 'T')

    Returns:
        QueryResponse: Информация о кошельке и времени запроса

    Raises:
        HTTPException: 404 если кошелек не найден
        HTTPException: 400 при ошибках валидации или проблемах с сетью Tron
    """
    try:
        # Получаем данные из сети Tron
        wallet_data = services.get_tron_wallet_data(address)
        if not wallet_data:
            raise HTTPException(status_code=404, detail="Wallet not found")

        # Сохраняем запрос в базу данных
        with get_db() as db:
            db_client = DBClient(db)
            db_query = db_client.create_wallet_query(schemas.WalletData(**wallet_data))
            return db_query

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


@router.get("/queries/", response_model=schemas.PaginatedResponse)
def get_queries(page: int = 1, limit: int = 10):
    """Получение истории запросов с пагинацией.

    Args:
        page (int, optional): Номер страницы. Defaults to 1.
        limit (int, optional): Количество записей на странице. Defaults to 10.

    Returns:
        PaginatedResponse: Объект с результатами и метаданными пагинации:
            - results: Список запросов
            - total: Общее количество запросов
            - page: Текущая страница
            - limit: Количество записей на странице
    """
    with get_db() as db:
        db_client = DBClient(db)
        skip = (page - 1) * limit

        return {
            "results": db_client.get_queries(skip, limit),
            "total": db_client.get_total_queries(),
            "page": page,
            "limit": limit,
        }
