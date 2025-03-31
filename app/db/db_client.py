from sqlalchemy.orm import Session
from app.api import schemas
from app.db import models


class DBClient:
    """Класс-обертка для работы с базой данных, предоставляющий CRUD-операции.

    Attributes:
        db (Session): Сессия SQLAlchemy для работы с базой данных
    """

    def __init__(self, db: Session):
        """Инициализация DBClient с сессией базы данных.

        Args:
            db (Session): Сессия SQLAlchemy
        """
        self.db = db

    def create_wallet_query(self, query: schemas.WalletData):
        """Создает и сохраняет в БД запись о запросе информации о кошельке.

        Args:
            query (schemas.WalletData): Данные о кошельке для сохранения,
                включая:
                - address (str): Адрес кошелька
                - bandwidth (int): Пропускная способность
                - energy (int): Энергия
                - trx_balance (int): Баланс TRX

        Returns:
            models.WalletQuery: Созданная запись в БД

        Raises:
            ValueError: Если произошла ошибка при сохранении в базу данных
            sqlalchemy.exc.SQLAlchemyError: При проблемах с подключением к БД

        Note:
            Автоматически устанавливает текущее время для query_time
        """
        try:
            db_query = models.WalletQuery(
                wallet_address=query.address,
                bandwidth=query.bandwidth,
                energy=query.energy,
                trx_balance=query.trx_balance
            )
            self.db.add(db_query)
            self.db.commit()
            self.db.refresh(db_query)
            return db_query
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Failed to create wallet query: {str(e)}")


    def get_queries(self, skip: int = 0, limit: int = 10) -> list[dict]:
        """Получает список запросов из БД с пагинацией.

        Args:
            skip (int, optional): Количество записей для пропуска. Defaults to 0.
            limit (int, optional): Максимальное количество возвращаемых записей.
                Defaults to 10.

        Returns:
            list[dict]: Список словарей с информацией о запросах, где каждый словарь содержит:
                - wallet_address (str): Адрес кошелька
                - bandwidth (int): Пропускная способность
                - energy (int): Энергия
                - trx_balance (int): Баланс TRX
                - query_time (datetime): Время выполнения запроса

        Note:
            Результаты сортируются по времени запроса (новые сначала)
        """
        query = self.db.query(
            models.WalletQuery.wallet_address,
            models.WalletQuery.bandwidth,
            models.WalletQuery.energy,
            models.WalletQuery.trx_balance,
            models.WalletQuery.query_time
        ).order_by(
            models.WalletQuery.query_time.desc()
        ).offset(skip).limit(limit)

        return [dict(q._asdict()) for q in query]

    def get_total_queries(self):
        """Получает общее количество запросов в базе данных.

        Returns:
            int: Общее количество сохраненных запросов
        """
        return self.db.query(models.WalletQuery).count()
