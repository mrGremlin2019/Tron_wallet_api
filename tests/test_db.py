import pytest
from app.api.schemas import WalletData


# Общая функция для создания тестовых данных
def create_wallet_data(address, bandwidth, energy, trx_balance):
    return WalletData(
        address=address,
        bandwidth=bandwidth,
        energy=energy,
        trx_balance=trx_balance
    )


# Тестовые данные
TEST_WALLETS = [
    ("TAF5Lnm4Q5gFnqoH6nbTv5k3Xr8F4S7R2E", 1000, 500, 10000),
    ("GDfkfd72383jlLsdnbETdk8ej2j7gdH4Ad", 2000, 1000, 20000),
    ("YEUoe3fp2fd46d4eoAfSa9Pw26Ks0Pds7l", 3000, 1500, 30000),
]


@pytest.mark.parametrize("address,bandwidth,energy,trx_balance", TEST_WALLETS)
def test_wallet_creation(db_client, address, bandwidth, energy, trx_balance):
    """Тестирует создание и чтение кошельков с разными данными"""
    wallet = create_wallet_data(address, bandwidth, energy, trx_balance)
    db_client.create_wallet_query(wallet)

    # Проверяем последнюю добавленную запись
    last_query = db_client.get_queries(limit=1)[0]
    assert last_query['wallet_address'] == address
    assert last_query['bandwidth'] == bandwidth
    assert last_query['energy'] == energy
    assert last_query['trx_balance'] == trx_balance


def test_multiple_wallets_count(db_client):
    """Тестирует количество записей после нескольких добавлений"""
    initial_count = db_client.get_total_queries()

    for wallet_params in TEST_WALLETS:
        wallet = create_wallet_data(*wallet_params)
        db_client.create_wallet_query(wallet)

    assert db_client.get_total_queries() == initial_count + len(TEST_WALLETS)
