from sqlalchemy import text
from app.api.schemas import QueryResponse

TEST_WALLET = "TQrY8tryqsYVCYS3MFbtffiPp2ccyn4STm"


class TestWalletAPI:
    """Класс для тестирования Wallet API"""

    def test_get_wallet_info(self, api_client, db_session):
        """Тест получения информации о кошельке"""
        initial_count = self.get_wallet_count(db_session)

        response = api_client.post(f"/tron_info/wallet/?address={TEST_WALLET}")
        response_data = response.json()

        assert response.status_code == 200
        QueryResponse(**response_data)  # Валидация схемы

        assert self.get_wallet_count(db_session) == initial_count + 1

    def test_invalid_wallet_address(self, api_client):
        """Тест обработки невалидного адреса кошелька"""
        response = api_client.post("/tron_info/wallet/?address=invalid_address")

        assert response.status_code == 400
        assert response.json()["detail"] in ["Wallet not found", "Error: 'invalid_address'"]

    def test_queries_pagination(self, api_client, db_session):
        """Тест пагинации"""
        # Очищаем БД перед тестом
        db_session.execute(text("DELETE FROM wallet_queries"))
        db_session.commit()

        # Создаем тестовые данные
        for _ in range(3):
            api_client.post(f"/tron_info/wallet/?address={TEST_WALLET}")

        # Проверяем пагинацию
        response = api_client.get("/tron_info/queries/?page=1&limit=2")
        data = response.json()

        assert response.status_code == 200
        assert len(data["results"]) == 2
        assert data["total"] == 3
        assert data["page"] == 1

    @staticmethod
    def get_wallet_count(db_session):
        """Возвращает количество записей в таблице wallet_queries"""
        return db_session.execute(text("SELECT COUNT(*) FROM wallet_queries")).scalar()
